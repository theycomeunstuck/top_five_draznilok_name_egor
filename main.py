import serial


# Запуская код, мы подразумеваем УЖЕ подключенный комплект ардуино со вшитым скетчем arduino_code.cpp
# поиск нужного порта comX ардуино.
def arduino_port():
    port = None
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description:
            port = p.device
    return port

# плохо не плохо трансформеру.
def analyze(ppm, touch, ph):
    #ppm more than 100 is bad
    #touch == 1 is bad
    #ph should be in 6-8
    trouble = []
    if ppm > 100:
        trouble.append("ppm")
    if touch == 1:
        trouble.append("touch")
    if ph < 6.0 or ph > 8.0: #один источник говорит 6.0-8, другой 6.0 9.0. доказать бы это...:
        trouble.append("ph")

    #если какая-то проблема, то вывести что не так и на даню кинуть то сколько осталось ну и вот эту часть
    if True:
        pass
    if True:
        pass
    if True:
        pass
    #чтобы не забыли сделать
def get_actual():
    pass

port = arduino_port()
ser = serial.Serial(port, 9600)
print(f"Connected to Arduino on {port}")

ppm = ser.readline().decode().strip() #100 --  bad
touch = ser.readline().decode().strip() # 1 == True
ph = ser.readline().decode().strip() #6-8


data = f'ppm: {ppm}\noxid: {True if touch > 0 else False}\npH: {ph}'
print(data)

ser.close()