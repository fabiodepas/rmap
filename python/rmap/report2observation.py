#!/usr/bin/env python
# Copyright (c) 2019 Paolo Patruno <p.patruno@iperbole.bologna.it>
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 

__author__ = "Paolo Patruno"
__copyright__ = "Copyright (C) 2017 by Paolo Patruno"


import rmap.settings
import paho.mqtt.client as paho
import os, sys
import logging
import time
import json
import signal
from rmap import rmapmqtt
import traceback


class report2observation(object):

  def __init__(self,mqtt_host,mqttuser, mqttpassword ):

    self.mqtt_host=mqtt_host
    self.mqttc = paho.Client(self.client_id, clean_session=True)
    self.terminateevent=terminate

    self.mqttc.username_pw_set(mqttuser,mqttpassword)

    self.mqttc.on_message = self.on_message
    self.mqttc.on_connect = self.on_connect
    self.mqttc.on_disconnect = self.on_disconnect
    self.mqttc.on_publish = self.on_publish
    self.mqttc.on_subscribe = self.on_subscribe

    # set timezone to GMT
    os.environ['TZ'] = 'GMT'
    time.tzset()

#    self.mqttc.will_set("clients/" + self.client_id, payload="Adios!", qos=0, retain=False)


  def cleanup(self,signum, frame):
    '''Disconnect cleanly on SIGTERM or SIGINT'''

#    self.mqttc.publish("clients/" + self.client_id, "Offline")
    self.mqttc.disconnect()
    logging.info("Disconnected from broker; exiting on signal %d", signum)
    sys.exit(signum)

  def terminate(self):
    '''Disconnect cleanly on terminate event'''

#    self.mqttc.publish("clients/" + self.client_id, "Offline")
    self.mqttc.disconnect()
    logging.info("Disconnected from broker; exiting on terminate event")
    sys.exit(0)


  def on_connect(self,mosq, userdata, flags, rc):
    logging.info("Connected to broker at %s as %s" % (self.mqtt_host, self.client_id))

#    self.mqttc.publish("clients/" + self.client_id, "Online")

    for topic in self.map:
        logging.debug("Subscribing to topic %s" % topic)
        self.mqttc.subscribe(topic, 0)

  def on_publish(self,mosq, userdata, mid):
    logging.debug("pubblish %s with id %s" % (userdata, mid))


  def on_message(self,mosq, userdata, msg):

    now = int(time.time())
    
    # Find out how to handle the topic in this message: slurp through our map 
    # this is not needed if all things are right; I cannot receive topics that I have not subscribed
    for t in self.map:
        if paho.topic_matches_sub(t, msg.topic):
            # print "%s matches MAP(%s) => %s" % (msg.topic, t, self.map[t])

            (user, slug) = self.map[t]

            # JSON: try and load the JSON string from payload             
            try:
                st = json.loads(msg.payload.decode())
                
                metadata=st["metadata"]
                #remove string part after second  (  2017-12-22T09:52:30.245940879Z  )
                mytime=metadata.pop("time",time.strftime("%Y-%m-%dT%H:%M:%S",time.gmtime(now))).split(".")[0]
                dt=datetime.datetime.strptime(mytime,"%Y-%m-%dT%H:%M:%S")                
            
                payload=base64.b64decode(st["payload_raw"])
                #print "payload: ",payload
                logging.debug("hex: %s" % binascii.hexlify(payload))
                
                nbits=len(binascii.hexlify(payload))*4
                template=int(binascii.hexlify(payload),16)
                
                #temp=int(binascii.hexlify(payload),16)
                #template=0
                #for i in xrange(0,nbits):
                    #    if (testBit(temp,i)!=0):
                #        template=setBit(template,nbits-i-1)
                    
                logging.debug("int: %d" %template)
                logging.debug("bynary: {0:b}".format(template))
                #print "bynary:",bin(template)
                
                nbit=8
                start=nbits-nbit
                numtemplate=bitextract(template,start,nbit)
                
                #                             TEMPLATE NUMBER 1
                if numtemplate > 0 and numtemplate < len(rmap_core.ttntemplate):

                    try:

                        #close django connection to DB to be sure we have a new active connection handler
                        try:
                            connection.close()
                        except Exception as e:
                            print(("django connection close error",e))
                        
                        mystation=StationMetadata.objects.get(slug=slug,ident__username=user)
                    except ObjectDoesNotExist :
                        logging.error("StationMetadata matching query does not exist")
                        return
                    if not mystation.active:
                        logging.error("disactivated station: %s %s ; do nothing!" % (slug,user) )
                        return

                else:
                    logging.error("Unknown template %d " % numtemplate)
                    return

            except Exception as exception:
                # log and retry on exception 
                logging.error('Exception occured: ' + str(exception))
                logging.error(traceback.format_exc())
                logging.error("error decoding message: skip it and do nothing!")
                #raise
                return

            try:
                #print "ident=",user,"username=",rmap.settings.mqttuser,"password=",rmap.settings.mqttpassword,"lon=",mystation.lon,"lat=",mystation.lat,"network=","fixed","host=","rmap.cc","prefix=","sample","maintprefix=","maint"                    
                logging.info("ident=%s username=%s password=%s lon=%f lat=%f network=fixed host=localhost prefix=sample maintprefix=maint" % (user,rmap.settings.mqttuser,"fakepassword",mystation.lon,mystation.lat))
                mqtt=rmapmqtt.rmapmqtt(ident=user,username=rmap.settings.mqttuser,password=rmap.settings.mqttpassword,lon=mystation.lon,lat=mystation.lat,network="fixed",host="localhost",prefix="sample",maintprefix="maint",logfunc=logging.debug)
                
                mytemplate=rmap_core.ttntemplate[numtemplate]
                for bcode,param in list(mytemplate.items()):
                    
                    nbit=param["nbit"]
                    start-=nbit
                    bval=bitextract(template,  start, nbit)
                    if (bval != ((1 << nbit) - 1)):
                        #val=(bval+param["offset"])/float(param["scale"])
                        val=bval+param["offset"]
                        datavar={bcode:{"t": dt,"v": val}}
                        #print "datavar=",datavar
                        logging.info("timerange=%s level=%s bcode=%s val=%d" % (param["timerange"],param["level"],bcode,val))
                        mqtt.data(timerange=param["timerange"],level=param["level"],datavar=datavar)

                mqtt.disconnect()
                #if mqtt.mqttc._sock:
                #    mqtt.mqttc._sock.close()
                #if mqtt.mqttc._sockpairW:
                #    mqtt.mqttc._sockpairW.close()
                #if mqtt.mqttc._sockpairR:
                #    mqtt.mqttc._sockpairR.close()
                    
            except Exception as exception:
                logging.error("Topic %s error decoding or publishing; payload: [%s]" %
                             (msg.topic, msg.payload))
                logging.error('Exception occured: ' + str(exception))
                logging.error(traceback.format_exc())

                # if some exception occour here, ask to terminate; if not the thread will stall forever
                self.terminateevent.set()

            finally:
                return

    logging.error("Message topic do not match any topics that I have subcribed [%s]", t)
    # somethings go wrong here; I cannot receive topics that I have not subscribed
    self.terminateevent.set()
    

  
  def on_subscribe(self,mosq, userdata, mid, granted_qos):
    logging.debug("Subscribed: "+str(mid)+" "+str(granted_qos))

  def on_disconnect(self,mosq, userdata, rc):

    if rc == 0:
        logging.info("Clean disconnection")
    else:
        logging.info("Unexpected disconnect (rc %s); reconnecting in 5 seconds" % rc)
        time.sleep(5)


        
  def run(self):
    logging.info("Starting %s" % self.client_id)
    logging.info("INFO MODE")
    logging.debug("DEBUG MODE")


    rc=self.mqttc.connect_async(self.mqtt_host, 1883, 60)
        
    self.mqttc.loop_start()

    while not self.terminateevent.isSet():
        time.sleep(5)

    self.terminate()
    self.mqttc.loop_stop()
        
if __name__ == '__main__':

    MQTT_HOST = os.environ.get('MQTT_HOST', 'eu.thethings.network')
    
    m2g=report2observation(MQTT_HOST,mqttuser, mqttpassword)
    m2g.run()
        

    
