# -*- encoding: utf-8 -*-
""" Capacity tests of ode-integrators

@timeit
def compute_magic(n):
     #function definition
     #....
Or re-alias the function you want to time.

compute_magic = timeit(compute_magic)
"""
# Standard libs:
import time
# Site-packages:
import numpy as np
from scipy.integrate import ode
# Custom libs:
import aerospace
from aerospace import gas, material, const

REPEAT = 10


# Wrapper
def timeit(f):
    def timed(*args, **kw):
        dt = 0
        for i in range(1, REPEAT):
            ts = time.time()
            result = f(*args, **kw)
            te = time.time()
            dt += te-ts
        dt /= REPEAT
        print('func:%r args:[%r, %r]\nMean time: %2.4f sec' %
              (f.__name__, args, kw, dt))
        return result
    return timed


# ODE-function for model
def odefun(time, y, balloon, payload):
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
    tf = aerospace.balloon.is_burst(h)
    return tf


@timeit
def free_lift_scipy_ode(duration, bal_mass, bal_diam, payload, plot_save_as):
    """ The same as aerospace.balloon.model_free_lift
    but using scipy ode-solver
    """
    balloon = aerospace.balloon.BalloonStatic(
        bal_mass=bal_mass,
        bal_diam=bal_diam,
        bal_mat=material.BY_NAME['rubber'],
        gas=gas.BY_NAME['helium'])

# Шаг детализации процесса по времени, с
    tstep = duration/100.0 if duration < 100.0 else 1
    time_points = np.arange(0, duration, tstep)

    # solve the DEs
    # -----------------------------------------------------------
    # Create solver
    y0 = [0, 0]
    t0 = 0
    r = ode(odefun).set_integrator('vode', method='bdf')
    r.set_initial_value(y0, t0).set_f_params(balloon, payload)
    dt = 1
    while r.successful() and r.t < duration:
        r.integrate(r.t+dt)
        # print(r.t, r.integrate(r.t+dt))


    # alt = y_sln[:, 0]
    # vel = y_sln[:, 1]
    #
    # # Максимальная высота
    # alt_max = max(alt)
    # # Момент достижения макс. высоты
    # time_alt_max = time[np.where(alt == alt_max)][0]
    #
    # # Индекс высшей точки в массиве
    # ind_max = np.argmax(alt)
    #
    # # Скрыть некорректные точки расчёта после разрыва шара
    # time = time[:ind_max]
    # alt = alt[:ind_max]
    # vel = vel[:ind_max]


# Free lift model: helium rubber balloon with payload
kwargs = {'duration': 180*60,
          'bal_mass': 3.0,
          'bal_diam': 2.164,
          'payload': 1.05,
          'plot_save_as': ''}

# Test 1 (scipy)
free_lift_scipy_ode(**kwargs)
# Test 2 (odespy)
free_lift = timeit(aerospace.balloon.model_free_lift)
free_lift(**kwargs)
