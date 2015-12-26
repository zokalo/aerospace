# -*- encoding: utf-8 -*-
""" Примеры вызовов функций
"""
import balloon

# Моделирование процесса свободного подъёма для шара с полезной нагрузкой
kwargs = {'duration': 180*60,
          'bal_mass': 3.0,
          'bal_diam': 2.164,
          'payload': 1.05,
          'plot_save_as': 'example.png'}
exit_code = balloon.model_free_lift(**kwargs)
