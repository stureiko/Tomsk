import inspect
import subprocess
import time
import pyautogui as pyg
import pyperclip
import re
import logging
import os
import sys
import pandas as pd
import numpy as np
from python_imagesearch.imagesearch import imagesearch_loop, imagesearch
import yaml
import warnings

import window_list

mouse_speed = .5

logger = logging.getLogger(__name__)
stdout_logger = logging.getLogger('stdout_logger')

# Создать папку для логов
if not os.path.isdir("log"):
    os.mkdir("log")

# Настройка обработчика и форматировщика для logger'a в файл
file_handler = logging.FileHandler(f"log\\main.log", mode='w')
file_formatter = logging.Formatter("%(levelname)-8s %(asctime)s %(funcName)s: %(message)s", "%Y-%m-%d %H:%M:%S")
# Добавление форматировщика к обработчику
file_handler.setFormatter(file_formatter)

# Настройка обработчика и форматировщика для logger'a в stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_formatter = logging.Formatter("[%(levelname)s] %(funcName)s: %(message)s", "%Y-%m-%d %H:%M:%S")
stdout_handler.setFormatter(stdout_formatter)

# добавление обработчика к логгеру
logger.addHandler(file_handler)
stdout_logger.addHandler(stdout_handler)


def open_tomsk(parameters):
    """
    Открывает схему томской системы
    """
    x = parameters['coordinate']['Menu_7_Input']['x']
    y = parameters['coordinate']['Menu_7_Input']['y']
    logger.debug(f'Open menu 7. x: {x}, y:{y}')
    # Open menu '7 Ввод'
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.click(x=x, y=y)

    # Select 'Схемы ГТС из библиотеки'
    x = parameters['coordinate']['Shemas_drom_library']['x']
    y = parameters['coordinate']['Shemas_drom_library']['y']
    logger.debug(f'Open shema menu. x: {x}, y: {y}')
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.click(x=x, y=y)

    # Select folder with shema
    x = parameters['coordinate']['target_folder']['x']
    y = parameters['coordinate']['target_folder']['y']
    logger.debug(f'Open library. x: {x}, y: {y}')
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.click(x=x, y=y)

    # Select 'Томская система'
    x = parameters['coordinate']['target_shema']['x']
    y = parameters['coordinate']['target_shema']['y']
    logger.debug(f'Select Tomsk system. x: {x}, y: {y}')
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.click(x=x, y=y)
    time.sleep(1)


def is_window_open(title: str) -> bool:
    res = False
    for x in pyg.getAllWindows():
        if title == x.title:
            res = True
            break
    return res


def click(parameters: dict, key: str, click=False, double_click=False):
    x = parameters['coordinate'][key]['x']
    y = parameters['coordinate'][key]['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    if click:
        if double_click:
            pyg.doubleClick(x=x, y=y)
        else:
            pyg.click(x=x, y=y)
    time.sleep(0.3)


def run_calculation(parameters) -> (bool, []):
    # Select '1 Расчет'
    # inspect.stack()[0][3]
    logger.debug('Select Rashet')
    click(parameters=parameters, key='Menu_1_Raschet', click=True)

    # Select 'Оптимизация режима работы ГТС'
    logger.debug('Select Optimizing')
    click(parameters=parameters, key='Menu_Optimisation', click=True)
    #
    # # Select button 'Выполнить оптимизацию'
    logger.debug('Select Make optimization')
    click(parameters=parameters, key='Button_make_optimisation', click=True)

    # Ждем появления окна что расчет завершен
    logger.debug('Wait modal window "Calculation complete"')

    fatal_error = False
    calculation_complete = False
    while not calculation_complete:
        if is_window_open('АСТРА-ГАЗ'):
            logger.error('Critical error in calculation')
            click(parameters=parameters, key='Critical_error_in_calculation', click=True)
            fatal_error = True
            print('Waiting Critical error')
            time.sleep(.1)

        elif is_window_open("Режимно-технологические расчеты"):
            calculation_complete = True
            click(parameters=parameters, key='Optimisation_complete_OK_button', click=True)
            time.sleep(.1)
        else:
            time.sleep(.1)

    # Анализируем логи расчета на предмет ошибок
    logger.info('Check calculation for errors')
    result_error = analyse_calculation_logs()
    if result_error[0]:
        logger.info('Calculation complete without errors')
    else:
        logger.error('There are errors in calculation')

    # Закрываем окно с результатами расчетов
    click(parameters=parameters, key='Close_window_with_calculation_result', click=True)
    # pyg.moveTo(x=1330, y=250, duration=mouse_speed)
    # # pyg.click(x=1330, y=250)
    if fatal_error:
        return False, []
    else:
        return result_error


def analyse_calculation_logs() -> (bool, []):
    res = []
    logger.info('Select calculations logs')

    # Идем в окно расчета и копируем логи в буфер обмена
    pyg.moveTo(x=600, y=762, duration=mouse_speed)
    pyg.click(x=600, y=762)
    pyg.hotkey('ctrl', 'a')
    pyg.hotkey('ctrl', 'c')

    # Получаем логи из буфера обмена
    spam = pyperclip.paste()
    # Ищем в логах сообщение об ошибке расчета
    # если оно есть - кидаем False иначе возвращаем True
    err = re.search(r'Внимание ! Расчет выполнен с нарушением ограничений !', spam)
    if err:
        logger.warning('There are some errors in calculation!')
        res = re.findall(r'N узла =\s+\d+', spam)
        for s in res:
            try:
                match = re.search(r'\d+', s)
                logger.warning(f'Error in node: {match[0]}')
            except Exception:
                logger.error(s)
        return False, res
    else:
        logger.info('There are no errors in calculation')
        return True, res


def load_new_data(file_name: str, parameters: dict):
    logger.debug('Open menu 7')
    # Open menu '7 Ввод'
    click(parameters=parameters, key='Menu_7_Input', click=True)

    logger.debug('Open load data from Excel')
    # Open menu "Load data from excel"
    click(parameters=parameters, key='Open_data_from_excel', click=True)

    # Select file
    logger.debug('Select button "View"')
    click(parameters=parameters, key='Select_excel_file_button', click=True)

    logger.debug('Select file name field')
    click(parameters=parameters, key='Select_input_line', click=False)
    logger.debug(f'Insert file name: {file_name}')
    pyg.write(file_name)
    time.sleep(.5)

    # Read file
    logger.debug('Read source file')
    click(parameters=parameters, key='Open_file_button', click=True)

    # Click "Ввод"
    logger.debug('Clic input button')
    click(parameters=parameters, key='Load_data_button', click=True)

    # Распознаем что файл загружен по красной надписи "Выбор типа объектов"
    pos = None

    logger.debug('Waiting loading data')
    while not pos:
        logger.debug('Wait Select_object.png')
        pos = imagesearch_loop(image='img\\Select_object.png', timesample=0.5)
    logger.debug('Select_object.png found')

    # Выбор типа объекта
    logger.debug('Select object type button')
    click(parameters=parameters, key='Object_type_list', click=True)

    # Выбор ПЗГ
    logger.debug('Select objects: "PZG"')
    click(parameters=parameters, key='Object_type_pzg', click=True)

    # Перетаскиваем названия ГРС
    logger.debug('Start move GRS name')
    x = parameters['coordinate']['Select_pzg_name']['x']
    y = parameters['coordinate']['Select_pzg_name']['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.mouseDown(button='left')
    x = parameters['coordinate']['Move_to_name_field']['x']
    y = parameters['coordinate']['Move_to_name_field']['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.mouseUp(button='left')
    time.sleep(.5)

    # Перетаскиваем расходы ГРС
    logger.debug('Start move GRS consumption')
    x = parameters['coordinate']['Select_consumption']['x']
    y = parameters['coordinate']['Select_consumption']['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.mouseDown(button='left')
    x = parameters['coordinate']['Move_to_consumption_field']['x']
    y = parameters['coordinate']['Move_to_consumption_field']['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.mouseUp(button='left')
    time.sleep(.5)

    # Давим кнопку "В Астру"
    logger.debug('Press button "To Astra"')
    click(parameters=parameters, key='Select_button_in_Astra', click=True)

    # Распознаем что загрузка произошла по надписи "Запись данных закончена"
    pos = [-1, -1]
    n = 0
    while pos[0] != -1 or n < 10:
        n += 1
        pos = imagesearch('img\\Not_loaded.png')

        if pos[0] != -1:
            logger.error(f'Some object not loaded from file {file_name}')
            # x = parameters['coordinate']['Select_not_loaded']['x']
            # y = parameters['coordinate']['Select_not_loaded']['y']
            # pyg.moveTo(x=x, y=y, duration=mouse_speed)
            # pyg.click(x=x, y=y)
            # pyg.mouseDown(button='left')
            # pyg.moveTo(x=x-200, y=y-50, duration=mouse_speed)
            # pyg.mouseUp(button='left')
            # pyg.hotkey('ctrl', 'c')
            # spam = pyperclip.paste()
            # logger.error(f'Not loaded objects: \n{spam}')
            break

    logger.debug('Close window for load data')
    click(parameters=parameters, key='Select_button_exit_from_excel_load_data', click=True)


def save_not_loaded_objects(text: str, file_name: str):
    with open(file=file_name, mode='w') as file:
        file.write(text)


def show_ks_novosibirsk(parameters):
    x = parameters['coordinate']['show_KS_novosibirsk']['x']
    y = parameters['coordinate']['show_KS_novosibirsk']['y']
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.mouseDown(button='left')
    pyg.moveTo(x=x - 900, y=y - 400, duration=mouse_speed)
    pyg.mouseUp(button='left')


def set_maximise_astra(parameters):
    x = parameters['coordinate']['max_button']['x']
    y = parameters['coordinate']['max_button']['y']
    logger.debug(f'Press to max button. x: {x}, y: {y}')
    pyg.moveTo(x=x, y=y, duration=mouse_speed)
    pyg.click(x=x, y=y)


def load_coordinates(file_name: str):
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)


def main():
    # Load coordinates
    parameters = load_coordinates('config\\config.yaml')
    if parameters['log_level'] == 'debug':
        logger.setLevel(logging.DEBUG)
    elif parameters['log_level'] == 'info':
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    stdout_logger.setLevel(logging.INFO)
    logger.info('Start app')
    # Установить флаг - выбросить исключение если не найдена область экрана
    pyg.useImageNotFoundException()

    # Отключить вывод FutureWarnings
    warnings.filterwarnings('ignore')

    time.sleep(2)

    # Запустить АСТРУ
    astra = subprocess.Popen('C:\\TP7\\TUM1\\AstraGaz.exe')
    logger.info('Start Astra: C:\\TP7\\TUM1\\AstraGaz.exe')
    time.sleep(2)
    # Развернуть Астру на весь экран
    set_maximise_astra(parameters=parameters)
    # Открыть схему Томской системы
    logger.info('Open Tomsk shema')
    logger.debug('Call open_tomsk(parameters=parameters)')
    try:
        open_tomsk(parameters=parameters)
    except Exception:
        logging.error('Error in function open_tomsk()', exc_info=True)

    # Показать на экране сброс на КС Новосибирская
    logger.info('Show KS Novosibirsk')
    logger.debug('Call func: show_ks_novosibirsk(parameters=parameters)')
    show_ks_novosibirsk(parameters=parameters)

    logger.info('Fist calculation')
    # Установить текущую производительность (начальное потребление) по всем ГРС
    # и убедиться что расчет завершен без ошибок

    # Установить начальное потребление
    logger.info('Set base consumption')
    load_new_data(file_name='C:\\TP7\\TUM1\\data\\input_data.xls', parameters=parameters)

    # Запустить расчет режима
    logger.info('Ferst calculation')
    logger.debug('Call function run_calculation(parameters=parameters)')
    calc_res = run_calculation(parameters=parameters)
    logger.info(f'First calc status: {calc_res[0]}')

    # Если расчет завершен без ошибок - то приступить к оптимизации
    # т.е поиску максимальных резервов
    # if True:
    if calc_res[0]:
        logger.info('Start Optimisation')
        optimize(parameters=parameters)
        logger.info('Optimisation complete')
        save_data(file_name='C:\\TP7\\TUM1\\data\\save_data.xls', parameters=parameters)
        os.remove('C:\\TP7\\TUM1\\data\\calc.xls')
        logger.info("Close Astra")
        close_astra()
    else:
        time.sleep(1)
        logger.error('There are some errors in in first calculation!')
        close_astra()



def optimize(parameters: dict):
    reserv_limit = parameters['reserv_limit']
    logger.debug('Start optimisation')
    logger.debug('Step in optimisation loop, while reserv > 0.5')
    # Получить ограничение на количество шагов оптимизации
    max_optimisation_steps = parameters['max_optimisation_steps']
    optimisation_step = 0
    while optimisation_step < max_optimisation_steps:
        save_data(file_name='C:\\TP7\\TUM1\\data\\save_data.xls', parameters=parameters)
        optimisation_step += 1
        logger.info(f'Optimisation step {optimisation_step} from {max_optimisation_steps}')
        logger.debug('Recalculate reserv with close Novosibirsk')
        # Закрыть выход на КС Новосибирск
        switch_novosibirsk(parameters=parameters)
        time.sleep(.5)
        # Запустить расчет доступного резерва
        calc_res = run_calculation(parameters=parameters)
        # Получить доступный резерв с КС Новосибирск
        reserv = get_reserv(parameters=parameters)
        logger.info(f'Current reserv: {reserv}')
        stdout_logger.info(f'Optimization step {optimisation_step}, Current reserv: {reserv}')
        logger.debug('Open Novosibirsk')
        # Открыть сброс на КС Новосибирск
        switch_novosibirsk(parameters=parameters)
        logger.info(f'Check reserv: {reserv}.')
        # Если текущий резерв меньше заданного лимита то сохраняем данные расчета и выходим
        if reserv < reserv_limit:
        #     # save_data()
            break
        logger.debug('Reserv > 0.5')
        logger.debug('set calc_res = (False, [])')
        # Иначе если текущий резерв больше заданного лимита, то
        # запускаем процесс оптимизации
        calc_res = (False, [])
        # Пока результат расчета не достигнет True
        while not calc_res[0]:
            logger.warning(f'Distribute reserv {reserv}')
            logger.debug('Call distribute_reserv(reserv=reserv)')
            # Распределить текущий резерв по узлам системы и сохранить результаты в файл
            # calc.xls для загрузки в систему
            distribute_reserv(reserv=reserv, file='C:\\TP7\\TUM1\\data\\save_data.xls')
            stdout_logger.info(f'Distribute reserv {reserv}')
            logger.debug('Call load_new_data(file_name="C:\\TP7\\TUM1\\data\\calc.xls"')
            # Загрузить новые данные по потреблению по узлам системы
            load_new_data(file_name='C:\\TP7\\TUM1\\data\\calc.xls', parameters=parameters)
            logger.debug('Run calculation')
            # Запустить расчет режима
            calc_res = run_calculation(parameters=parameters)

            logger.info(f'Calculation with reserv status: {calc_res[0]}')
            # Если расчет завершен без ошибок и предупрежждений, т.е. вернул True тогда выходим из цикла оптимизации
            # и возвращаемся в начало (закрываем Новосибирск и проверяем объем резерва)

            # Если расчет завершен с ошибками - то уменьшаем резерв вдвое и возвращаемся к распределению уменьшенного
            # резерва по узлам
            if not calc_res[0]:
                logger.debug(f'Current reserv: {reserv}')
                reserv /= 2
                logger.warning(f'Decrease reserv. Current reserv: {reserv}')
                logger.info('Recalculate reserv')



def save_data(file_name: str, parameters: dict):
    logger.info(f'Save GRS flows to Excel file {file_name}')
    # Select > on left side
    click(parameters=parameters, key='left_>', click=True)
    click(parameters=parameters, key='save_data_select_PZG', click=True)
    click(parameters=parameters, key='save_data_doc', click=True)
    click(parameters=parameters, key='save_data_select_type_PZG', click=True)
    click(parameters=parameters, key='save_data_select_all_PZG', click=True)
    #
    click(parameters=parameters, key='save_data_select_param_n_asdu', click=True)
    click(parameters=parameters, key='save_data_select_param_code_in_db', click=True)
    click(parameters=parameters, key='save_data_select_param_code_ooo', click=True)
    click(parameters=parameters, key='save_data_select_param_db_type', click=True)
    click(parameters=parameters, key='save_data_select_calc_param_q', click=True)
    click(parameters=parameters, key='save_data_select_doc', click=True)
    click(parameters=parameters, key='save_data_select_menu_print', click=True)
    click(parameters=parameters, key='save_data_select_menu_to_excel', click=True)
    click(parameters=parameters, key='save_data_select_file_name', click=True, double_click=True)
    pyg.write(file_name)
    click(parameters=parameters, key='save_data_select_save_button', click=True)
    pos = False
    while not pos:
        pos = imagesearch_loop(image='img\\Save_data_OK.png', timesample=0.5)

    click(parameters=parameters, key='save_data_select_button_OK', click=True)
    click(parameters=parameters, key='save_data_close_PZG_data', click=True)
    click(parameters=parameters, key='save_data_close_doc_window', click=True)
    click(parameters=parameters, key='save_data_close_panel', click=True)

def distribute_reserv(reserv: float, file: str):
    df = pd.read_excel(file, index_col=0)
    df['max_flow'] = df['Q(r)\nтыс.м3/час'] + reserv / df.shape[0]

    logger.debug('Load limits')
    df_limits = pd.read_excel('C:\\TP7\\TUM1\\data\\limits.xls', index_col=0)

    df_calc = pd.merge(df, df_limits, how='inner', on='Код в\nбазе')
    df_calc.to_excel('C:\\TP7\\TUM1\\data\\calc_log.xls')
    df_calc = df_calc.drop(columns=['Номер\nАСДУ_y', 'Код\nООО_y', 'Тип\nбазы_y'], axis=1)
    df_calc = df_calc.rename(columns={'Номер\nАСДУ_x': 'Номер\nАСДУ',
                                      'Код\nООО_x': 'Код\nООО',
                                      'Тип\nбазы_x': 'Тип\nбазы'})

    while reserv >= 0.5:
        df_calc['full'] = df_calc['max_flow'] >= df_calc['Проектная']
        df_calc['delta'] = (df_calc['max_flow'] - df_calc['Проектная']) * df_calc['full']
        df_calc.loc[df_calc['full'], 'max_flow'] = df_calc['Проектная']
        reserv = df_calc['delta'].sum()
        df_calc['delta'] = 0
        df_calc.loc[df_calc['full'] == False, 'max_flow'] += reserv / df_calc.loc[df_calc['full'] == False].shape[0]
        logger.debug(f'Distribution reserv. Current reserv = {reserv}')

    df_calc = df_calc.round({'max_flow': 3})
    df_calc.to_excel('C:\\TP7\\TUM1\\data\\calc.xls',
                     columns=['Наименование ГРС', 'Номер\nАСДУ', 'Код в\nбазе', 'Код\nООО', 'Тип\nбазы', 'max_flow'])

    if os.path.isfile('C:\\TP7\\TUM1\\data\\calc_log.xls'):
        df_log = pd.read_excel('C:\\TP7\\TUM1\\data\\calc_log.xls', index_col=0)
        ex_num = max_experiment_number(df_log)
        new_ex_name = 'max_flow_' + str(ex_num + 1)
        df_log[new_ex_name] = df_calc['max_flow']
        df_log.to_excel('C:\\TP7\\TUM1\\data\\calc_log.xls')
    else:
        df_log = df_calc
        df_calc.to_excel('C:\\TP7\\TUM1\\data\\calc_log.xls',
                         columns=['Наименование ГРС', 'Номер\nАСДУ', 'Код в\nбазе', 'Код\nООО', 'Тип\nбазы',
                                  'max_flow'])


def max_experiment_number(df: pd.DataFrame) -> int:
    ex_num = 0
    for i, _ in enumerate(df.columns):
        txt = df.columns[i]
        x = re.search("max_flow_\d*$", txt)
        if x:
            x = re.search('\d*$', x[0])
            try:
                int(x[0])
                ex_num = max(ex_num, int(x[0]))
            except ValueError:
                pass
    return ex_num


def get_reserv(parameters) -> float:
    logger.info('Get reserv')
    # Идем на "Сброс на новосибирск"
    click(parameters=parameters, key='Down_to_Novosibirsk', click=True)

    # Выбираем "Данные по ПЗГ"
    click(parameters=parameters, key='Select_PZG_Data', click=True)

    # Выбираем "Печать" - ввод данных в Excel
    pos = imagesearch_loop(image='img\\Novosibirsk_out.png', timesample=0.5)

    pyg.moveTo(x=pos[0] + 80, y=pos[1] + 50, duration=mouse_speed)
    pyg.click(x=pos[0] + 80, y=pos[1] + 50)
    time.sleep(.3)

    # # Вывод данных в Excel
    pyg.moveTo(x=pos[0] + 100, y=pos[1] + 150, duration=mouse_speed)
    pyg.click(x=pos[0] + 100, y=pos[1] + 150)
    time.sleep(.3)

    # Идем к названию файла для экспорта
    click(parameters=parameters, key='Move_to_export_file_name', click=True, double_click=True)
    # #
    # Вводим название файла
    pyg.write('C:\\TP7\\TUM1\\data\\novosibirsk.xls')
    #
    # # Давим Сохранить
    click(parameters=parameters, key='Select_save_to_file', click=True)
    # #
    # Закрываем модальное окно
    pos = imagesearch_loop(image='img\\Save_OK.png', timesample=0.5)

    pyg.moveTo(x=pos[0] + 400, y=pos[1] + 110, duration=mouse_speed)
    pyg.click(x=pos[0] + 400, y=pos[1] + 110)
    time.sleep(.3)

    # Закрываем окно с результатами
    pos = imagesearch_loop(image='img\\Novosibirsk_out_close.png', timesample=0.5)

    pyg.moveTo(x=pos[0] + 250, y=pos[1] + 20, duration=mouse_speed)
    pyg.click(x=pos[0] + 250, y=pos[1] + 20)
    time.sleep(.3)

    # Читаем файл в DataFrame
    df = pd.read_excel('C:\\TP7\\TUM1\\data\\novosibirsk.xls')
    reserv = df.loc[1, 'Значение']

    logger.info(f'"get_reserv" return reserv: {reserv}')
    return reserv
    # return 0


def close_astra():
    pyg.moveTo(x=1890, y=20, duration=.3)
    pyg.click(x=1890, y=20)
    pyg.moveTo(x=1000, y=610, duration=.3)
    pyg.click(x=1000, y=610)


def switch_novosibirsk(parameters):
    logger.debug('Switch Novosibirsk')
    # Открыть "2 Корректировка"
    click(parameters=parameters, key='Menu_2_Correct', click=True)

    # # Выбрали "Cостояние кранов"
    click(parameters=parameters, key='Select_valves_state', click=True)

    # Идем на Новосибирск и кликаем по крану
    click(parameters=parameters, key='Valve_Novosibirsk', click=True)

    # Идем в меню и закрываем "Мзменение кранов"
    click(parameters=parameters, key='Finish_valves_change', click=True)


if __name__ == '__main__':
    main()
