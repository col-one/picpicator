
COLOR = "color"
STRING = "string"
FLOAT = "float"
LIST = "list"

class PicPicShapeCore(object):
    def __init__(self):
        super(PicPicShapeCore, self).__init__()
        self.name = Property("Shape")
        self.name.type = STRING
        self.name.expo_order = 0
        self.action = Property("")
        self.action.type = STRING
        self.action.expo_order = 0.1
        self.color = Property((122,11,11,255))
        self.color.type = COLOR
        self.color.expo_order = 1
        self.pen_color = Property((125,55,44))
        self.pen_color.type = COLOR
        self.pen_color.expo_order = 2
        self.over_color = Property((122,78,45,255))
        self.over_color.type = COLOR
        self.over_color.expo_order = 3
        self.opacity = Property(50.0)
        self.opacity.type = FLOAT
        self.click_color = Property((120,200,255))
        self.click_color.type = COLOR
        self.click_color.expo_order = 4
        self.vertex = Property()
        self.vertex.type = LIST
        self.vertex.expo = False
        self.selected = None
        self.pen_width = Property(0.1)
        self.pen_width.type = FLOAT
        self.pen_width.expo_order = 5
        self.scale = Property(1.0)
        self.scale.type = FLOAT
        self.rotate = Property(0.0)
        self.rotate.type = FLOAT

class PicPicFreeCore(PicPicShapeCore):
    def __init__(self):
        super(PicPicFreeCore, self).__init__()

class PicPicTextCore(PicPicShapeCore):
    def __init__(self):
        super(PicPicTextCore, self).__init__()
        self.size = Property(2)
        self.size.type = FLOAT
        self.size.expo_order = 0.25
        self.text = Property("Text")
        self.text.type = STRING
        self.text.expo_order = 0.2
        self.pen_color.expo = False

class PicPicButtonCore(PicPicShapeCore):
    def __init__(self):
        super(PicPicButtonCore, self).__init__()
        self.name.value = "Button"
        self.color = None
        self.pen_color = None
        self.click_color = None
        self.opacity = None
        self.over_color = None
        self.pen_width = None
        self.rotate = None
        self.scale = None

class Property(object):
    def __init__(self, *args):
        self.valid_type = ["color", "string", "bool", "int", "float", "list"]
        if len(args) == 1:
            self._x = args[0]
        else:
            self._x = list(args)
        self._type = None
        self.expo = True
        self.expo_order = 10

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

def generate_randcolor():
    import random
    return (random.randint(0,256), random.randint(0,256), random.randint(0,256), 255)

class PicTabDict(object):
    def __init__(self, name=Property("A Tab (dlck to rename)"), image=Property(""), shapes=None, view=None):
        super(PicTabDict, self).__init__()
        self.name = name
        self.name.type = STRING
        self.image = image
        self.image.type = STRING
        self.view = view
        if shapes == None:
            self.shapes = []
        else:
            self.shapes = shapes
        self.layer = None
        self.wrapper = None

class PicPicTabCore(list):
    def __init__(self):
        super(PicPicTabCore, self).__init__()

    def __setitem__(self, key, value):
        if not isinstance(value, PicTabDict):
            raise TypeError("Value must a PicTabDict")