from abc import abstractmethod
from typing import Callable

from utils.imports import *


class Plot:
    AROUND_DECIMALS = 2
    LIM_OFFSET = 2
    LIN_SPACE_NUM = 1000

    def __init__(
        self,
        ax: axes.Axes,
        x: np.ndarray,
        y: np.ndarray,
        label: str,
        formula: Callable[[np.ndarray], np.ndarray],
    ):
        self.ax = ax
        self.x = x
        self.y = y
        self.label = label
        self.formula = formula

    @abstractmethod
    def draw(self):
        ...

    @property
    def x_round(self):
        return np.around(self.x, self.AROUND_DECIMALS)

    @property
    def y_round(self):
        return np.around(self.y, self.AROUND_DECIMALS)
