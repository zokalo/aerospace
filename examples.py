# -*- encoding: utf-8 -*-
""" Examples for high-level functions
"""
import aerospace

# Free lift model:
# helium rubber balloon with payload
kwargs = {'duration': 180*60,
          'bal_mass': 3.0,
          'bal_diam': 2.164,
          'payload': 1.05,
          'plot_save_as': 'example.png'}
exit_code = aerospace.balloon.model_free_lift(**kwargs)

# Design platform:
# plot schematic view at ground and at maximum altitude
kwargs = {'bal_mass': 3,
          'bal_diam': 2.164,
          'nbals': 3,
          'side_len': 2.7,
          'dmin': 0.5,
          'payload': 1.05,
          'plot_show': True}
exit_code = aerospace.platform.plot_ngon(**kwargs)
