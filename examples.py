# -*- encoding: utf-8 -*-
""" Examples for high-level functions
"""
import aerospace

# Free lift model: helium rubber balloon with payload
kwargs = {'duration': 180*60,
          'bal_mass': 3.0,
          'bal_diam': 2.164,
          'payload': 1.05,
          'plot_save_as': 'example.png'}
exit_code = aerospace.balloon.model_free_lift(**kwargs)
