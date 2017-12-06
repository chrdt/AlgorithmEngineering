from pygal import Line, Box
from time import gmtime, strftime


class PlotLine(object):
    def __init__(self):
        self.graph = Line()
        self.graph.title = 'Standardabweichung und Mittelwert'
        self.graph.x_title = 'Zeilen n [* 1.000.000]'
        self.graph.y_title = 'Laufzeit in s'
        self.graph.x_labels = map(str, range(2, 11, 2))

    def add_line(self, name, data):
        self.graph.add(name, data)

    def finish(self):
        time = strftime("%d_%d-%H_%M", gmtime())
        self.graph.render_to_file("average-deviation/{}.svg".format(time))


class PlotBox(object):
    def __init__(self):
        self.graph = Box(height=1000)
        self.graph.title = 'Darstellung von Ausreissern'
        self.graph.x_title = 'Zeilen n [* 1.000.000]'
        self.graph.y_title = 'Laufzeit in s'
        self.graph.x_labels = map(str, range(2, 11, 2))

    def add_line(self, name, data):
        self.graph.add(name, data)

    def finish(self):
        time = strftime("%d_%d-%H_%M", gmtime())
        self.graph.render_to_file("extremes/{}.svg".format(time))
