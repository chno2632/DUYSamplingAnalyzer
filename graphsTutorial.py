# from matplotlib import pyplot as plt
# import numpy as np
# import pandas as pd
#
# x_1 = np.linspace(0,5,10)
# y_1 = x_1**2
# #plt.plot = (x_1, y_1)
# plt.title("Days Squared Chart")
# plt.plot(x_1, y_1, color='r', linestyle='--', marker='.')
# plt.show()


# import matplotlib.pyplot as plt
# #import panels as FigureSizeLocator
# from panels import FigureSizeLocator
#
# loc = FigureSizeLocator(2, 3, figwidth=150, hsep=12, vsep=12,
#                         padleft=10, padright=10, padtop=10, padbottom=10)
# fig = plt.figure(figsize=loc.figsize)
#
# for i, pos in enumerate(loc.panel_position_iterator()):
#     ax = fig.add_axes(pos)
#     ax.plot([0, 1, 2], [3, 2, 1])
#     ax.set_title('Panel #{}'.format(i))
#
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplot_mosaic([['left', 'right_top'],
                            ['left', 'right_bottom']])
#fig = plt.figure()
#ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()