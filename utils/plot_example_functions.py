from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Callable

import numpy as np
from scipy.interpolate import interp1d

from imports import *


class Figure:
    AROUND_DECIMALS = 2

    class Type(Enum):
        ORIGINAL = auto()

        DERIVATIVE_1 = auto()
        DERIVATIVE_2 = auto()

        INTERVAL_UP = auto(),
        INTERVAL_DOWN = auto()

        COORDINATE_INTERVAL_X = auto()
        COORDINATE_INTERVAL_Y = auto()

        POINT_MIN = auto()
        POINT_MAX = auto()

        POINT_Y0 = auto()

    PARAMS = {
        Type.ORIGINAL: dict(marker=',', c='#00E6B3', linewidth=3, alpha=0.5),

        Type.DERIVATIVE_1: dict(marker=',', c='#43A2E6', linewidth=3),
        Type.DERIVATIVE_2: dict(marker=',', c='#586F80', linewidth=3),

        Type.INTERVAL_UP: dict(marker='^', c='#B355E5', linewidth=1),
        Type.INTERVAL_DOWN: dict(marker='v', c='#E6456C', linewidth=1),

        Type.COORDINATE_INTERVAL_X: dict(marker=',', c='#FF6E30', linewidth=1),
        Type.COORDINATE_INTERVAL_Y: dict(marker=',', c='#FF6E30', linewidth=1),

        Type.POINT_MAX: dict(marker='*', c='#C0E62C', s=50),
        Type.POINT_MIN: dict(marker='*', c='#37E651', s=50),

        Type.POINT_Y0: dict(marker='.', c='#FF3061', s=150)
    }

    def __init__(self, ax: axes.Axes, x: float | np.ndarray, y: float | np.ndarray, obj_type: Type):
        self.ax = ax
        self.x = x
        self.y = y
        self.obj_type = obj_type

    @abstractmethod
    def draw(self):
        ...


class Point(Figure):
    def draw(self):
        self.ax.scatter(x=self.x,
                        y=self.y,
                        **self.PARAMS.get(self.obj_type,
                                          dict()))


class Interval(Figure):
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
                             x_min: float,
                             x_max: float,
                             formula: Callable[[np.ndarray], np.ndarray]) -> Figure:
        x = np.linspace(x_min, x_max, cls.LIN_SPACE_NUM)
        y = formula(x)
        return Curve(ax=ax,
                     x=x,
                     y=y,
                     obj_type=Figure.Type.ORIGINAL,
                     formula=formula)

    @property
    def rounded_x(self):
        return np.around(self.x, self.AROUND_DECIMALS)

    @property
    def rounded_y(self):
        return np.around(self.y, self.AROUND_DECIMALS)

    def curve_analysis(self):
        figures = [self.get_d_y(),
                   self.get_e_y()]
        figures.extend(self.get_xs_where_y_eq_0())

        # curve_up(x[0], x[2])
        # curve_up(x[4], x[-1])
        # curve_down(x[2], x[4])
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

    def eliminate_point_duplicates(self, points):
        sorted_points = sorted(points, key=lambda point: point.x)
        points_x = [point.x for point in sorted_points]
        diff = np.ediff1d(points_x)
        threshold = 0.15
        if np.count_nonzero(diff < threshold):
            to_keep = np.where(diff >= threshold)
            if np.count_nonzero(to_keep) == 0:
                median = np.median(points_x)
                return [Point(ax=self.ax,
                              x=median,
                              y=np.around(self.formula(median), self.AROUND_DECIMALS),
                              obj_type=points[0].obj_type)]
        return sorted_points

    def get_xs_where_y_eq_0(self):
        return self.eliminate_point_duplicates([Point(ax=self.ax,
                                                      x=xi,
                                                      y=0,
                                                      obj_type=Figure.Type.POINT_Y0)
                                                for xi in self.rounded_x[np.where(self.rounded_y == 0)]])

    def get_x_where_y_below_0(self):
        ...

    def get_x_where_y_above_0(self):
        ...

    # def analyse_curve(x, y, formula):
    #     x_y_equal_0 = x[np.where(y == 0)]
    #     print(f'y = 0 where x = {set(x_y_equal_0.tolist())}')
    #     important_points.update([(xi, 0) for xi in x_y_equal_0])
    #
    #     x_where_y_above_0 = x[y > 0]
    #     if len(x_where_y_above_0):
    #         xy_above_0 = (min(x_where_y_above_0), max(x_where_y_above_0))
    #         print(f'y > 0 where x = [{xy_above_0[0]}, {xy_above_0[1]}]')
    #
    #     x_where_y_below_0 = x[y < 0]
    #     if len(x_where_y_below_0):
    #         xy_below_0 = (min(x_where_y_below_0), max(x_where_y_below_0))
    #         print(f'y < 0 where x = [{xy_below_0[0]}, {xy_below_0[1]}]')
    #
    #     sorted_points = tuple(sorted(important_points, key=lambda xy: xy[0]))
    #     points_x = [x for x, y in sorted_points]
    #     diff = np.ediff1d(points_x)
    #     threshold = 0.15
    #     if np.count_nonzero(diff < threshold):
    #         to_keep = np.where(diff >= threshold)
    #         if np.count_nonzero(to_keep) == 0:
    #             median = np.median(points_x)
    #             return [(median, np.around(formula(median), AROUND_DECIMALS))]
    #     return sorted_points


class CurveAnalyser:
    LIM_OFFSET = 1

    CURVES = {
        'sin(x)': dict(x_min=-np.pi,
                       x_max=np.pi,
                       formula=np.sin),
        u'x\u00B3': dict(x_min=-4,
                         x_max=4,
                         formula=np.square),
        u'x\u00B2': dict(x_min=-4,
                         x_max=4,
                         formula=lambda x: x * x * x)
    }

    def __init__(self):
        self.figures_to_draw: list[Figure] = []
        fig, axs = plt.subplots(nrows=1,
                                ncols=len(self.CURVES),
                                sharex=True)
        fig.suptitle('Curve sketching')

        for i, (title, params) in enumerate(self.CURVES.items()):
            axs[i].set_title(title)
            axs[i].grid()

            curve = Curve.get_curve_by_formula(ax=axs[i], **params)
            self.figures_to_draw.append(curve)
            self.figures_to_draw.extend(curve.curve_analysis())

    def draw(self):
        for figure in self.figures_to_draw:
            figure.draw()

        # ax.xlim(min(x) - lim_offset, max(x) + lim_offset)
        # ax.ylim(min(y) - lim_offset, max(y) + lim_offset)
        plt.axis('tight')
        plt.show()


def curve_up(x_start, x_end):
    up_arrow = u'\u2193'
    print(f'y{up_arrow} where x = [{x_start}, {x_end}]')


def curve_down(x_start, x_end):
    down_arrow = u'\u2191'
    print(f'y{down_arrow} where x = [{x_start}, {x_end}]')


if __name__ == '__main__':
    curve_analyser = CurveAnalyser()
    curve_analyser.draw()
