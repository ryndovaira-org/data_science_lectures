from typing import Callable

from utils.curve_analysis.points import Points
from utils.imports import *
from utils.curve_analysis.figure import Figure
from utils.curve_analysis.interval import Interval


class Curve(Interval):
    LIN_SPACE_NUM = 1000

    def __init__(
        self,
        ax: axes.Axes,
        x: float | np.ndarray,
        y: float | np.ndarray,
        obj_type: Figure.Type,
        formula: Callable[[np.ndarray], np.ndarray] = None,
    ):
        super().__init__(ax, x, y, obj_type)
        self.formula = formula

    @classmethod
    def get_curve_by_formula(
        cls,
        ax: axes.Axes,
        obj_type: Figure.Type,
        x_min: float,
        x_max: float,
        formula: Callable[[np.ndarray], np.ndarray],
    ):
        x = np.linspace(x_min, x_max, cls.LIN_SPACE_NUM)
        y = formula(x)
        return Curve(ax=ax, x=x, y=y, obj_type=obj_type, formula=formula)

    def draw(self):
        super(Curve, self).draw()
        ax_y_min, ax_y_max = self.ax.get_ylim()

        if ax_y_min > self.min_y:
            self.ax.set_ylim(self.min_y, ax_y_max)

    @property
    def rounded_x(self):
        return np.around(self.x, self.AROUND_DECIMALS)

    @property
    def rounded_y(self):
        return np.around(self.y, self.AROUND_DECIMALS)

    def curve_analysis(self):
        figures = [
            self.get_d_y(),
            self.get_e_y(),
            self.get_xs_where_y_eq_0(),
            *self.get_x_where_y_below_above_0(),
            *self.get_curve_up_down(),
        ]
        return figures

    def get_max_min_point(self):
        ...

    def get_d_y(self):
        return Interval(
            ax=self.ax,
            x=self.x,
            y=np.full((len(self.x), 1), 0),
            obj_type=Figure.Type.COORDINATE_INTERVAL_X,
        )

    def get_e_y(self):
        return Interval(
            ax=self.ax,
            x=np.full((len(self.x), 1), 0),
            y=self.y,
            obj_type=Figure.Type.COORDINATE_INTERVAL_Y,
        )

    def get_xs_where_y_eq_0(self):
        sorted_xs = sorted([xi for xi in self.rounded_x[np.where(self.rounded_y == 0)]])
        diff = np.ediff1d(sorted_xs)
        threshold = 0.15
        if np.count_nonzero(diff < threshold):
            to_keep = np.where(diff >= threshold)
            if np.count_nonzero(to_keep) == 0:
                median = np.median(sorted_xs)
                return Points(
                    ax=self.ax,
                    x=np.asarray(median),
                    y=np.asarray(0),
                    obj_type=Figure.Type.POINT_Y0,
                )
        return Points(
            ax=self.ax,
            x=np.asarray(sorted_xs),
            y=np.full((1, len(sorted_xs)), 0),
            obj_type=Figure.Type.POINT_Y0,
        )

    def get_x_where_y_below_above_0(self):
        tmp_xy = {Figure.Type.INTERVAL_ABOVE_0: [], Figure.Type.INTERVAL_BELOW_0: []}
        intervals: list[Interval] = []

        def try_save_interval(interval_type: Figure.Type):
            if len(tmp_xy[interval_type]) > 0:
                intervals.append(
                    Interval(
                        ax=self.ax,
                        x=np.asarray(tmp_xy[interval_type]),
                        y=np.full((len(tmp_xy[interval_type]), 1), 0),
                        obj_type=interval_type,
                    )
                )
                tmp_xy[interval_type].clear()

        for x, y in zip(self.x, self.y):
            if y > 0:
                try_save_interval(Figure.Type.INTERVAL_BELOW_0)
                tmp_xy[Figure.Type.INTERVAL_ABOVE_0].append(x)
            elif y < 0:
                try_save_interval(Figure.Type.INTERVAL_ABOVE_0)
                tmp_xy[Figure.Type.INTERVAL_BELOW_0].append(x)

        try_save_interval(Figure.Type.INTERVAL_BELOW_0)
        try_save_interval(Figure.Type.INTERVAL_ABOVE_0)

        return intervals

    def get_curve_up_down(self):
        tmp_xy = {
            Figure.Type.INTERVAL_UP: {"x": [], "y": []},
            Figure.Type.INTERVAL_DOWN: {"x": [], "y": []},
        }

        intervals: list[Interval] = []

        def try_save_interval(interval_type: Figure.Type):
            if len(tmp_xy[interval_type]["x"]) > 0:
                intervals.append(
                    Interval(
                        ax=self.ax,
                        x=np.asarray(tmp_xy[interval_type]["x"]),
                        y=np.asarray(tmp_xy[interval_type]["y"]),
                        obj_type=interval_type,
                    )
                )
                tmp_xy[interval_type]["x"].clear()
                tmp_xy[interval_type]["y"].clear()

        diffs_y = np.diff(self.y)
        for i, diff in enumerate(diffs_y):
            if diff > 0:
                try_save_interval(Figure.Type.INTERVAL_UP)
                tmp_xy[Figure.Type.INTERVAL_DOWN]["x"].append(self.x[i])
                tmp_xy[Figure.Type.INTERVAL_DOWN]["y"].append(self.y[i])
            if diff < 0:
                try_save_interval(Figure.Type.INTERVAL_DOWN)
                tmp_xy[Figure.Type.INTERVAL_UP]["x"].append(self.x[i])
                tmp_xy[Figure.Type.INTERVAL_UP]["y"].append(self.y[i])

        try_save_interval(Figure.Type.INTERVAL_UP)
        try_save_interval(Figure.Type.INTERVAL_DOWN)

        return intervals
