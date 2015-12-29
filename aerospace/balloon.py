# -*- encoding: utf-8 -*-
""" Метеошар

Все единицы в [СИ]
"""
# Standard libs:
from __future__ import print_function as print_function
import importlib
import math
import sys
import warnings
# Site-packages:
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import odespy
# Custom libs:
import const
import gas
import material
import isa
import utils


class BalloonStatic(object):
    """Класс описывающий состояние метеошара в некоторый момент времени

    Примеры:
    >>> balloon = BalloonStatic(bal_mass=3.0,
    ...                   bal_mat=material.RUBBER,
    ...                   gas=gas.HELIUM,
    ...                   bal_diam=2.164)

    >>> balloon.get_radius(alt=0.0)
    1.082

    >>> balloon.get_volume(0.0)
    5.306038436052428

    # Толщина стенки, мм
    >>> balloon.get_wall_thickness(0.0)*1000.0
    0.2228618724597761

    # Диаметр разрыва
    >>> balloon.get_diam(alt=38100.0)
    13.109034008497218

    # Относительная деформация разрыва, %
    >>> balloon.get_rel_strain(38100.0)*100.0
    505.77791166807845

    # Напряжение при деформации растяжения на высоте разрыва, мПа
    >>> balloon.get_stress(38100.0)/10.0**6.0
    76.34383572348354

    # Толщина стенки при разрыве, мм
    >>> balloon.get_wall_thickness(38100.0)*1000.0
    0.006073078679838702
    """

    _cx = 0.5  # коэффициент лобового сопротивления сферы

    def __init__(self, bal_mat, bal_mass,
                 gas, gas_mass=None,
                 bal_rad=None, bal_diam=None):
        """
        :param bal_mat:  Материал оболочки: константа <material>
                         например:
                         material.RUBBER
        :param bal_mass: Масса оболочки шара, кг
        :param gas:      Наименование наполняющего газа: константа пакета <gas>
                         например:
                         gas.HELIUM
        :param gas_mass: Масса газа в шаре, по умолчанию рассчитывается по
                         заполнению шара на высоте H=0 сферы радиусом r0
        :param bal_rad:  начальный радиус (в состоянии без растяжения), м
        :param bal_diam: начальный диаметр (в состоянии без растяжения), м
                         (указывать только r0 или d0)
        """
        object.__init__(self)

        if bal_rad and not bal_diam:
            self._r0 = bal_rad
        elif bal_diam and not bal_rad:
            self._r0 = bal_diam/2.0
        else:
            raise TypeError(
                'Unspecified initial diameter (arg d0) or radius (arg r0) or '
                'specified both of them. Use arg d0 or r0.')

        self._bal_mass = bal_mass
        self._bal_mat = importlib.import_module(bal_mat)

        self._gas = importlib.import_module(gas)
        if not gas_mass:
            alt = 0.0
            vol = 4.0/3.0*const.pi*self.r0**3.0
            gas_mass = self.gas.mu * isa.p(alt) * vol / (const.R * isa.t(alt))
        self.gas_mass = gas_mass

    @property
    def cx(self):
        return self._cx

    @property
    def r0(self):
        return self._r0

    @property
    def d0(self):
        return self._r0*2

    @property
    def bal_mass(self):
        return self._bal_mass

    @property
    def bal_mat(self):
        return self._bal_mat

    @property
    def gas(self):
        return self._gas

    def get_volume(self, alt, temp=None):
        """Объём метеошара в указанном аргументами состоянии
        Параметры состояния:
        :param alt:   высота над уровнем моря, м
        :param temp:  температура газа в шаре, К. Если не указана, то
                      принимается равной температуре окружающей среды на высоте
        :return:      Объём метеошара, м3
        """
        if not temp:
            temp = isa.t(alt)
        press = isa.p(alt)
        # Объём газа в шаре при атмосферном давлении на высоте alt
        vol = self.gas_mass * const.R * temp / (self.gas.mu * press)
        return vol

    def get_radius(self, alt, temp=None):
        """Радиус метеошара в указанном аргументами состоянии
        Параметры состояния:
        :param alt:   высота над уровнем моря, м
        :param temp:  температура газа в шаре, К. Если не указана, то
                      принимается равной температуре окружающей среды на высоте
        :return:      радиус метеошара, м
        """
        # ToDo: оценить уменьшение радиуса шара при поджатии газа оболочкой
        # и обновить с учётом этого предел относительной деформации
        vol = self.get_volume(alt, temp)
        rad = (3.0/4.0*vol/const.pi)**(1.0/3.0)
        return rad

    def get_diam(self, alt, temp=None):
        """Диаметр метеошара в указанном аргументами состоянии"""
        return 2.0*self.get_radius(alt, temp)

    def get_stress(self, alt, temp=None):
        """ Напряжение, sigma, Па """
        rel_strain = self.get_rel_strain(alt, temp)
        stress = rel_strain*self.bal_mat.E/(1.0-self.bal_mat.mu)
        return stress

    def is_burst(self, alt, temp=None):
        """ Шар взорвётся на этой высоте при этой температуре?
        :param alt:  высота над уровнем моря, м
        :param temp: температура газа в шаре, К. Если не указана, то
                     принимается равной температуре окружающей среды на высоте
        :return:     True если взорвётся, иначе False
        """
        rel_strain = self.get_rel_strain(alt, temp)
        return rel_strain > self.bal_mat.rel_strain_max

    def get_rel_strain(self, alt, temp=None):
        """ Относительная деформация e=dL/L """
        diam = self.get_diam(alt, temp)
        return (diam-self.d0) / self.d0

    def get_wall_thickness(self, alt, temp=None):
        """ Толщина стенки, м """
        rad = self.get_radius(alt, temp)
        th = self.bal_mass / (4*self.bal_mat.rho*const.pi*rad**2)
        return th

    def get_force_archimedes(self, alt, temp=None):
        """ Подъёмная сила (сила Архимеда), действующая на шар.
        Положительное значение соответствует направлению набора высоты.
        :param alt:  высота над уровнем моря, м
        :param temp: температура газа в шаре, К. Если не указана, то
                     принимается равной температуре окружающей среды на высоте
        :return:     сила Архимеда, Н
        """
        f_arch = isa.rho(alt) * const.g * self.get_volume(alt, temp)
        return f_arch

    def get_force_air_resistance(self, alt, vel, temp=None):
        """ Сопротивление окружающей среды движению шара.
        Положительное значение соответствует направлению набора высоты.
        :param alt:   высота над уровнем моря, м
        :param vel:   вертикальная скорость, м/с
        :param temp:  температура газа в шаре, К. Если не указана, то
                      принимается равной температуре окружающей среды на высоте
        :return:      сила воздушного сопротивления, Н
        """
        if abs(vel) > 150.0:
            warnings.warn(
                u"Скорость {0} м/с вне диапазона применения для "
                u"используемой формулы сопротивления воздуха (не применима "
                u"для скоростей близких к скорости звука)".format(vel))
        if abs(vel) < 1.0:
            n = 1.0
        else:
            n = 2.0
        f_res = self.cx * isa.rho(alt)*abs(vel)**n/2.0 * \
            (const.pi*self.get_radius(alt, temp)**2.0)
        # Установить знак противоположный направлению движения
        f_res = - math.copysign(f_res, vel)
        return f_res

    def get_forces_sum(self, alt, vel=0.0, temp=None, is_burst=False):
        """ Сумма всех сил, действующих на шар
        Положительное значение соответствует направлению набора высоты.
        :param alt:   высота над уровнем моря, м
        :param vel:   вертикальная скорость, м/с
        :param temp:  температура газа в шаре, К. Если не указана, то
                      принимается равной температуре окружающей среды на высоте
        :param is_burst:  состояние шара: True - шар взорвался, иначе False
        :return:      сила, Н
        """
        f_sum = 0.0
        f_gravity = -(self.bal_mass + self.gas_mass*(not is_burst)) * const.g
        f_sum += f_gravity
        if not is_burst:
            f_archimedes = self.get_force_archimedes(alt, temp)
            f_resistance = self.get_force_air_resistance(alt, vel, temp)
            f_sum += f_archimedes
            f_sum += f_resistance
        return f_sum

    def get_acceleration(self, alt, vel=0.0, temp=None, is_burst=False):
        """ Ускорение шара
        Положительное значение соответствует направлению набора высоты.
        :param alt:   высота над уровнем моря, м
        :param vel:   вертикальная скорость, м/с
        :param temp:  температура газа в шаре, К. Если не указана, то
                      принимается равной температуре окружающей среды на высоте
        :param is_burst:  состояние шара: True - шар взорвался, иначе False
        :return:      ускорение, м/с^2
        """
        f_sum = self.get_forces_sum(alt, vel, temp, is_burst)
        acc = f_sum / (self.get_mass())
        return acc

    def get_mass(self, is_burst=False):
        """ Масса шара и газа в нём, м/с^2
        :param is_burst:  состояние шара: True - шар взорвался, иначе False
        :return:          масса шара и газа в нём, м/с^2
        """
        mass = self.bal_mass
        if not is_burst:
            mass += self.gas_mass
        return mass


def model_free_lift(duration,
                    bal_mass, bal_diam, bal_mat='rubber',
                    bal_gas='helium',
                    payload=0,
                    plot_show=False, plot_save_as='',
                    ):
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
    ---------------------------------------------------------------------------
    :return:              exit_status:
                          0 - успешное завршение
                          1 - некорректные входные данные
                          2 - ошибка создания объекта метеошара
                          3 - ошибка интегрирования системы ОДУ
                          4 - ошибка создания графика решения

    Примеры вызова:
    >>> model_free_lift(duration=180*60,
    ...                 bal_mass=3.0,
    ...                 bal_diam=2.164,
    ...                 payload=1.05,
    ...                 plot_save_as='doctest.png',
    ...                 plot_show=False)
    Called function:
        model_free_lift(
            duration=10800,
            bal_mass=3.0,
            bal_diam=2.164,
            bal_mat=rubber,
            bal_gas=helium,
            payload=1.05,
            plot_show=False,
            plot_save_as=doctest.png)
    RK4 terminated at t=7018
    Successfull end.
    0

    >>> kwargs = {'duration': 180*60,
    ...           'bal_mass': 3.0,
    ...           'bal_diam':2.164,
    ...           'payload': 1.05,
    ...           'plot_save_as': 'doctest.png'}
    >>> model_free_lift(**kwargs)
    Called function:
        model_free_lift(
            duration=10800,
            bal_mass=3.0,
            bal_diam=2.164,
            bal_mat=rubber,
            bal_gas=helium,
            payload=1.05,
            plot_show=False,
            plot_save_as=doctest.png)
    RK4 terminated at t=7018
    Successfull end.
    0

    """
    # Send inputs to log
    log_msg = "Called function:\n" \
              "    model_free_lift(\n" \
              "        duration={0},\n" \
              "        bal_mass={1},\n" \
              "        bal_diam={2},\n" \
              "        bal_mat={3},\n" \
              "        bal_gas={4},\n" \
              "        payload={5},\n" \
              "        plot_show={6},\n" \
              "        plot_save_as={7})".\
        format(duration, bal_mass, bal_diam, bal_mat, bal_gas,
               payload, plot_show, plot_save_as)
    print(log_msg)

    # Create ODE-function for model
    def odefun(y, time, balloon, payload):
        """ Дифф. закон Ньютона -
        уравнение процесса свободного подъёма для шара с полезной нагрузкой
        В форме Коши: dy/dt = f(y, t)

        Внимание! Условие разрыва шара должно проверяться извне функции.
        """
        alt = y[0]
        vel = y[1]

        # Model equations
        f_sum_bal = balloon.get_forces_sum(alt, vel)
        f_sum_pl = - payload*const.g
        f_sum = f_sum_bal + f_sum_pl
        mass = balloon.get_mass() + payload
        return [vel, f_sum/mass]

    def terminator(y, t, step_no):
        # Функция, останавливающая интегрирование при разрыве метеошара
        h = y[step_no][0]
        tf = balloon.is_burst(h)
        return tf

    # Check inputs.
    # -----------------------------------------------------------
    try:
        # Confirm input numeric types
        duration = float(duration)
        if duration <= 0:
            raise ValueError('duration must be positive')
        bal_mass = float(bal_mass)
        if bal_mass <= 0:
            raise ValueError('bal_mass must be positive')
        bal_diam = float(bal_diam)
        if bal_diam <= 0:
            raise ValueError('bal_diam must be positive')
        payload = float(payload)
        if payload < 0:
            raise ValueError('payload must be non-negative')

        # Define material
        if not (bal_mat in material.__all__):
            raise ValueError("Unknown balloon material name ", bal_mat)

        # Define gas
        if not (bal_gas in gas.__all__):
            raise ValueError("Unknown gas name ", bal_gas)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1

    # Create balloon instance
    # -----------------------------------------------------------
    try:
        balloon = BalloonStatic(
            bal_mass=bal_mass,
            bal_diam=bal_diam,
            bal_mat=material.BY_NAME[bal_mat],
            gas=gas.BY_NAME[bal_gas])
    except Exception as err:
        print(err, file=sys.stderr)
        return 2

    # Шаг детализации процесса по времени, с
    tstep = duration/100.0 if duration < 100.0 else 1
    time_points = np.arange(0, duration, tstep)

    # solve the DEs
    # -----------------------------------------------------------
    try:

        # Create solver (Runge-Kutta, 4th order)
        solver = odespy.RK4(
            odefun,
            f_args=(balloon, payload))
        solver.set_initial_condition([0, 0])
        y_sln, time = solver.solve(
            time_points,
            terminate=terminator)

        alt = y_sln[:, 0]
        vel = y_sln[:, 1]

        # Максимальная высота
        alt_max = max(alt)
        # Момент достижения макс. высоты
        time_alt_max = time[np.where(alt == alt_max)][0]

        # Индекс высшей точки в массиве
        ind_max = np.argmax(alt)

        # Скрыть некорректные точки расчёта после разрыва шара
        time = time[:ind_max]
        alt = alt[:ind_max]
        vel = vel[:ind_max]
    except Exception as err:
        print(err, file=sys.stderr)
        return 3

    # Plot
    # -----------------------------------------------------------
    if plot_show or plot_save_as:
        try:
            # масштаб отображения
            scale_v = 1.0       # скорости
            scale_h = 1.0/1000.0    # высоты
            scale_t = 1.0/60.0  # времени

            time *= scale_t
            time_alt_max *= scale_t

            alt *= scale_h
            alt_max *= scale_h

            vel *= scale_v

            # Построение графика
            matplotlib.rcParams['font.size'] = 14
            matplotlib.rcParams['font.family'] = utils.get_font()
            matplotlib.rcParams["axes.grid"] = True
            plt.figure()

            plt.plot(
                time, alt, 'b-', linewidth=2.0, label=u'Высота, км')

            plt.plot(
                time, vel, 'r-', linewidth=2.0, label=u'Скорость, м/с')

            plt.xlabel(u'Время, мин')
            matplotlib.pyplot.ylim([0.0, alt_max*1.2])
            plt.legend(loc='upper left', shadow=True)
            plt.title(
                u"Полёт метеошара\n"
                u"(m = {0} кг; Ø = {1} м, нагрузка {2} кг)\n"
                u"Макс. высота {3} км достигнута спустя {4} мин".format(
                    balloon.bal_mass, balloon.d0, payload,
                    round(alt_max), round(time_alt_max)
                ))

            if plot_save_as:
                plt.savefig(plot_save_as, bbox_inches='tight')
            if plot_show:
                plt.show()
            plt.close()
        except Exception as err:
            print(err, file=sys.stderr)
            return 4
    else:
        warnings.warn("All output's disabled.")

    print('Successfull end.')
    return 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    


    
    
    

