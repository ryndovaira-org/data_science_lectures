import numpy as np

from utils.curve_analysis.curve import Curve
from utils.imports import *
from utils.curve_analysis.figure import Figure


class CurveAnalyser:
    FIGURE_WIDTH = 12
    FIGURE_HEIGHT = 6

    def __init__(
        self,
        curves: dict,
        analyse: bool = True,
        figure_width: int = FIGURE_WIDTH,
        figure_height: int = FIGURE_HEIGHT,
    ):
        self.curves_to_analyse = curves
        self.analyse = analyse
        self.figure_width = figure_width
        self.figure_height = figure_height
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
                self.figure_width,
                len(self.curves_to_analyse) * self.figure_height,
            ),
        )
        if type(self.axes) != np.ndarray:
            self.axes = [self.axes]
        for i, (title, functions) in enumerate(self.curves_to_analyse.items()):
            for params in functions:
                self.axes[i].set_title(title)
                self.axes[i].grid()

                main_figure = Curve.get_curve_by_formula(ax=self.axes[i], **params)
                self.figures_to_draw.append(main_figure)
                if self.analyse:
                    self.figures_to_draw.extend(main_figure.curve_analysis())

    def draw(self):
        for figure in self.figures_to_draw:
            figure.draw()

        plt.tight_layout(h_pad=5, w_pad=2)

        for ax in self.axes:
            ax.legend(ncol=3)

        plt.show()
