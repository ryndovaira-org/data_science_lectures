from abc import abstractmethod
from enum import Enum, auto

from utils.imports import *


class Figure:
    AROUND_DECIMALS = 2
    LIM_OFFSET = 2

    class Type(Enum):
        CURVE = auto()
        DERIVATIVE_1 = auto()
        DERIVATIVE_2 = auto()
        INTERVAL_UP = (auto(),)
        INTERVAL_DOWN = auto()
        INTERVAL_ABOVE_0 = auto()
        INTERVAL_BELOW_0 = (auto(),)
        COORDINATE_INTERVAL_X = auto()
        COORDINATE_INTERVAL_Y = auto()
        POINT_MIN = auto()
        POINT_MAX = auto()
        POINT_Y0 = auto()
        POINT_EMPTY = auto()
        POINT_FULL = auto()

    PARAMS = {
        Type.CURVE: dict(
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
        Type.INTERVAL_UP: dict(
            # label="interval up",
            marker=",",
            c="#E61D00",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        ),
        Type.INTERVAL_DOWN: dict(
            # label="interval down",
            marker=",",
            c="#3A30E6",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        ),
        Type.INTERVAL_ABOVE_0: dict(
            # label="interval above 0",
            marker=",",
            c="#E65D6F",
            linewidth=1,
            alpha=0.5,
            zorder=4,
        ),
        Type.INTERVAL_BELOW_0: dict(
            # label="interval below 0",
            marker=",",
            c="#187099",
            linewidth=1,
            alpha=0.5,
            zorder=4,
        ),
        Type.COORDINATE_INTERVAL_X: dict(
            # label="D(y)",
            marker=".",
            c="#E5E180",
            linewidth=2,
            alpha=0.25,
            zorder=0,
        ),
        Type.COORDINATE_INTERVAL_Y: dict(
            # label="E(y)",
            marker=".",
            c="#E5E180",
            linewidth=2,
            alpha=0.25,
            zorder=0,
        ),
        Type.POINT_MAX: dict(
            # label="max",
            marker="*",
            c="#C0E62C",
            alpha=0.35,
            s=50,
            zorder=2,
        ),
        Type.POINT_MIN: dict(
            # label="min",
            marker="*",
            c="#37E651",
            alpha=0.35,
            s=50,
            zorder=2,
        ),
        Type.POINT_Y0: dict(
            # label="y=0",
            marker="o",
            c="#069900",
            alpha=0.35,
            s=150,
            zorder=2,
        ),
        Type.POINT_EMPTY: dict(
            # label="y=0",
            marker="o",
            c="#AE351C",
            alpha=0.8,
            s=100,
            zorder=2,
        ),
        Type.POINT_FULL: dict(
            # label="y=0",
            marker=".",
            c="#AE351C",
            alpha=0.8,
            s=100,
            zorder=2,
        ),
    }

    def __init__(
        self,
            ax: axes.Axes,
            x: np.ndarray,
            y: np.ndarray,
            obj_type: Type,
            label: str
    ):
        self.ax = ax
        self.x = x
        self.y = y
        self.obj_type = obj_type
        self.label = label

    @abstractmethod
    def draw(self):
        ...

    @property
    def x_round(self):
        return np.around(self.x, self.AROUND_DECIMALS)

    @property
    def y_round(self):
        return np.around(self.y, self.AROUND_DECIMALS)
