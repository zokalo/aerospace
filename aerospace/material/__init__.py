# -*- encoding: utf-8 -*-
"""Свойства газообразных веществ

Структура пакета:
material/
    rubber
    ... и другие вещества

Принятые обозначения и размерности:
    mu [] - коэффициент Пуассона
    E [Па] - модуль упругости
    rho [кг/м3] - плотность
    rel_strain_max [] - предел относительной деформации
"""
# Modules of package to import
import rubber
__all__ = ['rubber', ]

# Global materials names
# used to import specified gas properties, i.e.
# >>> mat = importlib.import_module(aerospace.material.RUBBER)
RUBBER = 'aerospace.material.rubber'

# Material names dictionary
# used to import specified gas properties, i.e.
# >>> mat = importlib.import_module(aerospace.material.BY_NAME['rubber'])
BY_NAME = {
    'rubber': RUBBER,
}
