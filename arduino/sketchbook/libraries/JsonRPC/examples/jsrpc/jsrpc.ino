// create a simple messageing
// with the RH_CC110 class. RH_CC110 class does not provide for addressing or
// reliability, so you should only use RH_CC110 if you do not need the higher
// level messaging abilities.

#include <avr/wdt.h>

#define CONFVER "conf00"


#include "config.h"
#include <EEPROM.h>
#include "EEPROMAnything.h"

#include <avr/wdt.h>

// include the aJSON library
#include <aJSON.h>

// include the JsonRPC library
#include <JsonRPC.h>

// initialize an instance of the JsonRPC library for registering 
// exactly 3 method
JsonRPC rpcserver(3,false ); //serial port with standard protocoll

// initialize a serial json stream for receiving json objects
// through a serial/USB connection
aJsonStream stream(&Serial);
aJsonObject *serialmsg = NULL;

char confver[7] = CONFVER; // version of configuration saved on eeprom

struct config_t               // configuration to save and load fron eeprom
{
  int did;
  void save () {
    int p=0;                  // save to eeprom
    p+=EEPROM_writeAnything(p, confver);
    p+=EEPROM_writeAnything(p, did);
  }
bool load () {                // load from eeprom
    int p=0;
    char ver[7];
    p+=EEPROM_readAnything(p, ver);
    if (strcmp(ver,confver ) == 0){ 
      p+=EEPROM_readAnything(p, did);
      return true;
    }
    else{
      return false;
    }
  }
} configuration;

//-------------

const uint8_t pins [] = {PINS};

//-------------


int pulse(aJsonObject* params)
{

  uint8_t status=0;

  aJsonObject* didParam = aJson.getObjectItem(params, "did");
  if (didParam){
    int did = didParam -> valueint;
    if (did == configuration.did || did == 0 ){     //my did or broadcast
    
      aJsonObject* dstunitParam = aJson.getObjectItem(params, "dstunit");
      if (dstunitParam){
	int dstunit = dstunitParam -> valueint;

	if (dstunit >= 0 && dstunit < sizeof(pins)/sizeof(*pins)){
	  aJsonObject* onoffParam = aJson.getObjectItem(params, "onoff");
	  if (onoffParam){
	    boolean onoff = onoffParam -> valuebool;
	    Serial.print(F("#did: "));
	    Serial.print(did);
	    Serial.print(F(" dstunit: "));
	    Serial.print(dstunit);
	    Serial.print(F(" onoff: "));
	    Serial.println(onoff);

	    digitalWrite(pins[dstunit], ! onoff);

	  }else{
	    Serial.println(F("#no onoff"));
	    status=1;
	  }
	}else{
	  Serial.println(F("#wrong dstunit"));
	  status=2;
	}
      }else{
	Serial.println(F("#no dstunit"));
	status=3;
      }
    }else{
      Serial.println(F("#not for me"));
      status=4;
    }
  }else{
    Serial.println(F("#no did"));
    status=5;
  }


  aJsonObject* mymethod = aJson.detachItemFromObject(serialmsg, "method");
  aJson.addItemToObject(newrpc, "m",mymethod );

  aJsonObject* myparams = aJson.detachItemFromObject(serialmsg, "params");
  aJson.addItemToObject(newrpc, "p",myparams );

  //Serial.println("{\"jsonrpc\": \"2.0\", \"result\":true, \"id\": 0}");	
  if (status) {
    //Serial.println("{\"jsonrpc\": \"2.0\", \"result\":true, \"id\": 0}");	
    aJson.addTrueToObject(serialmsg, "result");
  }else{
    aJson.addFalseToObject(serialmsg, "result");
  }
  
  char serialbuf[SERIALBUFFERSIZE];
  aJson.print(serialmsg,serialbuf, sizeof(serialbuf));
  Serial.println(serialbuf);

  return status;

}


int setdid(aJsonObject* params)
{    
  uint8_t status=1; 
  aJson.deleteItemFromObject(serialmsg, "method");
  
  aJsonObject* myparams = aJson.detachItemFromObject(serialmsg, "params");
  aJsonObject* didParam = aJson.getObjectItem(myparams, "did");
  if (didParam){
    int did = didParam -> valueint;
    configuration.did=did;

    aJson.addTrueToObject(serialmsg, "result");
    char buf[SERIALBUFFERSIZE];
    aJson.print(serialmsg,buf, sizeof(buf));
    Serial.println(buf);
    
    status= 0;
  }
  aJson.deleteItem(params);
  return status;
}

int save(aJsonObject* params)
{    
  uint8_t status=1; 
  aJson.deleteItemFromObject(serialmsg, "method");

  aJsonObject* myparams = aJson.detachItemFromObject(serialmsg, "params");
  
  aJsonObject* saveParam = aJson.getObjectItem(myparams, "eeprom");
  if (saveParam){
    bool eeprom = saveParam -> valuebool;
    
    if (eeprom) configuration.save();
    
    aJson.addTrueToObject(serialmsg, "result");
    char buf[SERIALBUFFERSIZE];
    aJson.print(serialmsg,buf, sizeof(buf));
    Serial.println(buf);
    
    status = 0;
  }

  aJson.deleteItem(params);
  return status;

}


void setup() 
{

  /*
    Nel caso di un chip in standalone senza bootloader, la prima
    istruzione che è bene mettere nel setup() è sempre la disattivazione
    del Watchdog stesso: il Watchdog, infatti, resta attivo dopo il
    reset e, se non disabilitato, esso può provare il reset perpetuo del
    microcontrollore
  */
  wdt_disable();
  
  Serial.begin(115200);
  while (!Serial); // wait for serial port to connect. Needed for native USB
  Serial.println(F("#Started"));

  if (configuration.load()){
    Serial.println(F("#Configuration loaded"));
    Serial.print(F("#did:"));
    Serial.println(configuration.did);
  } else {     
    Serial.println(F("#Configuration not loaded"));
  }

  // register the local method
  // Serial port
  rpcserver.registerMethod("pulse",     &pulse);
  rpcserver.registerMethod("setdid",    &setdid);
  rpcserver.registerMethod("save",      &save);
  
  // initialize the digital pin as an output
  pinMode(13, OUTPUT);

  for (int dstunit=0 ;dstunit  < sizeof(pins)/sizeof(*pins); dstunit++)
    {
      pinMode(pins[dstunit], OUTPUT);
      digitalWrite(pins[dstunit], 1);
    }
}

void mgr_serial(){
  uint8_t err;
    
  if (stream.available()) {
    // skip any accidental whitespace like newlines
    stream.skip();
  }

  if (stream.available()) {

    serialmsg = aJson.parse(&stream);
    if (serialmsg){
      Serial.print(F("#rpc.processMessage:"));
      char serialbuf[SERIALBUFFERSIZE];
      aJson.print(serialmsg, serialbuf, sizeof(serialbuf));
      Serial.println(serialbuf);
    
      err=rpcclient.processMessage(serialmsg);
      Serial.print(F("#rpcserver.processMessage return status:"));
      Serial.print(err);
      if (!err){
	aJson.deleteItem(serialmsg);      
      }else{
	err = 1;
      }
      
    }else{
      Serial.println(F("#skip wrong message"));	
      err = 2;
    }
    if (stream.available()) {
      stream.flush();
    }

    if (err == 1){
      aJsonObject *result = aJson.createObject();
      aJson.addItemToObject(serialmsg, "error", result);
      aJson.addNumberToObject(result, "code", E_INTERNAL_ERROR);
      aJson.addStringToObject(result,"message", strerror(E_INTERNAL_ERROR));   
      
      /*
      if (!rpcid || !msg){
	IF_SDEBUG(DBGSERIAL.println(F("#add null id in response")));
	aJson.addNullToObject(serialmsg, "id");
      } else {
	IF_SDEBUG(DBGSERIAL.println(F("#add id in response")));
        aJson.addNumberToObject(serialmsg, "id", rpcid->valueint);
      }
      */

      char serialbuf[SERIALBUFFERSIZE];

      aJson.print(serialmsg,serialbuf, sizeof(serialbuf));
      Serial.println(serialbuf);
      aJson.deleteItem(serialmsg);

    }
  }
}


void loop()
{
  wdt_reset();
  mgr_serial();
}
