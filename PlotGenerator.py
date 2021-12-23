import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager

class PlotGenerator:
    def __init__(self, path='./', style='./spotify.mplstyle'):
        font_manager.fontManager.addfont('./gotham-medium.otf')
        mpl.style.use(style)
        mpl.rcParams['font.family'] = 'Gotham Medium'