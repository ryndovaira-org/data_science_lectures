from enum import Enum, auto
from typing import Callable

import numpy as np
from matplotlib import axes

from utils.curve_analysis.plot import Plot
from utils.curve_analysis.points import Points


class Curve(Plot):
    class Type(Enum):
        MAIN = auto()
        DERIVATIVE_1 = auto()
        DERIVATIVE_2 = auto()
        UP = auto()
        DOWN = auto()
        ABOVE_0 = auto()
        BELOW_0 = auto()
        COORDINATE_X = auto()
        COORDINATE_Y = auto()

    PARAMS = {
        Type.MAIN: dict(
            marker=",",
            c="#00E6B3",
            linewidth=6,
            alpha=0.75,
            zorder=1,
        ),
        Type.DERIVATIVE_1: dict(
            # label="derivative 1",
            marker=".",
            c="#43A2E6",
            linewidth=6,
            alpha=0.5,
            zorder=1,
        ),
        Type.DERIVATIVE_2: dict(
            # label="derivative 2",
            marker=".",
            c="#586F80",
            linewidth=6,
            alpha=0.5,
            zorder=1,
        ),
        Type.UP: dict(
            # label="interval up",
            marker=",",
            c="#E61D00",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        ),
        Type.DOWN: dict(
            # label="interval down",
            marker=",",
            c="#3A30E6",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        ),
        Type.ABOVE_0: dict(
            # label="interval above 0",
            marker=",",
            c="#E65D6F",
            linewidth=1,
            alpha=0.5,
            zorder=4,
        ),
        Type.BELOW_0: dict(
            # label="interval below 0",
            marker=",",
            c="#187099",
            linewidth=1,
            alpha=0.5,
            zorder=4,
        ),
        Type.COORDINATE_X: dict(
            # label="D(y)",
            marker=".",
            c="#E5E180",
            linewidth=2,
            alpha=0.25,
            zorder=0,
        ),
        Type.COORDINATE_Y: dict(
            # label="E(y)",
            marker=".",
            c="#E5E180",
            linewidth=2,
            alpha=0.25,
            zorder=0,
        ),
    }

    def __init__(
        self,
        ax: axes.Axes,
        x: np.ndarray,
        y: np.ndarray,
        label: str,
        obj_type: Type,
        formula: Callable[[np.ndarray], np.ndarray] = None,
    ):
        super().__init__(ax, x, y, label, formula)
        self.obj_type = obj_type

    def draw(self):
        self.ax.plot(
            self.x, self.y, label=self.label, **self.PARAMS.get(self.obj_type, dict())
        )

    @classmethod
    def by_formula(
        cls,
        ax: axes.Axes,
        label: str,
        obj_type: Type,
        x_min: float,
        x_max: float,
        formula: Callable[[np.ndarray], np.ndarray],
    ):
        x = np.linspace(start=x_min, stop=x_max, num=cls.LIN_SPACE_NUM)
        y = formula(x)
        return Curve(ax=ax, label=label, x=x, y=y, obj_type=obj_type, formula=formula)

    def curve_analysis(self):
        figures = [
            self.get_d_y(),
            self.get_e_y(),
            self.get_xs_where_y_eq_0(),
            *self.get_x_where_y_below_above_0(),
            *self.get_curve_up_down(),
        ]
        return figures

    def get_d_y(self):
        return Curve(
            ax=self.ax,
            label=self.label,
            x=self.x,
            y=np.full((len(self.x), 1), 0),
            obj_type=Curve.Type.COORDINATE_X,
        )

    def get_e_y(self):
        return Curve(
            ax=self.ax,
            label=self.label,
            x=np.full((len(self.x), 1), 0),
            y=self.y,
            obj_type=Curve.Type.COORDINATE_Y,
        )

    def get_xs_where_y_eq_0(self):
        sorted_xs = sorted([xi for xi in self.x_round[np.where(self.y_round == 0)]])
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
                    obj_type=Points.Type.Y0,
                    label="$y = 0$",
                )
        return Points(
            ax=self.ax,
            x=np.asarray(sorted_xs),
            y=np.full((1, len(sorted_xs)), 0),
            obj_type=Points.Type.Y0,
            label="$y = 0$",
        )

    def get_x_where_y_below_above_0(self):
        tmp_xy = {Curve.Type.ABOVE_0: [], Curve.Type.BELOW_0: []}
        intervals: list[Curve] = []

        def try_save_interval(interval_type: Curve.Type):
            if len(tmp_xy[interval_type]) > 0:
                intervals.append(
                    Curve(
                        ax=self.ax,
                        label=self.label,
                        x=np.asarray(tmp_xy[interval_type]),
                        y=np.full((len(tmp_xy[interval_type]), 1), 0),
                        obj_type=interval_type,
                    )
                )
                tmp_xy[interval_type].clear()

        for x, y in zip(self.x, self.y):
            if y > 0:
                try_save_interval(Curve.Type.BELOW_0)
                tmp_xy[Curve.Type.ABOVE_0].append(x)
            elif y < 0:
                try_save_interval(Curve.Type.ABOVE_0)
                tmp_xy[Curve.Type.BELOW_0].append(x)

        try_save_interval(Curve.Type.BELOW_0)
        try_save_interval(Curve.Type.ABOVE_0)

        return intervals

    def get_curve_up_down(self):
        tmp_xy = {
            Curve.Type.UP: {"x": [], "y": []},
            Curve.Type.DOWN: {"x": [], "y": []},
        }

        intervals: list[Curve] = []

        def try_save_interval(interval_type: Curve.Type):
            if len(tmp_xy[interval_type]["x"]) > 0:
                intervals.append(
                    Curve(
                        ax=self.ax,
                        label=self.label,
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
                try_save_interval(Curve.Type.UP)
                tmp_xy[Curve.Type.DOWN]["x"].append(self.x[i])
                tmp_xy[Curve.Type.DOWN]["y"].append(self.y[i])
            if diff < 0:
                try_save_interval(Curve.Type.DOWN)
                tmp_xy[Curve.Type.UP]["x"].append(self.x[i])
                tmp_xy[Curve.Type.UP]["y"].append(self.y[i])

        try_save_interval(Curve.Type.UP)
        try_save_interval(Curve.Type.DOWN)

        return intervals
