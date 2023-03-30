from utils.curve_analysis.curve import Curve
from utils.imports import *
from utils.curve_analysis.figure import Figure


class CurveAnalyser:
    FIGURE_HEIGHT = 6
    FIGURE_WIDTH = 12

    def __init__(self, curves_to_analyse: dict):
        self.curves_to_analyse = curves_to_analyse
        self.figures_to_draw = None
        self.axes = None
        self.prepare_figures()
        self.draw()

    def prepare_figures(self):
        self.figures_to_draw: list[Figure] = []
        fig, self.axes = plt.subplots(
            nrows=len(self.curves_to_analyse),
            ncols=1,
            sharex=True,
            figsize=(
                self.FIGURE_WIDTH,
                len(self.curves_to_analyse) * self.FIGURE_HEIGHT,
            ),
        )
        for i, (title, functions) in enumerate(self.curves_to_analyse.items()):
            for params in functions:
                self.axes[i].set_title(title)
                self.axes[i].grid()

                curve: Curve = Curve.get_curve_by_formula(ax=self.axes[i], **params)
                self.figures_to_draw.append(curve)
                self.figures_to_draw.extend(curve.curve_analysis())

    def draw(self):
        for figure in self.figures_to_draw:
            figure.draw()

        plt.tight_layout(h_pad=5, w_pad=2)

        for ax in self.axes:
            ax.legend(ncol=3)

        plt.show()
