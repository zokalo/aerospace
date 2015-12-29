# -*- encoding: utf-8 -*-
"""Свойства газообразных веществ

Структура пакета:
gas/
    helium
    ... и другие вещества

Принятые обозначения и размерности:
    mu [кг/моль] - молярная масса
"""
# Modules of package to import
import helium
__all__ = ['helium', ]

# Global gas names
# used to import specified gas properties, i.e.
# >>> gas = importlib.import_module(aerospace.gas.HELIUM)
HELIUM = 'aerospace.gas.helium'

# Gas names dictionary
# used to import specified gas properties, i.e.
# >>> gas = importlib.import_module(aerospace.gas.BY_NAME['helium'])
BY_NAME = {
    'helium': HELIUM,
}
