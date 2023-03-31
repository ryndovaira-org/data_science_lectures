from utils.curve_analysis.figure import Figure


class Interval(Figure):
    @property
    def min_y(self):
        return min(self.y) - self.LIM_OFFSET

    @property
    def max_y(self):
        return max(self.y) + self.LIM_OFFSET

    def draw(self):
        self.ax.plot(self.x, self.y, **self.PARAMS.get(self.obj_type, dict()))
