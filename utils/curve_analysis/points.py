from utils.curve_analysis.figure import Figure


class Points(Figure):
    def draw(self):
        self.ax.scatter(
            x=self.x,
            y=self.y,
            label=self.label,
            **self.PARAMS.get(self.obj_type, dict())
        )
