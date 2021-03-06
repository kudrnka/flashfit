from PyQt4 import QtCore, QtGui
from font import Font
import numbers
import gui_textitems

class Variable:
    """
    A named variable (key-value pair) accessible from whole
    application. Its value can be stored in user's settings and
    preserved between application runs.
    """
    def __init__(self, key, defaultValue):
        self._key = key
        self._defaultValue = defaultValue
        self.type = "normal"
        if isinstance(defaultValue, Font):
            self.type = "font"
        elif defaultValue == True or defaultValue == False:
            self.type = "bool"
        elif isinstance(defaultValue, numbers.Integral):
            self.type = "int"

    def key(self):
        return self._key;

    def value(self, default=False):
        if default:
            return self._defaultValue

        settings = QtCore.QSettings()

        defaultValue = self._defaultValue
        if self.type == "font":
            defaultValue = self._defaultValue.toStorableString()

        value = settings.value(self._key, defaultValue)
        if self.type == "font":
            f = Font()
            f.fromStorableString(value.toString())
            return f
        elif self.type == "bool":
            return value.toBool()
        elif self.type == "int":
            return value.toInt()[0]

        return value.toPyObject()

    def setValue(self, value):
        settings = QtCore.QSettings()
        if self.type == "font":
            value = value.toStorableString()
        settings.setValue(self._key, QtCore.QVariant(value))

valueAxisValuesFont = Variable("valueAxisValuesFont", Font())
valueAxisCaptionFont = Variable("valueAxisCaptionFont", Font(pointSize = 30))
valueAxisCaptionEnabled = Variable("valueAxisCaptionEnabled", True)
absorbanceAxisCaption = Variable("absorbanceAxisCaption", "A")
luminiscenceAxisCaption = Variable("luminiscenceAxisCaption", "I_r")
timeAxisValuesFont = Variable("timeAxisValuesFont", Font())
timeAxisCaptionFont = Variable("timeAxisCaptionFont", Font(pointSize = 30))
timeAxisCaptionEnabled = Variable("timeAxisCaptionEnabled", True)
timeAxisCaption = Variable("timeAxisCaption", "time")

fullLightBarsVisible = Variable("fullLightBarsVisible", True)
fullLightBarsFont = Variable("fullLightBarsFont", Font(pointSize = 18))
fullLightBarsCaptionEnabled = Variable("fullLightBarsCaptionEnabled", True)
fullLightBarsCaption = Variable("fullLightBarsCaption", "Full light")

fitBarsVisible = Variable("fitBarsVisible", True)
fitBarsFont = Variable("fitBarsFont", Font(pointSize = 18))
fitBarsCaptionEnabled = Variable("fitBarsCaptionEnabled", True)
fitBarsCaption = Variable("fitBarsCaption", "Fit area")

legendFont = Variable("legendFont", Font(pointSize = 26))
legendDisplayedPrecision = Variable("legendDisplayedPrecision", 6)
legendTable = Variable("legendTable",
                       [ gui_textitems.Name.__name__,
                         gui_textitems.MeasureDate.__name__,
                         gui_textitems.Model.__name__,
                         gui_textitems.A0.__name__,
                         gui_textitems.Ainf.__name__,
                         gui_textitems.Amax.__name__,
                         gui_textitems.RateConstants.__name__,
                         gui_textitems.A0minusAinf.__name__ ])
