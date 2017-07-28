'''
Atomic plot functions for mcplot-pyqtgraph
'''
import os
import sys
import numpy as np
import pyqtgraph as pg

from pyqtgraph.graphicsItems.LegendItem import LegendItem, ItemSample

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from mccodelib.plotgraph import PNMultiple, PNSingle
from mccodelib.mcplotloader import Data1D, Data2D


def plot(node, i, plt, opts):
    '''
    node : plot node containing data
    i    : index of said data in node
    opts : dict containing options such as --> log, legend, icolormap, verbose, legend_fontsize
    '''
    if type(node) == PNSingle and i != 0:
        raise Exception("inconsistent plot request, idx=%s" % str(i))
    
    data = node.getdata_idx(i)
    
    if type(data) is Data1D:
        view_box = plot_Data1D(data, plt, log=opts['log'], legend=opts['legend'], icolormap=opts['icolormap'], verbose=opts['verbose'], legend_fontsize=opts['legend_fontsize'])
        return view_box, plt
    elif type(data) is Data2D:
        view_box, lyt = plot_Data2D(data, plt, log=opts['log'], legend=opts['legend'], icolormap=opts['icolormap'], verbose=opts['verbose'], legend_fontsize=opts['legend_fontsize'])
        return view_box, lyt
    else:
        raise Exception("unknown plot data type")


GlobalColormap='none'

class ModLegend(pg.LegendItem):
    """
    Modified LegendItem to remove the ugly / in the label. Also reduces text size and padding.
    """
    def __init__(self, offset, text_size='9pt'):
        self.text_size = text_size
        LegendItem.__init__(self, None, offset)
    
    def addItem(self, item, name):
        label = pg.LabelItem(name, size=self.text_size)
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        self.layout.setContentsMargins(0, 0, 0, 0)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(label, row, 1)
        self.updateSize()
        
    def paint(self, p, *args):
        p.setPen(pg.functions.mkPen(255,255,255,100))
        p.setBrush(pg.functions.mkBrush(0,0,0,100))
        p.drawRect(self.boundingRect())

def plot_Data1D(data, plt, log=False, legend=True, icolormap=0, verbose=True, legend_fontsize=10):
    ''' create a plotItem and populate it with data, Data1D '''
    # data
    x = np.array(data.xvals).astype(np.float)
    y = np.array(data.yvals).astype(np.float)
    e = np.array(data.y_err_vals).astype(np.float)
    
    if log:
        nonzeros=[]
        zeros=[]
        for i in range(len(y)):
            if y[i]>0:
                nonzeros.append(i)
            else:
                zeros.append(i)
        if len(nonzeros)>0:
            y[zeros] = np.min(y[nonzeros])/10
            plt.setLogMode(y=True)
        else:
            plt.setLogMode(y=False)
    else:
        plt.setLogMode(y=False)
    
    plt.setXRange(np.min(x), np.max(x), padding=0)
    
    # labels
    plt.setLabels(title=" ",bottom=data.xlabel, left=data.ylabel)
    
    # how to add labels with html styling:
    #plt.titleLabel.item.setHtml('<span style="font-size:5pt; text-align:center;color:#FFFFFF">data.component <br>hest</span>')
    #axis_style = {'color': '#FFF', 'font-size': '5pt'}
    #plt.setLabel(axis='left', text=data.ylabel, **axis_style)
    #plt.setLabel(axis='bottom', text=data.xlabel, **axis_style)
    
    # error bars
    beam = 0
    if len(x) > 1:
        beam = (x[1]-x[0])*0.5
    
    # TODO: Find solution for adding errorbars in the log case
    if not log:
        err = pg.ErrorBarItem(x=x, y=y, height=e, beam=beam)
        plt.addItem(err)
    
    # commit
    if legend:
        plt.legend = ModLegend(offset=(-1, 1), text_size='%spt' % str(legend_fontsize))
        plt.legend.setParentItem(plt.vb)
        # this construct reduces the requiremet for header data in Data1D, in case of an error during parsing of the string
        try:
            lname1 = '<center>%s<br>I = %s</center>' % (data.component, data.values[0])
            if verbose:
                lname1 = '%s [%s]<br><br>%s<br><br>I = %s Err = %s N = %s; %s' % (data.component, data.filename, data.title, data.values[0], data.values[1], data.values[2], data.statistics)
        except:
            lname1 = '%s<br>[%s]' % (data.component, data.filename)
        if lname1:
            plt.plot([x[0]], [y[0]], name=lname1)
    
    # plots data
    plt.plot(x, y)
    
    plt.setMenuEnabled(False)
    vb = plt.getViewBox()
    
    return vb

def get_color_map(idx, pos_min, pos_max):
    # The contents of this function was generated from Matlab using the generate_colormaps.m script
    # 
    # < Paste from next line >
    colormaps={
        'jet'  : np.array([[  0,   0, 143, 255], [  0,   0, 159, 255], [  0,   0, 175, 255], [  0,   0, 191, 255], [  0,   0, 207, 255], [  0,   0, 223, 255], [  0,   0, 239, 255], [  0,   0, 255, 255], [  0,  16, 255, 255], [  0,  32, 255, 255], [  0,  48, 255, 255], [  0,  64, 255, 255], [  0,  80, 255, 255], [  0,  96, 255, 255], [  0, 112, 255, 255], [  0, 128, 255, 255], [  0, 143, 255, 255], [  0, 159, 255, 255], [  0, 175, 255, 255], [  0, 191, 255, 255], [  0, 207, 255, 255], [  0, 223, 255, 255], [  0, 239, 255, 255], [  0, 255, 255, 255], [ 16, 255, 239, 255], [ 32, 255, 223, 255], [ 48, 255, 207, 255], [ 64, 255, 191, 255], [ 80, 255, 175, 255], [ 96, 255, 159, 255], [112, 255, 143, 255], [128, 255, 128, 255], [143, 255, 112, 255], [159, 255,  96, 255], [175, 255,  80, 255], [191, 255,  64, 255], [207, 255,  48, 255], [223, 255,  32, 255], [239, 255,  16, 255], [255, 255,   0, 255], [255, 239,   0, 255], [255, 223,   0, 255], [255, 207,   0, 255], [255, 191,   0, 255], [255, 175,   0, 255], [255, 159,   0, 255], [255, 143,   0, 255], [255, 128,   0, 255], [255, 112,   0, 255], [255,  96,   0, 255], [255,  80,   0, 255], [255,  64,   0, 255], [255,  48,   0, 255], [255,  32,   0, 255], [255,  16,   0, 255], [255,   0,   0, 255], [239,   0,   0, 255], [223,   0,   0, 255], [207,   0,   0, 255], [191,   0,   0, 255], [175,   0,   0, 255], [159,   0,   0, 255], [143,   0,   0, 255], [128,   0,   0, 255]], dtype=np.ubyte),
        'autumn'  : np.array([[255,   0,   0, 255], [255,   4,   0, 255], [255,   8,   0, 255], [255,  12,   0, 255], [255,  16,   0, 255], [255,  20,   0, 255], [255,  24,   0, 255], [255,  28,   0, 255], [255,  32,   0, 255], [255,  36,   0, 255], [255,  40,   0, 255], [255,  45,   0, 255], [255,  49,   0, 255], [255,  53,   0, 255], [255,  57,   0, 255], [255,  61,   0, 255], [255,  65,   0, 255], [255,  69,   0, 255], [255,  73,   0, 255], [255,  77,   0, 255], [255,  81,   0, 255], [255,  85,   0, 255], [255,  89,   0, 255], [255,  93,   0, 255], [255,  97,   0, 255], [255, 101,   0, 255], [255, 105,   0, 255], [255, 109,   0, 255], [255, 113,   0, 255], [255, 117,   0, 255], [255, 121,   0, 255], [255, 125,   0, 255], [255, 130,   0, 255], [255, 134,   0, 255], [255, 138,   0, 255], [255, 142,   0, 255], [255, 146,   0, 255], [255, 150,   0, 255], [255, 154,   0, 255], [255, 158,   0, 255], [255, 162,   0, 255], [255, 166,   0, 255], [255, 170,   0, 255], [255, 174,   0, 255], [255, 178,   0, 255], [255, 182,   0, 255], [255, 186,   0, 255], [255, 190,   0, 255], [255, 194,   0, 255], [255, 198,   0, 255], [255, 202,   0, 255], [255, 206,   0, 255], [255, 210,   0, 255], [255, 215,   0, 255], [255, 219,   0, 255], [255, 223,   0, 255], [255, 227,   0, 255], [255, 231,   0, 255], [255, 235,   0, 255], [255, 239,   0, 255], [255, 243,   0, 255], [255, 247,   0, 255], [255, 251,   0, 255], [255, 255,   0, 255]], dtype=np.ubyte),
        'bone'  : np.array([[  0,   0,   1, 255], [  4,   4,   6, 255], [  7,   7,  11, 255], [ 11,  11,  16, 255], [ 14,  14,  21, 255], [ 18,  18,  26, 255], [ 21,  21,  31, 255], [ 25,  25,  35, 255], [ 28,  28,  40, 255], [ 32,  32,  45, 255], [ 35,  35,  50, 255], [ 39,  39,  55, 255], [ 43,  43,  60, 255], [ 46,  46,  65, 255], [ 50,  50,  70, 255], [ 53,  53,  74, 255], [ 57,  57,  79, 255], [ 60,  60,  84, 255], [ 64,  64,  89, 255], [ 67,  67,  94, 255], [ 71,  71,  99, 255], [ 74,  74, 104, 255], [ 78,  78, 108, 255], [ 81,  81, 113, 255], [ 85,  86, 117, 255], [ 89,  91, 120, 255], [ 92,  96, 124, 255], [ 96, 101, 128, 255], [ 99, 106, 131, 255], [103, 111, 135, 255], [106, 116, 138, 255], [110, 120, 142, 255], [113, 125, 145, 255], [117, 130, 149, 255], [120, 135, 152, 255], [124, 140, 156, 255], [128, 145, 159, 255], [131, 150, 163, 255], [135, 155, 166, 255], [138, 159, 170, 255], [142, 164, 174, 255], [145, 169, 177, 255], [149, 174, 181, 255], [152, 179, 184, 255], [156, 184, 188, 255], [159, 189, 191, 255], [163, 193, 195, 255], [166, 198, 198, 255], [172, 202, 202, 255], [178, 205, 205, 255], [183, 209, 209, 255], [189, 213, 213, 255], [194, 216, 216, 255], [200, 220, 220, 255], [205, 223, 223, 255], [211, 227, 227, 255], [216, 230, 230, 255], [222, 234, 234, 255], [227, 237, 237, 255], [233, 241, 241, 255], [238, 244, 244, 255], [244, 248, 248, 255], [249, 251, 251, 255], [255, 255, 255, 255]], dtype=np.ubyte),
        'colorcube'  : np.array([[ 85,  85,   0, 255], [ 85, 170,   0, 255], [ 85, 255,   0, 255], [170,  85,   0, 255], [170, 170,   0, 255], [170, 255,   0, 255], [255,  85,   0, 255], [255, 170,   0, 255], [255, 255,   0, 255], [  0,  85, 128, 255], [  0, 170, 128, 255], [  0, 255, 128, 255], [ 85,   0, 128, 255], [ 85,  85, 128, 255], [ 85, 170, 128, 255], [ 85, 255, 128, 255], [170,   0, 128, 255], [170,  85, 128, 255], [170, 170, 128, 255], [170, 255, 128, 255], [255,   0, 128, 255], [255,  85, 128, 255], [255, 170, 128, 255], [255, 255, 128, 255], [  0,  85, 255, 255], [  0, 170, 255, 255], [  0, 255, 255, 255], [ 85,   0, 255, 255], [ 85,  85, 255, 255], [ 85, 170, 255, 255], [ 85, 255, 255, 255], [170,   0, 255, 255], [170,  85, 255, 255], [170, 170, 255, 255], [170, 255, 255, 255], [255,   0, 255, 255], [255,  85, 255, 255], [255, 170, 255, 255], [ 43,   0,   0, 255], [ 85,   0,   0, 255], [128,   0,   0, 255], [170,   0,   0, 255], [213,   0,   0, 255], [255,   0,   0, 255], [  0,  43,   0, 255], [  0,  85,   0, 255], [  0, 128,   0, 255], [  0, 170,   0, 255], [  0, 213,   0, 255], [  0, 255,   0, 255], [  0,   0,  43, 255], [  0,   0,  85, 255], [  0,   0, 128, 255], [  0,   0, 170, 255], [  0,   0, 213, 255], [  0,   0, 255, 255], [  0,   0,   0, 255], [ 36,  36,  36, 255], [ 73,  73,  73, 255], [109, 109, 109, 255], [146, 146, 146, 255], [182, 182, 182, 255], [219, 219, 219, 255], [255, 255, 255, 255]], dtype=np.ubyte),
        'cool'  : np.array([[  0, 255, 255, 255], [  4, 251, 255, 255], [  8, 247, 255, 255], [ 12, 243, 255, 255], [ 16, 239, 255, 255], [ 20, 235, 255, 255], [ 24, 231, 255, 255], [ 28, 227, 255, 255], [ 32, 223, 255, 255], [ 36, 219, 255, 255], [ 40, 215, 255, 255], [ 45, 210, 255, 255], [ 49, 206, 255, 255], [ 53, 202, 255, 255], [ 57, 198, 255, 255], [ 61, 194, 255, 255], [ 65, 190, 255, 255], [ 69, 186, 255, 255], [ 73, 182, 255, 255], [ 77, 178, 255, 255], [ 81, 174, 255, 255], [ 85, 170, 255, 255], [ 89, 166, 255, 255], [ 93, 162, 255, 255], [ 97, 158, 255, 255], [101, 154, 255, 255], [105, 150, 255, 255], [109, 146, 255, 255], [113, 142, 255, 255], [117, 138, 255, 255], [121, 134, 255, 255], [125, 130, 255, 255], [130, 125, 255, 255], [134, 121, 255, 255], [138, 117, 255, 255], [142, 113, 255, 255], [146, 109, 255, 255], [150, 105, 255, 255], [154, 101, 255, 255], [158,  97, 255, 255], [162,  93, 255, 255], [166,  89, 255, 255], [170,  85, 255, 255], [174,  81, 255, 255], [178,  77, 255, 255], [182,  73, 255, 255], [186,  69, 255, 255], [190,  65, 255, 255], [194,  61, 255, 255], [198,  57, 255, 255], [202,  53, 255, 255], [206,  49, 255, 255], [210,  45, 255, 255], [215,  40, 255, 255], [219,  36, 255, 255], [223,  32, 255, 255], [227,  28, 255, 255], [231,  24, 255, 255], [235,  20, 255, 255], [239,  16, 255, 255], [243,  12, 255, 255], [247,   8, 255, 255], [251,   4, 255, 255], [255,   0, 255, 255]], dtype=np.ubyte),
        'copper'  : np.array([[  0,   0,   0, 255], [  5,   3,   2, 255], [ 10,   6,   4, 255], [ 15,   9,   6, 255], [ 20,  13,   8, 255], [ 25,  16,  10, 255], [ 30,  19,  12, 255], [ 35,  22,  14, 255], [ 40,  25,  16, 255], [ 46,  28,  18, 255], [ 51,  32,  20, 255], [ 56,  35,  22, 255], [ 61,  38,  24, 255], [ 66,  41,  26, 255], [ 71,  44,  28, 255], [ 76,  47,  30, 255], [ 81,  51,  32, 255], [ 86,  54,  34, 255], [ 91,  57,  36, 255], [ 96,  60,  38, 255], [101,  63,  40, 255], [106,  66,  42, 255], [111,  70,  44, 255], [116,  73,  46, 255], [121,  76,  48, 255], [126,  79,  50, 255], [132,  82,  52, 255], [137,  85,  54, 255], [142,  89,  56, 255], [147,  92,  58, 255], [152,  95,  60, 255], [157,  98,  62, 255], [162, 101,  64, 255], [167, 104,  66, 255], [172, 108,  68, 255], [177, 111,  70, 255], [182, 114,  72, 255], [187, 117,  75, 255], [192, 120,  77, 255], [197, 123,  79, 255], [202, 126,  81, 255], [207, 130,  83, 255], [212, 133,  85, 255], [218, 136,  87, 255], [223, 139,  89, 255], [228, 142,  91, 255], [233, 145,  93, 255], [238, 149,  95, 255], [243, 152,  97, 255], [248, 155,  99, 255], [253, 158, 101, 255], [255, 161, 103, 255], [255, 164, 105, 255], [255, 168, 107, 255], [255, 171, 109, 255], [255, 174, 111, 255], [255, 177, 113, 255], [255, 180, 115, 255], [255, 183, 117, 255], [255, 187, 119, 255], [255, 190, 121, 255], [255, 193, 123, 255], [255, 196, 125, 255], [255, 199, 127, 255]], dtype=np.ubyte),
        'gray'  : np.array([[  0,   0,   0, 255], [  4,   4,   4, 255], [  8,   8,   8, 255], [ 12,  12,  12, 255], [ 16,  16,  16, 255], [ 20,  20,  20, 255], [ 24,  24,  24, 255], [ 28,  28,  28, 255], [ 32,  32,  32, 255], [ 36,  36,  36, 255], [ 40,  40,  40, 255], [ 45,  45,  45, 255], [ 49,  49,  49, 255], [ 53,  53,  53, 255], [ 57,  57,  57, 255], [ 61,  61,  61, 255], [ 65,  65,  65, 255], [ 69,  69,  69, 255], [ 73,  73,  73, 255], [ 77,  77,  77, 255], [ 81,  81,  81, 255], [ 85,  85,  85, 255], [ 89,  89,  89, 255], [ 93,  93,  93, 255], [ 97,  97,  97, 255], [101, 101, 101, 255], [105, 105, 105, 255], [109, 109, 109, 255], [113, 113, 113, 255], [117, 117, 117, 255], [121, 121, 121, 255], [125, 125, 125, 255], [130, 130, 130, 255], [134, 134, 134, 255], [138, 138, 138, 255], [142, 142, 142, 255], [146, 146, 146, 255], [150, 150, 150, 255], [154, 154, 154, 255], [158, 158, 158, 255], [162, 162, 162, 255], [166, 166, 166, 255], [170, 170, 170, 255], [174, 174, 174, 255], [178, 178, 178, 255], [182, 182, 182, 255], [186, 186, 186, 255], [190, 190, 190, 255], [194, 194, 194, 255], [198, 198, 198, 255], [202, 202, 202, 255], [206, 206, 206, 255], [210, 210, 210, 255], [215, 215, 215, 255], [219, 219, 219, 255], [223, 223, 223, 255], [227, 227, 227, 255], [231, 231, 231, 255], [235, 235, 235, 255], [239, 239, 239, 255], [243, 243, 243, 255], [247, 247, 247, 255], [251, 251, 251, 255], [255, 255, 255, 255]], dtype=np.ubyte),
        'hot'  : np.array([[ 11,   0,   0, 255], [ 21,   0,   0, 255], [ 32,   0,   0, 255], [ 43,   0,   0, 255], [ 53,   0,   0, 255], [ 64,   0,   0, 255], [ 74,   0,   0, 255], [ 85,   0,   0, 255], [ 96,   0,   0, 255], [106,   0,   0, 255], [117,   0,   0, 255], [128,   0,   0, 255], [138,   0,   0, 255], [149,   0,   0, 255], [159,   0,   0, 255], [170,   0,   0, 255], [181,   0,   0, 255], [191,   0,   0, 255], [202,   0,   0, 255], [213,   0,   0, 255], [223,   0,   0, 255], [234,   0,   0, 255], [244,   0,   0, 255], [255,   0,   0, 255], [255,  11,   0, 255], [255,  21,   0, 255], [255,  32,   0, 255], [255,  43,   0, 255], [255,  53,   0, 255], [255,  64,   0, 255], [255,  74,   0, 255], [255,  85,   0, 255], [255,  96,   0, 255], [255, 106,   0, 255], [255, 117,   0, 255], [255, 128,   0, 255], [255, 138,   0, 255], [255, 149,   0, 255], [255, 159,   0, 255], [255, 170,   0, 255], [255, 181,   0, 255], [255, 191,   0, 255], [255, 202,   0, 255], [255, 213,   0, 255], [255, 223,   0, 255], [255, 234,   0, 255], [255, 244,   0, 255], [255, 255,   0, 255], [255, 255,  16, 255], [255, 255,  32, 255], [255, 255,  48, 255], [255, 255,  64, 255], [255, 255,  80, 255], [255, 255,  96, 255], [255, 255, 112, 255], [255, 255, 128, 255], [255, 255, 143, 255], [255, 255, 159, 255], [255, 255, 175, 255], [255, 255, 191, 255], [255, 255, 207, 255], [255, 255, 223, 255], [255, 255, 239, 255], [255, 255, 255, 255]], dtype=np.ubyte),
        'hsv'  : np.array([[255,   0,   0, 255], [255,  24,   0, 255], [255,  48,   0, 255], [255,  72,   0, 255], [255,  96,   0, 255], [255, 120,   0, 255], [255, 143,   0, 255], [255, 167,   0, 255], [255, 191,   0, 255], [255, 215,   0, 255], [255, 239,   0, 255], [247, 255,   0, 255], [223, 255,   0, 255], [199, 255,   0, 255], [175, 255,   0, 255], [151, 255,   0, 255], [128, 255,   0, 255], [104, 255,   0, 255], [ 80, 255,   0, 255], [ 56, 255,   0, 255], [ 32, 255,   0, 255], [  8, 255,   0, 255], [  0, 255,  16, 255], [  0, 255,  40, 255], [  0, 255,  64, 255], [  0, 255,  88, 255], [  0, 255, 112, 255], [  0, 255, 135, 255], [  0, 255, 159, 255], [  0, 255, 183, 255], [  0, 255, 207, 255], [  0, 255, 231, 255], [  0, 255, 255, 255], [  0, 231, 255, 255], [  0, 207, 255, 255], [  0, 183, 255, 255], [  0, 159, 255, 255], [  0, 135, 255, 255], [  0, 112, 255, 255], [  0,  88, 255, 255], [  0,  64, 255, 255], [  0,  40, 255, 255], [  0,  16, 255, 255], [  8,   0, 255, 255], [ 32,   0, 255, 255], [ 56,   0, 255, 255], [ 80,   0, 255, 255], [104,   0, 255, 255], [128,   0, 255, 255], [151,   0, 255, 255], [175,   0, 255, 255], [199,   0, 255, 255], [223,   0, 255, 255], [247,   0, 255, 255], [255,   0, 239, 255], [255,   0, 215, 255], [255,   0, 191, 255], [255,   0, 167, 255], [255,   0, 143, 255], [255,   0, 120, 255], [255,   0,  96, 255], [255,   0,  72, 255], [255,   0,  48, 255], [255,   0,  24, 255]], dtype=np.ubyte),
        'parula'  : np.array([[ 53,  42, 135, 255], [ 54,  48, 147, 255], [ 54,  55, 160, 255], [ 53,  61, 173, 255], [ 50,  67, 186, 255], [ 44,  74, 199, 255], [ 32,  83, 212, 255], [ 15,  92, 221, 255], [  3,  99, 225, 255], [  2, 104, 225, 255], [  4, 109, 224, 255], [  8, 113, 222, 255], [ 13, 117, 220, 255], [ 16, 121, 218, 255], [ 18, 125, 216, 255], [ 20, 129, 214, 255], [ 20, 133, 212, 255], [ 19, 137, 211, 255], [ 16, 142, 210, 255], [ 12, 147, 210, 255], [  9, 152, 209, 255], [  7, 156, 207, 255], [  6, 160, 205, 255], [  6, 164, 202, 255], [  6, 167, 198, 255], [  7, 169, 194, 255], [ 10, 172, 190, 255], [ 15, 174, 185, 255], [ 21, 177, 180, 255], [ 29, 179, 175, 255], [ 37, 181, 169, 255], [ 46, 183, 164, 255], [ 56, 185, 158, 255], [ 66, 187, 152, 255], [ 77, 188, 146, 255], [ 89, 189, 140, 255], [101, 190, 134, 255], [113, 191, 128, 255], [124, 191, 123, 255], [135, 191, 119, 255], [146, 191, 115, 255], [156, 191, 111, 255], [165, 190, 107, 255], [174, 190, 103, 255], [183, 189, 100, 255], [192, 188,  96, 255], [200, 188,  93, 255], [209, 187,  89, 255], [217, 186,  86, 255], [225, 185,  82, 255], [233, 185,  78, 255], [241, 185,  74, 255], [248, 187,  68, 255], [253, 190,  61, 255], [255, 195,  55, 255], [254, 200,  50, 255], [252, 206,  46, 255], [250, 211,  42, 255], [247, 216,  38, 255], [245, 222,  33, 255], [245, 228,  29, 255], [245, 235,  24, 255], [246, 243,  19, 255], [249, 251,  14, 255]], dtype=np.ubyte),
        'pink'  : np.array([[ 30,   0,   0, 255], [ 50,  26,  26, 255], [ 64,  37,  37, 255], [ 75,  45,  45, 255], [ 85,  52,  52, 255], [ 94,  59,  59, 255], [102,  64,  64, 255], [110,  69,  69, 255], [117,  74,  74, 255], [123,  79,  79, 255], [130,  83,  83, 255], [136,  87,  87, 255], [141,  91,  91, 255], [147,  95,  95, 255], [152,  98,  98, 255], [157, 102, 102, 255], [162, 105, 105, 255], [167, 108, 108, 255], [172, 111, 111, 255], [176, 114, 114, 255], [181, 117, 117, 255], [185, 120, 120, 255], [189, 123, 123, 255], [194, 126, 126, 255], [195, 132, 129, 255], [197, 138, 131, 255], [199, 144, 134, 255], [201, 149, 136, 255], [202, 154, 139, 255], [204, 159, 141, 255], [206, 164, 144, 255], [207, 169, 146, 255], [209, 174, 148, 255], [211, 178, 151, 255], [212, 183, 153, 255], [214, 187, 155, 255], [216, 191, 157, 255], [217, 195, 160, 255], [219, 199, 162, 255], [220, 203, 164, 255], [222, 207, 166, 255], [223, 211, 168, 255], [225, 215, 170, 255], [226, 218, 172, 255], [228, 222, 174, 255], [229, 225, 176, 255], [231, 229, 178, 255], [232, 232, 180, 255], [234, 234, 185, 255], [235, 235, 191, 255], [237, 237, 196, 255], [238, 238, 201, 255], [240, 240, 206, 255], [241, 241, 211, 255], [243, 243, 216, 255], [244, 244, 221, 255], [245, 245, 225, 255], [247, 247, 230, 255], [248, 248, 234, 255], [250, 250, 238, 255], [251, 251, 243, 255], [252, 252, 247, 255], [254, 254, 251, 255], [255, 255, 255, 255]], dtype=np.ubyte),
        'spring'  : np.array([[255,   0, 255, 255], [255,   4, 251, 255], [255,   8, 247, 255], [255,  12, 243, 255], [255,  16, 239, 255], [255,  20, 235, 255], [255,  24, 231, 255], [255,  28, 227, 255], [255,  32, 223, 255], [255,  36, 219, 255], [255,  40, 215, 255], [255,  45, 210, 255], [255,  49, 206, 255], [255,  53, 202, 255], [255,  57, 198, 255], [255,  61, 194, 255], [255,  65, 190, 255], [255,  69, 186, 255], [255,  73, 182, 255], [255,  77, 178, 255], [255,  81, 174, 255], [255,  85, 170, 255], [255,  89, 166, 255], [255,  93, 162, 255], [255,  97, 158, 255], [255, 101, 154, 255], [255, 105, 150, 255], [255, 109, 146, 255], [255, 113, 142, 255], [255, 117, 138, 255], [255, 121, 134, 255], [255, 125, 130, 255], [255, 130, 125, 255], [255, 134, 121, 255], [255, 138, 117, 255], [255, 142, 113, 255], [255, 146, 109, 255], [255, 150, 105, 255], [255, 154, 101, 255], [255, 158,  97, 255], [255, 162,  93, 255], [255, 166,  89, 255], [255, 170,  85, 255], [255, 174,  81, 255], [255, 178,  77, 255], [255, 182,  73, 255], [255, 186,  69, 255], [255, 190,  65, 255], [255, 194,  61, 255], [255, 198,  57, 255], [255, 202,  53, 255], [255, 206,  49, 255], [255, 210,  45, 255], [255, 215,  40, 255], [255, 219,  36, 255], [255, 223,  32, 255], [255, 227,  28, 255], [255, 231,  24, 255], [255, 235,  20, 255], [255, 239,  16, 255], [255, 243,  12, 255], [255, 247,   8, 255], [255, 251,   4, 255], [255, 255,   0, 255]], dtype=np.ubyte),
        'summer'  : np.array([[  0, 128, 102, 255], [  4, 130, 102, 255], [  8, 132, 102, 255], [ 12, 134, 102, 255], [ 16, 136, 102, 255], [ 20, 138, 102, 255], [ 24, 140, 102, 255], [ 28, 142, 102, 255], [ 32, 144, 102, 255], [ 36, 146, 102, 255], [ 40, 148, 102, 255], [ 45, 150, 102, 255], [ 49, 152, 102, 255], [ 53, 154, 102, 255], [ 57, 156, 102, 255], [ 61, 158, 102, 255], [ 65, 160, 102, 255], [ 69, 162, 102, 255], [ 73, 164, 102, 255], [ 77, 166, 102, 255], [ 81, 168, 102, 255], [ 85, 170, 102, 255], [ 89, 172, 102, 255], [ 93, 174, 102, 255], [ 97, 176, 102, 255], [101, 178, 102, 255], [105, 180, 102, 255], [109, 182, 102, 255], [113, 184, 102, 255], [117, 186, 102, 255], [121, 188, 102, 255], [125, 190, 102, 255], [130, 192, 102, 255], [134, 194, 102, 255], [138, 196, 102, 255], [142, 198, 102, 255], [146, 200, 102, 255], [150, 202, 102, 255], [154, 204, 102, 255], [158, 206, 102, 255], [162, 208, 102, 255], [166, 210, 102, 255], [170, 212, 102, 255], [174, 215, 102, 255], [178, 217, 102, 255], [182, 219, 102, 255], [186, 221, 102, 255], [190, 223, 102, 255], [194, 225, 102, 255], [198, 227, 102, 255], [202, 229, 102, 255], [206, 231, 102, 255], [210, 233, 102, 255], [215, 235, 102, 255], [219, 237, 102, 255], [223, 239, 102, 255], [227, 241, 102, 255], [231, 243, 102, 255], [235, 245, 102, 255], [239, 247, 102, 255], [243, 249, 102, 255], [247, 251, 102, 255], [251, 253, 102, 255], [255, 255, 102, 255]], dtype=np.ubyte),
        'winter'  : np.array([[  0,   0, 255, 255], [  0,   4, 253, 255], [  0,   8, 251, 255], [  0,  12, 249, 255], [  0,  16, 247, 255], [  0,  20, 245, 255], [  0,  24, 243, 255], [  0,  28, 241, 255], [  0,  32, 239, 255], [  0,  36, 237, 255], [  0,  40, 235, 255], [  0,  45, 233, 255], [  0,  49, 231, 255], [  0,  53, 229, 255], [  0,  57, 227, 255], [  0,  61, 225, 255], [  0,  65, 223, 255], [  0,  69, 221, 255], [  0,  73, 219, 255], [  0,  77, 217, 255], [  0,  81, 215, 255], [  0,  85, 213, 255], [  0,  89, 210, 255], [  0,  93, 208, 255], [  0,  97, 206, 255], [  0, 101, 204, 255], [  0, 105, 202, 255], [  0, 109, 200, 255], [  0, 113, 198, 255], [  0, 117, 196, 255], [  0, 121, 194, 255], [  0, 125, 192, 255], [  0, 130, 190, 255], [  0, 134, 188, 255], [  0, 138, 186, 255], [  0, 142, 184, 255], [  0, 146, 182, 255], [  0, 150, 180, 255], [  0, 154, 178, 255], [  0, 158, 176, 255], [  0, 162, 174, 255], [  0, 166, 172, 255], [  0, 170, 170, 255], [  0, 174, 168, 255], [  0, 178, 166, 255], [  0, 182, 164, 255], [  0, 186, 162, 255], [  0, 190, 160, 255], [  0, 194, 158, 255], [  0, 198, 156, 255], [  0, 202, 154, 255], [  0, 206, 152, 255], [  0, 210, 150, 255], [  0, 215, 148, 255], [  0, 219, 146, 255], [  0, 223, 144, 255], [  0, 227, 142, 255], [  0, 231, 140, 255], [  0, 235, 138, 255], [  0, 239, 136, 255], [  0, 243, 134, 255], [  0, 247, 132, 255], [  0, 251, 130, 255], [  0, 255, 128, 255]], dtype=np.ubyte),
    }
    # < To this line >
    keys=['jet','autumn','bone','colorcube','cool','copper','gray','hot','hsv','parula','pink','spring','summer','winter']
    idx = idx % len(keys)
    colormap = colormaps[keys[idx]]
    pos = pos_min + (pos_max - pos_min) * np.arange(len(colormap))/(len(colormap)-1)

    global GlobalColormap
    if not GlobalColormap == keys[idx]:
        print('Active colormap: ' + keys[idx])
        GlobalColormap=keys[idx]

    return pg.ColorMap(pos, colormap)

def plot_Data2D(data, plt, log=False, legend=True, icolormap=0, verbose=False, legend_fontsize=10):
    ''' create a layout and populate a plotItem with data Data2D, adding a color bar '''
    # data
    img = pg.ImageItem()
    dataset = np.array(data.zvals)
    dataset = np.transpose(dataset)
    datashape = dataset.shape
    
    ymin = 1e-19
    if log:
        dataset = np.reshape(dataset, (1, datashape[0]*datashape[1]))
        idx = dataset[dataset>0]
        if len(idx) > 0:
            ymin = np.min(idx)/10
            dataset[dataset<=0] = ymin
            dataset = np.reshape(dataset, datashape)
            dataset = np.log10(dataset)
        else:
            dataset = np.reshape(dataset, datashape)
    img.setImage(dataset)
    
    # scale(x,y) is in %, translate(x,y) is in the original units
    dx = (data.xlimits[1] - data.xlimits[0])/datashape[0]
    dy = (data.xlimits[3] - data.xlimits[2])/datashape[1]
    img.scale(dx,dy)
    # Calculate translation in original pixel units
    img.translate(data.xlimits[0]/dx,data.xlimits[2]/dy)
    
    # color map (by lookup table)
    pos_min = np.min(dataset)
    pos_max = np.max(dataset)
    
    colormap = get_color_map(icolormap, pos_min, pos_max)
    lut = colormap.getLookupTable(pos_min, pos_max, 256)
    img.setLookupTable(lut)

    # graphics layout with a plotitem and a gradienteditoritem
    layout = pg.GraphicsLayout()
    layout.setContentsMargins(0, 0, 20, 5)
    
    # plot area
    layout.addLabel(' ', 0, 0, colspan=2)
    layout.addItem(plt, 1, 0)
    plt.setLabels(bottom=data.xlabel, left=data.ylabel)
    plt.setMenuEnabled(False)
    
    if legend:
        plt.legend = ModLegend(offset=(-1, 1), text_size='%spt' % str(legend_fontsize))
        plt.legend.setParentItem(plt.vb)
        
        try:
            lname1 = '<center>%s<br>I = %s</center>' % (data.component, data.values[0])
            if verbose:
                lname1 = '%s [%s]<br><br>%s<br><br>I = %s Err = %s N = %s; %s' % (data.component, data.filename, data.title, data.values[0], data.values[1], data.values[2], data.statistics)
        except:
            lname1 = '%s<br>[%s]' % (data.component, data.filename)
        if lname1:
            plt.plot([0], [0], name=lname1)
    
    plt.addItem(img)
    # Set the x and y ranges correctly
    plt.getViewBox().setXRange(data.xlimits[0], data.xlimits[1], padding=0)
    plt.getViewBox().setYRange(data.xlimits[2], data.xlimits[3], padding=0)
    
    # color bar
    cbimg = pg.ImageItem()
    numsteps = 100
    arr_1 = pos_min + (pos_max - pos_min) * np.arange(numsteps)/(numsteps)
    cbimg.setImage(np.array([arr_1]))
    # calculate scaling and translation for the y-axis
    dy = (pos_max - pos_min) / numsteps
    # Prevent division by 0
    if (dy==0):
        dy=1;
    ty = (pos_min) / dy
    cbimg.scale(1, dy)
    cbimg.translate(0,ty)
    
    cbimg.setLookupTable(lut)
    
    colorbar = layout.addPlot(1, 1)
    colorbar.addItem(cbimg)
    colorbar.setFixedWidth(40)
    
    pg.GradientEditorItem
    
    colorbar.axes['top']['item'].show()
    colorbar.axes['top']['item'].setStyle(showValues=False)
    colorbar.axes['bottom']['item'].show()
    colorbar.axes['bottom']['item'].setStyle(showValues=False)
    colorbar.axes['left']['item'].show()
    colorbar.axes['left']['item'].setStyle(showValues=False)
    colorbar.axes['right']['item'].show()
    
    colorbar.getViewBox().autoRange(padding=0)
    
    plt.layout_2d = layout
    
    # return layout so it doesn't get garbage collected, but the proper plot viewBox pointer for click events
    return plt.getViewBox(), layout

