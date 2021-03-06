from PyQt4 import QtCore, QtGui
from gui_timebar import TimeBar
import variables

class TimeBarPair(QtGui.QGraphicsLineItem):
    # Defined here until PyQt includes it.
    ItemHasNoContents = 0x400

    def __init__(self, timeAxis, parent):
        """
        Parameter text is displayed as a label between the time bars.
        Parameter timeAxis points to Time Axis on which the time bars
        are placed.
        Parameter leftBorder contains the width of free space between
        the left side of the scene and Time Axis, in pixels.
        Parameter parent is a parent object in scene where time bars
        will be displayed.
        """
        # QGraphicsLineItem(QGraphicsItem parent=None,
        #                   QGraphicsScene scene=None)
        super(TimeBarPair, self).__init__(None, parent)
        self.timeAxis = timeAxis
        self.height = 0
        # Should this really be set? If bars stop to draw, delete this.
        self.setFlag(self.ItemHasNoContents, True)
        self.bar1 = TimeBar(timeAxis)
        self.bar2 = TimeBar(timeAxis)
        self.setBarPos(100, 200)
        self.bar1.setParentItem(self)
        self.bar2.setParentItem(self)
        self.bar1.signals.positionChanged.connect(self.onPositionChanged)
        self.bar2.signals.positionChanged.connect(self.onPositionChanged)

        self.legendLine = QtGui.QGraphicsLineItem()
        self.legendLine.setPen(QtGui.QPen(QtCore.Qt.DotLine))
        self.legendLine.setParentItem(self)
        self.legendText = QtGui.QGraphicsSimpleTextItem()
        self.legendTextVisible = True
        self.legendText.setParentItem(self)
        self.updateAppearance()

    def setHeight(self, height):
        if self.height == height:
            return
        self.height = height
        self.bar1.setHeight(height)
        self.bar2.setHeight(height)

    def setBarPos(self, bar1, bar2):
        self.bar1.setPos(bar1, 0)
        self.bar2.setPos(bar2, 0)

    def setColor(self, color):
        self.bar1.setColor(color)
        self.bar2.setColor(color)
        # Color legend line
        p = self.legendLine.pen()
        p.setColor(color)
        self.legendLine.setPen(p)
        # Color legend text
        b = self.legendText.brush()
        b.setColor(color)
        self.legendText.setBrush(b)

    def onPositionChanged(self):
        self.updateLegend()

    def updateLegend(self):
        line = QtCore.QLineF(self.bar1.pos().x(), 40,
                             self.bar2.pos().x(), 40)
        self.legendLine.setLine(line)
        textX = abs(line.dx()) / 2 + min(line.x1(), line.x2())
        textX -= self.legendText.boundingRect().width() / 2
        self.legendText.setPos(textX, 12)
        self.legendText.setVisible(self.legendTextVisible and
                                   abs(line.dx()) > self.legendText.boundingRect().width() + 5)

    def updatePositionFromData(self, time1, time2):
        """
        Parameters are time values in seconds.
        """
        self.bar1.setPos(self.timeAxis.mapTimeToPixels(time1), 0)
        self.bar2.setPos(self.timeAxis.mapTimeToPixels(time2), 0)

    def updateAppearance(self):
        raise NotImplemented

    def setEnabled(self, enabled):
        self.bar1.setEnabled(enabled)
        self.bar2.setEnabled(enabled)

class FullLightBarPair(TimeBarPair):
    def __init__(self, timeAxis, parent):
        TimeBarPair.__init__(self, timeAxis, parent)

    def updateAppearance(self):
        self.legendText.setFont(variables.fullLightBarsFont.value())
        self.legendTextVisible = variables.fullLightBarsCaptionEnabled.value()
        self.legendText.setText(variables.fullLightBarsCaption.value())
        self.updateLegend()
        self.setVisible(variables.fullLightBarsVisible.value())

class FitBarPair(TimeBarPair):
    def __init__(self, timeAxis, parent):
        TimeBarPair.__init__(self, timeAxis, parent)

    def updateAppearance(self):
        self.legendText.setFont(variables.fitBarsFont.value())
        self.legendTextVisible = variables.fitBarsCaptionEnabled.value()
        self.legendText.setText(variables.fitBarsCaption.value())
        self.updateLegend()
        self.setVisible(variables.fitBarsVisible.value())
