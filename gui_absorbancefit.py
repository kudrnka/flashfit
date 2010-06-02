from PyQt4 import QtCore, QtGui

class AbsorbanceFit(QtGui.QGraphicsItemGroup):
    def __init__(self, data, parent=None):
        super(AbsorbanceFit, self).__init__(parent)
        self.data = data
        self.pen = QtGui.QPen()
        self.pen.setWidth(3)
        self.pen.setColor(QtGui.QColor("#882222"))
        self.child = QtGui.QGraphicsItemGroup()
        self.child.setParentItem(self)

    def setSize(self, width, height):
        self.width = width
        self.height = height

    def recreateFromData(self):
        # Remove all subitems.
        self.removeFromGroup(self.child)
        self.scene().removeItem(self.child)
        self.child = QtGui.QGraphicsItemGroup()
        self.child.setParentItem(self)

        # Do nothing if no data are loaded.
        if self.data.timeSpan == None:
            return
        if len(self.data.fitdata.values) == 0:
            return

        timeModifier = self.width / float(self.data.timeSpan)
        absorbanceModifier = self.height / float(self.data.absorbanceSpan)
        lastTime = None
        lastAbsorbance = None
        for t in range(0, self.data.fitAbsorbanceTimePointer[1] - self.data.fitAbsorbanceTimePointer[0] + 1):
            time = (self.data.time[self.data.fitAbsorbanceTimePointer[0] + t] - self.data.minTime) * timeModifier
            fit = self.height - (self.data.fitdata.values[t] - self.data.minAbsorbance) * absorbanceModifier
            if lastTime != None and lastFit != None:
                line = QtGui.QGraphicsLineItem(QtCore.QLineF(lastTime, lastFit, time, fit))
                line.setPen(self.pen)
                line.setParentItem(self.child)
            lastTime = time
            lastFit = fit

    def resizeFromData(self):
        # Do nothing if no data are loaded.
        if self.data.timeSpan == None:
            return
        if len(self.data.absorbanceFit) == 0:
            return

        timeModifier = self.width / float(self.data.timeSpan)
        absorbanceModifier = self.height / float(self.data.absorbanceSpan)
        lastTime = None
        lastAbsorbance = None
        children = self.child.children()
        for t in range(0, self.data.fitAbsorbanceTimePointer[1] - self.data.fitAbsorbanceTimePointer[0] + 1):
            time = (self.data.time[self.data.fitAbsorbanceTimePointer[0] + t] - self.data.minTime) * timeModifier
            fit = self.height - (self.data.absorbanceFit[t] - self.data.minAbsorbance) * absorbanceModifier
            if lastTime != None and lastFit != None:
                line = QtCore.QLineF(lastTime, lastFit, time, fit)
                children[t - 1].setLine(line)
            lastTime = time
            lastFit = fit