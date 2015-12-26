# -*- coding: utf-8 -*-
"""
Интерфейсный файл для связи с приложением aerospace (где бы оно не находилось)

пример:
#получаем директорию в которой находися (на случай переноса хостов итд)
import os
app_path = os.path.dirname(__file__)

#добавляем наш путь и другие нужные пути в системный список чтобы импортитьвать модули
if app_path not in sys.path: 
    sys.path.insert(0, app_path)

if app_path + '/some_app_packeges' not in sys.path:
    sys.path.insert(0, app_path + '/some_app_packeges')
   
#импортируем что надо
from aerospace import launch
"""
import balloon


def launch_somethin(cats):
    '''
    launch(cats)
    '''
    return 'cats in space!'


def balloon_free_lift(*args, **kwargs):
    """ Моделирование процесса свободного подъёма для шара с полезной нагрузкой

    Функция создаёт изображение-график, если в аргументе <plot_save_as> для
    него передано имя
    ---------------------------------------------------------------------------
    :param duration:      продолжительность моделируемого процесса, с
    :param bal_mass:      масса метеошара, кг
    :param bal_diam:      диаметр метеошара в состоянии без растяжения, м
    :param bal_mat:       наименование материала метеошара. Варианты:
                          {'rubber', }
                          (см пакет <material>)
    :param bal_gas:       наименование наполняющего газа метеошара. Варианты:
                          {'helium', }
                          (см пакет <gas>)
    :param payload:       полезная нагрузка, поднимаемая метеошаром, кг
    :param plot_show:     True/False отображение графика процесса
    :param plot_save_as:  путь к сохраняемому файлу графика, с расширением.
                          '' - пустая строка - не сохранять изображение
                          '..'
    ---------------------------------------------------------------------------
    :return:              exit_status:
                          0 - успешное завршение
                          1 - некорректные входные данные
                          2 - ошибка создания объекта метеошара
                          3 - ошибка интегрирования системы ОДУ
                          4 - ошибка создания графика решения
    """
    return balloon.model_free_lift(*args, **kwargs)
