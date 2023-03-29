from abc import abstractmethod
from enum import Enum, auto
from typing import Callable

import numpy as np

from .imports import *


class Figure:
    AROUND_DECIMALS = 2
    LIM_OFFSET = 2

    class Type(Enum):
        ORIGINAL = auto()

        DERIVATIVE_1 = auto()
        DERIVATIVE_2 = auto()

        INTERVAL_UP = auto(),
        INTERVAL_DOWN = auto()

        INTERVAL_ABOVE_0 = auto()
        INTERVAL_BELOW_0 = auto(),

        COORDINATE_INTERVAL_X = auto()
        COORDINATE_INTERVAL_Y = auto()

        POINT_MIN = auto()
        POINT_MAX = auto()

        POINT_Y0 = auto()

    PARAMS = {
        Type.ORIGINAL: dict(label='original',
                            marker='.',
                            c='#00E6B3',
                            linewidth=6,
                            alpha=0.5,
                            zorder=1),

        Type.DERIVATIVE_1: dict(label='derivative 1',
                                marker='.',
                                c='#43A2E6',
                                linewidth=6,
                                alpha=0.5,
                                zorder=1),
        Type.DERIVATIVE_2: dict(label='derivative 2',
                                marker='.',
                                c='#586F80',
                                linewidth=6,
                                alpha=0.5,
                                zorder=1),

        Type.INTERVAL_UP: dict(label='interval up',
                               marker=',',
                               c='#E61D00',
                               linewidth=2,
                               alpha=0.5,
                               zorder=3),
        Type.INTERVAL_DOWN: dict(label='interval down',
                                 marker=',',
                                 c='#3A30E6',
                                 linewidth=2,
                                 alpha=0.5,
                                 zorder=3),

        Type.INTERVAL_ABOVE_0: dict(label='interval above 0',
                                    marker=',',
                                    c='#E65D6F',
                                    linewidth=1,
                                    alpha=0.5,
                                    zorder=4),
        Type.INTERVAL_BELOW_0: dict(label='interval below 0', marker=',', c='#187099', linewidth=1, alpha=0.5,
                                    zorder=4),

        Type.COORDINATE_INTERVAL_X: dict(label='D(y)', marker='.', c='#E5E180', linewidth=2, alpha=0.25, zorder=0),
        Type.COORDINATE_INTERVAL_Y: dict(label='E(y)', marker='.', c='#E5E180', linewidth=2, alpha=0.25, zorder=0),

        Type.POINT_MAX: dict(label='max', marker='*', c='#C0E62C', alpha=0.35, s=50, zorder=2),
        Type.POINT_MIN: dict(label='min', marker='*', c='#37E651', alpha=0.35, s=50, zorder=2),

        Type.POINT_Y0: dict(label='y=0', marker='o', c='#069900', alpha=0.35, s=150, zorder=2)
    }

    def __init__(self, ax: axes.Axes, x: np.ndarray, y: np.ndarray, obj_type: Type):
        self.ax = ax
        self.x = x
        self.y = y
        self.obj_type = obj_type

    def draw(self):
        ...


class Points(Figure):
    def draw(self):
        self.ax.scatter(x=self.x,
                        y=self.y,
                        **self.PARAMS.get(self.obj_type,
                                          dict()))


class Interval(Figure):
    @property
    def min_y(self):
        return min(self.y) - self.LIM_OFFSET

    @property
    def max_y(self):
        return max(self.y) + self.LIM_OFFSET

    def draw(self):
        self.ax.plot(self.x,
                     self.y,
                     **self.PARAMS.get(self.obj_type,
                                       dict()))


class Curve(Interval):
    LIN_SPACE_NUM = 1000

    def __init__(self,
                 ax: axes.Axes,
                 x: float | np.ndarray,
                 y: float | np.ndarray,
                 obj_type: Figure.Type,
                 formula: Callable[[np.ndarray], np.ndarray] = None):
        super().__init__(ax, x, y, obj_type)
        self.formula = formula

    @classmethod
    def get_curve_by_formula(cls,
                             ax: axes.Axes,
                             obj_type: Figure.Type,
                             x_min: float,
                             x_max: float,
                             formula: Callable[[np.ndarray], np.ndarray]):
        x = np.linspace(x_min, x_max, cls.LIN_SPACE_NUM)
        y = formula(x)
        return Curve(ax=ax,
                     x=x,
                     y=y,
                     obj_type=obj_type,
                     formula=formula)

    def draw(self):
        super(Curve, self).draw()
        ax_y_min, ax_y_max = self.ax.get_ylim()

        if ax_y_min > self.min_y:
            self.ax.set_ylim(self.min_y,
                             ax_y_max)

    @property
    def rounded_x(self):
        return np.around(self.x, self.AROUND_DECIMALS)

    @property
    def rounded_y(self):
        return np.around(self.y, self.AROUND_DECIMALS)

    def curve_analysis(self):
        figures = [self.get_d_y(),
                   self.get_e_y(),
                   self.get_xs_where_y_eq_0(),
                   *self.get_x_where_y_below_above_0(),
                   *self.get_curve_up_down()]
        return figures

    def get_max_min_point(self):
        ...

    def get_d_y(self):
        return Interval(ax=self.ax,
                        x=self.x,
                        y=np.full((len(self.x), 1), 0),
                        obj_type=Figure.Type.COORDINATE_INTERVAL_X)

    def get_e_y(self):
        return Interval(ax=self.ax,
                        x=np.full((len(self.x), 1), 0),
                        y=self.y,
                        obj_type=Figure.Type.COORDINATE_INTERVAL_Y)

    def get_xs_where_y_eq_0(self):
        sorted_xs = sorted([xi for xi in self.rounded_x[np.where(self.rounded_y == 0)]])
        diff = np.ediff1d(sorted_xs)
        threshold = 0.15
        if np.count_nonzero(diff < threshold):
            to_keep = np.where(diff >= threshold)
            if np.count_nonzero(to_keep) == 0:
                median = np.median(sorted_xs)
                return Points(ax=self.ax,
                              x=np.asarray(median),
                              y=np.asarray(0),
                              obj_type=Figure.Type.POINT_Y0)
        return Points(ax=self.ax,
                      x=np.asarray(sorted_xs),
                      y=np.full((1, len(sorted_xs)), 0),
                      obj_type=Figure.Type.POINT_Y0)

    def get_x_where_y_below_above_0(self):
        tmp_xy = {Figure.Type.INTERVAL_ABOVE_0: [],
                  Figure.Type.INTERVAL_BELOW_0: []}
        intervals: list[Interval] = []

        def try_save_interval(interval_type: Figure.Type):
            if len(tmp_xy[interval_type]) > 0:
                intervals.append(Interval(ax=self.ax,
                                          x=np.asarray(tmp_xy[interval_type]),
                                          y=np.full((len(tmp_xy[interval_type]), 1), 0),
                                          obj_type=interval_type))
                tmp_xy[interval_type].clear()

        for (x, y) in zip(self.x, self.y):
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
        tmp_xy = {Figure.Type.INTERVAL_UP: {'x': [],
                                            'y': []},
                  Figure.Type.INTERVAL_DOWN: {'x': [],
                                              'y': []}}

        intervals: list[Interval] = []

        def try_save_interval(interval_type: Figure.Type):
            if len(tmp_xy[interval_type]['x']) > 0:
                intervals.append(Interval(ax=self.ax,
                                          x=np.asarray(tmp_xy[interval_type]['x']),
                                          y=np.asarray(tmp_xy[interval_type]['y']),
                                          obj_type=interval_type))
                tmp_xy[interval_type]['x'].clear()
                tmp_xy[interval_type]['y'].clear()

        diffs_y = np.diff(self.y)
        for i, diff in enumerate(diffs_y):
            if diff > 0:
                try_save_interval(Figure.Type.INTERVAL_UP)
                tmp_xy[Figure.Type.INTERVAL_DOWN]['x'].append(self.x[i])
                tmp_xy[Figure.Type.INTERVAL_DOWN]['y'].append(self.y[i])
            if diff < 0:
                try_save_interval(Figure.Type.INTERVAL_DOWN)
                tmp_xy[Figure.Type.INTERVAL_UP]['x'].append(self.x[i])
                tmp_xy[Figure.Type.INTERVAL_UP]['y'].append(self.y[i])

        try_save_interval(Figure.Type.INTERVAL_UP)
        try_save_interval(Figure.Type.INTERVAL_DOWN)

        return intervals


class CurveAnalyser:
    FIGURE_HEIGHT = 6
    FIGURE_WIDTH = 12

    CURVES = {
        'sin(x)': (dict(obj_type=Figure.Type.ORIGINAL,
                        x_min=-np.pi,
                        x_max=np.pi,
                        formula=np.sin),
                   dict(obj_type=Figure.Type.DERIVATIVE_1,
                        x_min=-np.pi,
                        x_max=np.pi,
                        formula=np.cos),
                   dict(obj_type=Figure.Type.DERIVATIVE_2,
                        x_min=-np.pi,
                        x_max=np.pi,
                        formula=lambda x: -np.sin(x))
                   ),
        u'x\u00B3': (dict(obj_type=Figure.Type.ORIGINAL,
                          x_min=-4,
                          x_max=4,
                          formula=np.square),
                     dict(obj_type=Figure.Type.DERIVATIVE_1,
                          x_min=-4,
                          x_max=4,
                          formula=lambda x: 2 * x),
                     dict(obj_type=Figure.Type.DERIVATIVE_2,
                          x_min=-4,
                          x_max=4,
                          formula=lambda x: 2 + 0 * x)
                     ),
        u'x\u00B2': (dict(obj_type=Figure.Type.ORIGINAL,
                          x_min=-4,
                          x_max=4,
                          formula=lambda x: x * x * x),
                     dict(obj_type=Figure.Type.DERIVATIVE_1,
                          x_min=-4,
                          x_max=4,
                          formula=lambda x: 3 * x * x),
                     dict(obj_type=Figure.Type.DERIVATIVE_2,
                          x_min=-4,
                          x_max=4,
                          formula=lambda x: 6 * x))
    }

    def __init__(self):
        self.figures_to_draw: list[Figure] = []
        fig, self.axes = plt.subplots(nrows=len(self.CURVES),
                                      ncols=1,
                                      sharex=True,
                                      figsize=(self.FIGURE_WIDTH, len(self.CURVES) * self.FIGURE_HEIGHT)
                                      )
        for i, (title, functions) in enumerate(self.CURVES.items()):
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

        for axes in self.axes:
            axes.legend(ncol=3)

        plt.show()


if __name__ == '__main__':
    curve_analyser = CurveAnalyser()
    curve_analyser.draw()
