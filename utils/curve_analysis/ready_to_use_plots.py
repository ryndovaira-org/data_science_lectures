import numpy as np

from utils.imports import *

from utils.curve_analysis.curve import Curve
from utils.curve_analysis.plot_builder import PlotBuilder
from utils.curve_analysis.points import Points


def discontinuous_functions():
    curves = {
        r"infinite": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$\frac{1}{x}$",
                x_min=-4,
                x_max=0,
                formula=lambda x: 1 / x,
            ),
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$\frac{1}{x}$",
                x_min=0,
                x_max=4,
                formula=lambda x: 1 / x,
            ),
        ),
        r"jump": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$x^2$",
                x_min=-2,
                x_max=0.9,
                formula=lambda x: x * x,
            ),
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$x^2 + 1$",
                x_min=1.1,
                x_max=2,
                formula=lambda x: x * x + 1,
            ),
            dict(
                obj_type=Points.Type.EMPTY,
                label=r"$singularity$",
                x_min=1,
                x_max=1,
                formula=lambda x: 0 * x + 1,
            ),
            dict(
                obj_type=Points.Type.EMPTY,
                label=r"$singularity$",
                x_min=1,
                x_max=1,
                formula=lambda x: 0 * x + 2,
            ),
        ),
        r"removable": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$x^2 + 1$",
                x_min=-2,
                x_max=0.9,
                formula=lambda x: x * x + 1,
            ),
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$x^2 + 1$",
                x_min=1.1,
                x_max=2,
                formula=lambda x: x * x + 1,
            ),
            dict(
                obj_type=Points.Type.EMPTY,
                label=r"$singularity$",
                x_min=1,
                x_max=1,
                formula=lambda x: 0 * x + 2,
            ),
        ),
        r"endpoint": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                label=r"$\sqrt{x}$",
                x_min=0,
                x_max=4,
                formula=np.sqrt,
            ),
            dict(
                obj_type=Points.Type.FULL,
                label=r"$singularity$",
                x_min=0,
                x_max=0,
                formula=lambda x: 0 * x,
            ),
        ),
    }
    PlotBuilder(curves, False, 8, 4)


def sign_function():
    curves = {
        "sign(x)": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=-0.1,
                formula=np.sign,
                label="$sign(x)$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=0.1,
                x_max=4,
                formula=np.sign,
                label="$sign(x)$",
            ),
            dict(
                obj_type=Points.Type.FULL,
                x_min=0,
                x_max=0,
                formula=np.sign,
                label="$sign(x)$",
            ),
        )
    }
    PlotBuilder(curves, False, 6, 4)


def example_functions_to_analyse():
    curves_to_analyse = {
        "sin(x)": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-1.5 * np.pi,
                x_max=1.5 * np.pi,
                formula=np.sin,
                label=r"$sin(x)$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-1.5 * np.pi,
                x_max=1.5 * np.pi,
                formula=np.cos,
                label=r"$sin'(x) = cos(x)$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-1.5 * np.pi,
                x_max=1.5 * np.pi,
                formula=lambda x: -np.sin(x),
                label=r"$sin''(x) = -sin(x)$",
            ),
        ),
        r"$x ^ 2$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=np.square,
                label=r"$x ^ 2$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 2 * x,
                label=r"$x^{2}' = 2x$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: 2 + 0 * x,
                label=r"$x^{2}'' = 2$",
            ),
        ),
        f"$x^3$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: x * x * x,
                label=r"$x^{3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 3 * x * x,
                label=r"$x^{3}' = 3x^2$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: 6 * x,
                label=r"$x^{3}'' = 6x$",
            ),
        ),
    }

    PlotBuilder(curves_to_analyse, True, 12, 9)


def power_functions():
    curves_x_3 = {
        r"$x^3$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: x**3,
                label="$x^3$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: x**3 - 50,
                label="$x^3 - 50$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: x**3 + 50,
                label="$x^3 + 50$",
            ),
        ),
    }
    curves_x_6 = {
        "$x^6$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: x**6,
                label="$x^6$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 4 * (x**6),
                label="$4 * x^6$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: 0.25 * (x**6),
                label="$0.25 * x^6$",
            ),
        ),
    }
    curves_x_pow_frac = {
        r"$x^\frac{1}{4}$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=0,
                x_max=4,
                formula=lambda x: x ** (1 / 4),
                label=r"$x^\frac{1}{4}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=0,
                x_max=4,
                formula=lambda x: 4 * x ** (1 / 4),
                label=r"$4 * x^\frac{1}{4}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=0,
                x_max=4,
                formula=lambda x: 0.25 * x ** (1 / 4),
                label=r"$0.25 * x^\frac{1}{4}$",
            ),
        ),
        r"$x^\frac{3}{2}$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: x ** (3 / 2),
                label=r"$x^\frac{3}{2}$",
            ),
        ),
    }

    curves_x_minus = {
        r"$x^{-3}$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-0.1,
                x_max=-0.01,
                formula=lambda x: x ** (-3),
                label=r"$x^{-3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=0.01,
                x_max=0.1,
                formula=lambda x: x ** (-3),
                label=r"$x^{-3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-0.1,
                x_max=-0.01,
                formula=lambda x: 2 * x ** (-3),
                label=r"$4 * x^{-3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=0.01,
                x_max=0.1,
                formula=lambda x: 2 * x ** (-3),
                label=r"$4 * x^{-3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=-0.1,
                x_max=-0.01,
                formula=lambda x: 0.25 * x ** (-3),
                label=r"$0.25 * x^{-3}$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_2,
                x_min=0.01,
                x_max=0.1,
                formula=lambda x: 0.25 * x ** (-3),
                label=r"$0.25 * x^{-3}$",
            ),
        )
    }
    PlotBuilder(curves_x_3, False)
    PlotBuilder(curves_x_6, False)
    PlotBuilder(curves_x_pow_frac, False)
    PlotBuilder(curves_x_minus, False)


def exponential_functions():
    curves = {
        "$a^x$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: 2**x,
                label="$2^x$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 0.5**x,
                label="$0.5^x$",
            ),
        ),
    }

    PlotBuilder(curves, False)


def logarithm_functions():
    curves = {
        r"$\log_{2}x$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: np.log2(x),
                label=r"$\log_{2}x$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: np.log2(-x),
                label=r"$\log_{2}(-x)$",
            ),
        ),
    }

    PlotBuilder(curves, False)


def trigonometric_functions():
    curves = {
        r"$\sin & \cos$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=np.sin,
                label=r"$\sin(x)$",
            ),
            dict(
                obj_type=Curve.Type.MAIN_1,
                x_min=-4,
                x_max=4,
                formula=np.cos,
                label=r"$\cos(x)$",
            ),
        ),
    }

    PlotBuilder(curves, False)


def identity_function():
    curves = {
        r"$identity functon$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=lambda x: x,
                label=r"$f(x) = x$",
            ),
        ),
    }
    PlotBuilder(curves, False)


def absolute_value():
    curves = {
        r"$abs$": (
            dict(
                obj_type=Curve.Type.MAIN_0,
                x_min=-4,
                x_max=4,
                formula=abs,
                label=r"$f(x) = |x|$",
            ),
        ),
    }
    PlotBuilder(curves, False)


if __name__ == "__main__":
    example_functions_to_analyse()
