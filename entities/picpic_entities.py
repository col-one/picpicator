
COLOR = "color"
STRING = "string"
FLOAT = "float"
LIST = "list"

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
        self.opacity = Property(0)
        self.opacity.type = FLOAT
        self.click_color = Property(255,255,255)
        self.click_color.type = COLOR
        self.vertex = Property()
        self.vertex.type = LIST
        self.action = None
        self.selected = None
        self.pen_width = Property()
        self.pen_width.type = FLOAT

class PicPicFreeCore(PicPicShapeCore):
    def __init__(self):
        super(PicPicFreeCore, self).__init__()
        self.start_point = None
        self.drawing = None
        self.path = None

class Property(object):
    def __init__(self, *args):
        self.valid_type = ["color", "string", "bool", "int", "float", "list"]
        if len(args) == 1:
            self._x = args[0]
        else:
            self._x = args
        self._type = None

    def getx(self):
        return self._x

    def setx(self, value):
        if self._type == LIST:
            self._x.append(value)
        else:
            self._x = value

    def gettype(self):
        return self._type

    def settype(self, type):
        if not type in self.valid_type:
            raise TypeError("Type must be color, string, bool, int, float")
        self._type = type

    value = property(getx, setx)
    type = property(gettype, settype)
