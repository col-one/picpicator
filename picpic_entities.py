

class PicPicShape(object):
    def __init__(self):
        super(PicPicShape, self).__init__()
        self.name = None
        self.color = None
        self.pen_color = None
        self.over_color = None
        self.click_color = None
        self.vertex = None
        self.action = None
        self.selected = None

class PicPicFree(PicPicShape):
    def __init__(self):
        super(PicPicFree, self).__init__()
        self.start_point = None
        self.drawing = None
        self.path = None
