//disable debug at compile time but call function anyway
//#define DISABLE_LOGGING disable

// set the I2C clock frequency 
#define I2C_CLOCK 30418

// define the version of the configuration saved on eeprom
// if you chenge this the board start with default configuration at boot
#define CONFVER "confpwm00"

// pins definitions
#define LED_PIN  13
#define FORCEDEFAULTPIN 8
#define PWM1_PIN  2
#define PWM2_PIN  3
#define ONOFF1_PIN  4
#define ONOFF2_PIN  5
#define ANALOG1_PIN  A0
#define ANALOG2_PIN  A1
