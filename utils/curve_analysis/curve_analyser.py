from utils.curve_analysis.curve import Curve
from utils.curve_analysis.plot import Plot
from utils.curve_analysis.points import Points
from utils.imports import *


class CurveAnalyser:
    FIGURE_WIDTH = 12
    FIGURE_HEIGHT = 6

    def __init__(
        self,
        curves_to_draw: dict,
        analyse: bool = True,
        figure_width: int = FIGURE_WIDTH,
        figure_height: int = FIGURE_HEIGHT,
    ):
        self.curves_to_draw = curves_to_draw
        self.analyse = analyse
        self.figure_width = figure_width
        self.figure_height = figure_height
        self.figures_to_draw = None
        self.axes = None

        self.prepare_figures()
        self.draw()

    def prepare_figures(self):
        self.figures_to_draw: list[Plot] = []
        fig, self.axes = plt.subplots(
            nrows=len(self.curves_to_draw),
            ncols=1,
            sharex=True,
            figsize=(
                self.figure_width,
                len(self.curves_to_draw) * self.figure_height,
            ),
        )
        if type(self.axes) != np.ndarray:
            self.axes = [self.axes]
        for i, (title, functions) in enumerate(self.curves_to_draw.items()):
            self.axes[i].set_title(title)
            main_figure = None
            for params in functions:
                if isinstance(params['obj_type'], Points.Type):
                    main_figure = Points.by_formula(ax=self.axes[i], **params)
                elif isinstance(params['obj_type'], Curve.Type):
                    main_figure = Curve.by_formula(ax=self.axes[i], **params)
                self.figures_to_draw.append(main_figure)
                if self.analyse:
                    self.figures_to_draw.extend(main_figure.curve_analysis())

    def draw(self):
        for figure in self.figures_to_draw:
            figure.draw()

        plt.tight_layout(h_pad=5, w_pad=2)
        for ax in self.axes:
            handlers, labels = ax.get_legend_handles_labels()
            ax.legend(handles=set(handlers), labels=set(labels), ncol=len(handlers))
            ax.grid(visible=True, color="#757575", which="major", linestyle="-")
            ax.grid(visible=True, color="#BDBDBD", which="minor", linestyle="--")
            ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
            ax.xaxis.set_minor_locator(tck.AutoMinorLocator())

        plt.show()


if __name__ == "__main__":
    curves = {
        r"$\frac{1}{x}$": (
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$\frac{1}{x}$",
                x_min=-4,
                x_max=0,
                formula=lambda x: 1 / x,
            ),
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$\frac{1}{x}$",
                x_min=0,
                x_max=4,
                formula=lambda x: 1 / x,
            ),
            dict(
                obj_type=Points.Type.EMPTY,
                label=r"$circle$",
                x_min=1,
                x_max=1,
                formula=lambda x: x + 99,
            ),
        )
    }
    CurveAnalyser(curves, False, 6, 4)
