# -*- encoding: utf-8 -*-
""" Платформа-аэростат

Модуль проектных расчётов для платформ-аэростатов
Все единицы в [СИ]
"""
# Standard libs:
from __future__ import print_function
import math
import sys
import warnings
# Site-packages:
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# Custom:
from balloon import BalloonStatic
import const
import gas
import material
import utils


def plot_ngon(bal_mass, bal_diam, nbals, side_len, dmin, payload=0.0,
              plot_show=False, plot_save_as=''):
    """ Функция построения эскиза размеров плоской платформы-многоугольника
    (с указанием максимально достижимой высоты подъёма)
    - с метеошарами на каждом углу
    - с центральным отверстием не менее заданного диаметра
    ---------------------------------------------------------------------------
    :param bal_mass:  масса метеошара, кг
    :param bal_diam:  диаметр метеошара без растяжения, м
    :param nbals:     число углов / число метеошаров, шт (не менее 3)
    :param side_len:  длина стороны многоугольника / расстояние между шарами, м
    :param dmin:      минимальный диаметр центрального отверстия, м
    :param payload:   масса платформы и полезной нагрузки на платформе, кг
    :param plot_show:     True/False отображение графика (эскиза)
    :param plot_save_as:  путь к сохраняемому файлу графика, с расширением.
                          '' - пустая строка - не сохранять изображение (по
                          умолчанию)
    ---------------------------------------------------------------------------
    :return:              exit_status:
                          0 - успешное завршение
                          1 - некорректные входные данные
                          2 - ошибка создания объекта метеошара

                          4 - ошибка создания графика решения

    Примеры вызова:
    >>> plot_ngon(bal_mass=3,
    ...           bal_diam=2.164,
    ...           nbals=3,
    ...           side_len=2.7,
    ...           dmin=0.5,
    ...           payload=1.05,
    ...           plot_show=True,
    ...           plot_save_as='doctest.png')
    0
    """

    # Check inputs.
    # -----------------------------------------------------------
    try:
        # Confirm input numeric types
        bal_mass = float(bal_mass)
        if bal_mass <= 0:
            raise ValueError('bal_mass must be positive')
        bal_diam = float(bal_diam)
        if bal_diam <= 0:
            raise ValueError('bal_diam must be positive')
        nbals = int(nbals)
        if nbals < 2:
            raise ValueError('nbals must be integer greater than 2')

        side_len = float(side_len)
        if side_len <= 0:
            raise ValueError('side_len must be positive')
        dmin = float(dmin)
        if dmin <= 0:
            raise ValueError('dmin must be positive')
        payload = float(payload)
        if payload < 0:
            raise ValueError('payload must be non-negative')
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1

    # Create balloon instance
    # -----------------------------------------------------------
    try:
        balloon = BalloonStatic(bal_mass=bal_mass,
                                bal_mat=material.RUBBER,
                                gas=gas.HELIUM,
                                bal_diam=bal_diam)
    except Exception as err:
        print(err, file=sys.stderr)
        return 2

    # Create geometrical-condition checker function
    # -----------------------------------------------------------
    # Calc radius of a circumscribed circle (over N-gon)
    rcs = side_len/(2*math.sin(const.pi/nbals))

    def geom_check(alt, bal=balloon, rcs=rcs, l=side_len, dmin=dmin):
        bal_d = bal.get_diam(alt)
        if bal_d > l:
            # Balloons contact
            return False
        # Check dmin
        if (bal_d/2.0 + dmin/2.0) > rcs:
            # Balloons overlap central shaft
            return False
        return True

    # Create platform plot-function
    # -----------------------------------------------------------
    def plot(ax, alt, bal=balloon, n=nbals, rcs=rcs, l=side_len, dmin=dmin):
        ax.set_aspect('equal')
        # ax.set_title(u'H = ' + str(round(alt/1000, 1)) + u' км')

        # Plot dmin-shaft circle
        circle_shaft = plt.Circle((0, 0), radius=dmin/2.0,
                                  edgecolor='k',
                                  facecolor='k',
                                  fill=True,
                                  linestyle='-',
                                  linewidth=1.0)
        ax.add_artist(circle_shaft)

        # Polar coordinate <theta> [radians] of platform corners
        corners_theta = np.arange(0.0, 2*math.pi, 2*math.pi/n)
        # Polar coordinate <rho> [meters] is equal to radius
        # of a circumscribed circle (over N-gon)
        corners_rho = [rcs]*n

        # Plot N=gon
        for i in range(0, n):
            x_end, y_end = utils.pol2cart(corners_theta[i], corners_rho[i])
            x_beg, y_beg = utils.pol2cart(corners_theta[i-1], corners_rho[i-1])
            ax.plot([x_beg, x_end], [y_beg, y_end],
                    color='b',
                    linestyle='-',
                    linewidth=2.0)

        # Plot balloons
        bal_rad = bal.get_radius(alt)
        for theta, rho in zip(corners_theta, corners_rho):
            x_cnt, y_cnt = utils.pol2cart(theta, rho)
            circle_bal = plt.Circle((x_cnt, y_cnt), radius=bal_rad,
                                  edgecolor='r',
                                  facecolor=None,
                                  fill=False,
                                  linestyle='--',
                                  linewidth=1.0)
            ax.add_artist(circle_bal)

        ax.set_xlim([-(l+bal_rad), (l+bal_rad)])
        ax.set_ylim([-(l+bal_rad), (l+bal_rad)])

    # ========================================================================
    # Now we need to detect maximum altitude where geom_check() returns True.
    # Cycle-variable:
    alt = 0
    # Commentary
    txt_alt_limiter = u"Высота ограничена "
    # Cycle step
    alt_step = 100  # step of altitude checking
    # Run iter-cycle
    weight_payload = payload*const.g
    while geom_check(alt):
        f_arh = balloon.get_forces_sum(alt)
        f_sum = f_arh - weight_payload
        if f_sum <= 0:
            txt_alt_limiter += u"подъёмной силой"
            break
        if balloon.is_burst(alt):
            txt_alt_limiter += u"предельным растяжением шара"
            break
        alt += alt_step
    txt_alt_limiter += u"геометрическими параметрами платформы"
    alt_max = alt
    # ========================================================================

    # Create 2 subplots: (1) at H=0 and (2) at H=Hmax
    try:
        if plot_show or plot_save_as:
            matplotlib.rcParams['font.size'] = 12
            matplotlib.rcParams['font.family'] = utils.get_font()
            matplotlib.rcParams["axes.grid"] = True
            f, (ax1, ax2) = plt.subplots(1, 2)
            # at H=0
            plot(ax1, alt=0)
            ax1.set_title(u'Исходное состояние:\nH = 0 км')
            # at Hmax
            plot(ax2, alt=alt_max)
            ax2.set_title(u'Макс. высота:\nH = ' +
                          str(round(alt/1000, 1)) + u' км' +
                          '\n' + txt_alt_limiter)
            if plot_show:
                plt.show()
            if plot_save_as:
                f.set_size_inches(18.5, 10.5)
                f.savefig(plot_save_as, dpi=100, bbox_inches='tight')
            plt.close()
        else:
            warnings.warn("All output's disabled.")
    except Exception as err:
        print(err, file=sys.stderr)
        return 4

    return 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
