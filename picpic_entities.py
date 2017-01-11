
COLOR = "color"
STRING = "string"

class PicPicShapeCore(object):
    def __init__(self):
        super(PicPicShapeCore, self).__init__()
        self.name = Property()
        self.name.type = STRING
        self.color = Property()
        self.color.type = COLOR
        self.pen_color = Property()
        self.pen_color.type = COLOR
        self.over_color = Property()
        self.over_color.type = COLOR
        self.click_color = None
        self.vertex = []
        self.action = None
        self.selected = None
        self.pen_width = None

class PicPicFreeCore(PicPicShapeCore):
    def __init__(self):
        super(PicPicFreeCore, self).__init__()
        self.start_point = None
        self.drawing = None
        self.path = None

class Property(object):
    def __init__(self):
        self.valid_type = ["color", "string", "bool", "int", "float"]
        self._x = None
        self._type = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def gettype(self):
        return self._type

    def settype(self, type):
        if not type in self.valid_type:
            raise TypeError("Type must be color, string, bool, int, float")
        self._type = type

    value = property(getx, setx)
    type = property(gettype, settype)
