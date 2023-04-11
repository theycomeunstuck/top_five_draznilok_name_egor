import time
import datetime
import random
from colorama import init
from colorama import Fore, Back



# Дефолтная функция вывода информации, её нужно вызывать каждый час.
def hourly_message(ph_level, temperature, knockouts_number, shutdowns_number, overloads_number):
    init()
    current_datetime = datetime.datetime.now()
    month = current_datetime.month
    if len(str(month)) == 1:
        month = f'0{str(month)}'
    verdict_time = f'{current_datetime.day}.{month}.{current_datetime.year} {current_datetime.hour}:{current_datetime.minute}'

    # В эти два списка будут заноситься фразы из словарей, которые потом выведет код
    verdict_warn = []
    verdict_err = []

    # Словарь с сообщениями при варнингах
    ERRORS_DICT = {
        'ph_level': 'Критический уровень наличия примесей в масле, требуется замена!',
        'temperature': 'Критический уровень температуры масла, #ЧТО-ТО ТРЕБУЕТСЯ#!',
        'knockouts_number': 'Критическое количество выбиваний! #ЧТО-ТО ТРЕБУЕТСЯ!#',
        'shutdowns_number': 'Критическое количество экстренных выключений! #ЧТО-ТО ТРЕБУЕТСЯ!#',
        'overloads_number': 'Критическое количество перегрузок! #ЧТО-ТО ТРЕБУЕТСЯ!#'
    }
    # Словарь с сообщениями при ошибках
    WARNINGS_DICT = {
        'ph_level': 'Уровень наличия примесей в масле ниже среднего. Предположительный остаточный ресурс: {ddhh}, #ЧТО-ТО РЕКОМЕНДУЕТСЯ#',
        'temperature': 'Уровень температуры масла ниже среднего. Предположительный остаточный ресурс: {ddhh}, #ЧТО-ТО РЕКОМЕНДУЕТСЯ#!',
        'knockouts_number': 'Количество выбиваний ниже среднего. Предположительный остаточный ресурс: {ddhh}, #ЧТО-ТО РЕКОМЕНДУЕТСЯ!#',
        'shutdowns_number': 'Количество экстренных выключений ниже среднего. Предположительный остаточный ресурс: {ddhh}, #ЧТО-ТО РЕКОМЕНДУЕТСЯ!#',
        'overloads_number': 'Количество перегрузок ниже среднего. Предположительный остаточный ресурс: {ddhh}, #ЧТО-ТО РЕКОМЕНДУЕТСЯ!#'
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

    if 0 <= overloads_number < 10:
        verdict_warn.append(WARNINGS_DICT['overloads_number'])
    elif overloads_number < 0:
        verdict_err.append(ERRORS_DICT['overloads_number'])

    # Проверка, заполнился ли список с фразами - ошибками
    if len(verdict_err):
        print(verdict_time, Fore.BLUE + '|',  Fore.RED + ' '.join(verdict_err), Fore.YELLOW + ' '.join(verdict_warn), '\033[39m', sep=' ')
    # Проверка, заполнился ли список с фразами - варнингами
    elif len(verdict_warn):
        print(verdict_time, Fore.BLUE + '|', Fore.YELLOW + ' '.join(verdict_warn), '\033[39m', sep=' ')
    # Если всё ок
    else:

        print(verdict_time, Fore.BLUE + '|', Fore.GREEN + 'Устройство в порядке',  '\033[39m',)

