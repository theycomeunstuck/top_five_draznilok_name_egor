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
  Analyze(); // надо научиться вызывать эту функцию пока активен delay или придумать костыль.
  //delay for 100 second before next read
  delay(100000);
}

void Analyze() {
  int mq135_Value = analogRead(GAS_SENSOR_PIN);     //датчик газа
  int ky036_Value = analogRead(TOUCH_SENSOR_PIN);   //датчик касания (металла)
  int ph_Value = analogRead(PH_SENSOR_PIN);         //датчик ph

  //get weird value
  float ppm = getPPM(mq135_Value);
  float pH = CALIBRATION_FACTOR * ((ph_Value * OPERATING_VOLTAGE / 1023) + ZERO_SHIFT); //formula from documentation  http://wiki.amperka.ru/products:troyka-ph-sensor
  int touch = ky036_Value > threshold ? 0 : 1; // touch

  //mq135 data
  Serial.println(ppm);

  //ky036 data
  Serial.print(touch);

  //ph data
  Serial.println(pH, 2); // round. (py| import math math.ceil(ph_value) )
}

float getPPM(mq135_Value) {
  float rs = 1023.0 / sensorValue - 1.0;    // Вычисляем сопротивление в данный момент
  float ratio = rs / RZERO;                 // Вычисляем отношение rs / чистый воздух (погрешность)
  float ppm = pow(10, (log10(ratio) - 1.0309) / -0.2107);  // Вычисляем PPM по формуле
  return ppm;
}


// ToDO
// line 42: calibration_factor может изменяться с эксплуатацией. через год использования эта переменная долнжа быть с другим значением.
// чтобы автоматически изменять эту переменную, нужно прикрутить как-то 2 жидкости с точным и неизменнным ph, сравнивать и получать новое значение переменной
// !! ph в неких пробирках, описанных на line выше, могут измениться из-за каких-то газов, которые не будут являться критичными для трансформатора!!


  // different way to get ph. for universal sensors
  //float pH = 14.0 - (float(ph_Value) * (14.0 - 0.0) / 1023.0); // pH = 14 - (V_sensor - V_offset) * (14 - 0) / V_range
  // probably its not true, cause ph_value can be not equal (V_sens - V_0ffset). and V_range its from 0-5v. typically v_offset == 2.5v, cause were use analogread

  // different way to get touch sensor. through voltage
  //float voltage_ky036 = ky036_Value * (5.0 / 1023.0);