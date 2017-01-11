

class PicPicShapeCore(object):
    def __init__(self):
        super(PicPicShapeCore, self).__init__()
        self.name = None
        self.color = Property()
        self.pen_color = None
        self.over_color = None
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
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        print "prop setted"
        self.value = value

    def set(self, value):
        print "prop setted"
        self.value = value