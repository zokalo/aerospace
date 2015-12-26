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
__all__ = ['rubber', ]
from . import rubber

# Global materials names
# used to import specified gas properties, i.e.
# >>> mat = material.import_module(material.RUBBER)
RUBBER = 'material.rubber'
