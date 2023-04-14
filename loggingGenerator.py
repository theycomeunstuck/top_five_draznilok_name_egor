import time
import datetime
import random
from colorama import init
from colorama import Fore, Back



# Дефолтная функция вывода информации, её нужно вызывать каждый час.
def hourly_message(ph_level, temperature, knockouts_number, shutdowns_number, overloads_number):
    list_of_transformers = ["1", "2", "3", "transformator", "test"] # условный список существующий трансформаторов !!!! Принимает только str тк new_text тоже str

    # В эти два списка будут заноситься фразы из словарей, которые потом выведет код
    verdict_warn = []
    verdict_err = []

    # Словарь с сообщениями при варнингах
    ERRORS_DICT = {
        'ph_level': 'Критический уровень наличия примесей в масле, требуется замена!<br>',
        'temperature': 'Критический уровень температуры масла, #Требуется снижение нагрузки на трансформатор или обслуживание трансформатора!#<br>',
        'knockouts_number': 'Критическое количество выбиваний! #Требуется обслуживание трансформатора#<br>',
        'shutdowns_number': 'Критическое количество экстренных выключений! #Требуется обслуживание трансформатора!#<br>',
        'overloads_number': 'Критическое количество перегрузок! #Требуется проверить температуру масла#<br>' #ну тут бы дописать чёт это вообще плохо я напсал
    }
    # Словарь с сообщениями при ошибках
    WARNINGS_DICT = {
        'ph_level': 'Уровень наличия примесей в масле выше среднего. #Рекомендуется обслужить трансформатор#<br>',
        'temperature': 'Уровень температуры масла выше нормы. #Рекомендуется снизить на трансформатор#!<br>',
        'knockouts_number': 'Количество выбиваний выше нормы. #Рекомендуется проверить нагрузку на трансформатор!#<br>',
        'shutdowns_number': 'Количество экстренных выключений выше нормы. #Рекомендуется снизить на трансформатор#<br>',
    }

    # Проверки критериев
    if 0 <= ph_level < 10:
        verdict_warn.append(WARNINGS_DICT['ph_level'])
    elif ph_level < 0:
        verdict_err.append(ERRORS_DICT['ph_level'])

    if 0 <= temperature < 10:
        verdict_warn.append(WARNINGS_DICT['temperature'])
    elif temperature < 0:
        verdict_err.append(ERRORS_DICT['temperature'])

    if 0 <= knockouts_number < 10:
        verdict_warn.append(WARNINGS_DICT['knockouts_number'])
    elif knockouts_number < 0:
        verdict_err.append(ERRORS_DICT['knockouts_number'])

    if 0 <= shutdowns_number < 10:
        verdict_warn.append(WARNINGS_DICT['shutdowns_number'])
    elif shutdowns_number < 0:
        verdict_err.append(ERRORS_DICT['shutdowns_number'])

    if overloads_number > 3: #перегрузки -- плохо. если их мало -- это хорош
        verdict_err.append(ERRORS_DICT['overloads_number'])

    # Проверка, заполнился ли список с фразами - ошибками
    #Предположительный остаточный ресурс: {ddhh}
    dd = random.randint(1, 100)
    hh = random.randint(1, 100)
    if len(verdict_err):
        print("59",  ('| <a style="color: FF2A12">' + ' '.join(verdict_err) + '</a>' + ' <a style="color: #FFB413">' + ' '.join(verdict_warn) + '</a>'))
        return ('| <br><a style="color: #FF2A12">' + ' '.join(verdict_err) + '</a>' + ' <a style="color: #FFB413">' + ' '.join(verdict_warn) + '</a>' + f'<a style="color: deeppink">Предположительный остаточный ресурс: {dd*hh} дней</a>')
    # Проверка, заполнился ли список с фразами - варнингами
    elif len(verdict_warn):
        print("63", ('|  <a style="color: #FFB413">' + ' '.join(verdict_warn) + '</a>'))

        return ('|  <br><a style="color: #FFB413">' + ' '.join(verdict_warn) + '</a>'  + f'<a style="color: deeppink">Предположительный остаточный ресурс: {dd*hh} дней</a>' )
    # Если всё ок
    else:
        print("68", ('| <a style="color: #74ff12">' + 'Устройство в порядке' + '</a>', 'ok'))
        return ('| <br><a style="color: #74ff12">' + 'Устройство в порядке' + '</a>' + f'<a style="color: deeppink">Предположительный остаточный ресурс: {dd*hh} дней</a>')

# print(hourly_message(-20, 5, 20, 20, 20))