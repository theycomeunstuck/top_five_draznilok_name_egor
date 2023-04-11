//Include the MQ-135 library
#include <MQ135.h>


#define GAS_SENSOR_PIN A0
#define TOUCH_SENSOR_PIN A1
#define PH_SENSOR_PIN A2

// Коэффициент перевода напряжения в концентрацию pH. Взято с официальной документации и может отличаться для каждого датчика | for ph sensor
#define CALIBRATION_FACTOR  3.5 // value can be different.

#if defined(__AVR__)
#define OPERATING_VOLTAGE   5.0
#define ZERO_SHIFT          0
#else
#define OPERATING_VOLTAGE   3.3
#define ZERO_SHIFT          1.1
#endif
 


//Initialize the MQ-135 sensor object
MQ135 gasSensor = MQ135(GAS_SENSOR_PIN);
int ky036_Value = 0;
int threshold = 350;

void setup() {

  Serial.begin(9600);
}

void loop() {
  //read sensors value
  int mq135_Value = analogRead(GAS_SENSOR_PIN);     //датчик газа
  int ky036_Value = analogRead(TOUCH_SENSOR_PIN);   //датчик касания (металла)
  int ph_Value = analogRead(PH_SENSOR_PIN);         //датчик ph 




  //get weird value
  float ppm = gasSensor.getPPM();
  float pH = CALIBRATION_FACTOR * ((ph_Value * OPERATING_VOLTAGE / 1023) + ZERO_SHIFT); //formula from documentation  //http://wiki.amperka.ru/products:troyka-ph-sensor

  // different way to get ph. for universal sensors
  //float pH = 14.0 - (float(ph_Value) * (14.0 - 0.0) / 1023.0); // pH = 14 - (V_sensor - V_offset) * (14 - 0) / V_range
  // probably its not true, cause ph_value can be not equal (V_sens - V_0ffset). and V_range its from 0-5v. typically v_offset == 2.5v, cause were use analogread 

  // different way to get touch sensor. through voltage
  //float voltage_ky036 = ky036_Value * (5.0 / 1023.0);

	if (ky036_Value > threshold) { 
	    int touch = 0;
	  } else {
	    int touch = 1; // touch
	  }


  //print to serial
  //mq135 data
  // Serial.print("PPM: ");
  Serial.println(ppm);
  
  //ky036 data
  // Serial.print("Touch: ");
  Serial.print(touch);

  //ph data
  // Serial.print("pH: ");
  Serial.println(pHValue, 2); // round. (py| import math math.ceil(ph_value) )




  //delay for 100 second before next read
  delay(100000);
}




// ToDO
// line 42: calibration_factor может изменяться с эксплуатацией. через год использования эта переменная долнжа быть с другим значением.
// чтобы автоматически изменять эту переменную, нужно прикрутить как-то 2 жидкости с точным и неизменнным ph, сравнивать и получать новое значение переменной
// !! ph в неких пробирках, описанных на line выше, могут измениться из-за каких-то газов, которые не будут являться критичными для трансформатора!!