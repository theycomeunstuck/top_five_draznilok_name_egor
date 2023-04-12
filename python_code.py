import serial

#Запуская код, мы подразумеваем УЖЕ подключенный комплект ардуино со вшитым скетчем arduino_code.cpp 
def arduino_port():
    arduino_port = None
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description:
            arduino_port = p.device

port = arduino_port()
ser = serial.Serial(por t, 9600)
print(f"Connected to Arduino on {port}")

ppm = ser.readline().decode().strip()
touch = ser.readline().decode().strip()
ph = ser.readline().decode().strip()




# Serial.print("PPM: ");
#   Serial.println(ppm);
  
#   //ky036 data
#   Serial.print("Voltage: ");
#   Serial.print(voltage);
#   Serial.println("V");

#   //ph data
#   Serial.print("pH: ");
#   Serial.println(pHValue, 2); // round. (py| import math math.ceil(ph_value) )

print(data)

ser.close()