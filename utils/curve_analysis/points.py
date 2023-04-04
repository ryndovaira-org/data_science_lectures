from enum import Enum, auto
from typing import Callable

import numpy as np
from matplotlib import axes

from utils.curve_analysis.plot import Plot


class Points(Plot):
    class Type(Enum):
        MIN = auto()
        MAX = auto()
        Y0 = auto()
        EMPTY = auto()
        FULL = auto()

    PARAMS = {
        Type.MAX: dict(
            # label="max",
            marker="*",
            c="#C0E62C",
            alpha=0.75,
            s=50,
            zorder=2,
        ),
        Type.MIN: dict(
            # label="min",
            marker="*",
            c="#37E651",
            alpha=0.75,
            s=50,
            zorder=2,
        ),
        Type.Y0: dict(
            # label="y=0",
            marker="o",
            c="#069900",
            alpha=0.75,
            s=150,
            zorder=2,
        ),
        Type.EMPTY: dict(
            # label="y=0",
            marker="o",
            facecolors="none",
            edgecolors="#00E6B3",
            alpha=0.75,
            s=100,
            zorder=2,
        ),
        Type.FULL: dict(
            # label="y=0",
            marker="o",
            c="#00E6B3",
            alpha=0.75,
            s=100,
            zorder=2,
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
        x = np.around(
            np.linspace(start=x_min, stop=x_max, num=cls.LIN_SPACE_NUM),
            cls.AROUND_DECIMALS,
        )
        y = np.around(formula(x))
        return Points(ax=ax, label=label, x=x, y=y, obj_type=obj_type, formula=formula)

    def draw(self):
        self.ax.scatter(
            x=self.x,
            y=self.y,
            label=self.label,
            **self.PARAMS.get(self.obj_type, dict())
        )
