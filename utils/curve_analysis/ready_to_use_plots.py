from utils.imports import *

from utils.curve_analysis.curve import Curve
from utils.curve_analysis.plot_builder import PlotBuilder
from utils.curve_analysis.points import Points


def discontinuous_functions():
    curves = {
        r"infinite": (
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$\frac{1}{x}$",
                x_min=-4,
                x_max=0,
                formula=lambda x: 1 / x,
            ),
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$\frac{1}{x}$",
                x_min=0,
                x_max=4,
                formula=lambda x: 1 / x,
            ),
        ),
        r"jump": (
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$x^2$",
                x_min=-2,
                x_max=0.95,
                formula=lambda x: x * x,
            ),
            dict(
                obj_type=Curve.Type.MAIN,
                label=r"$x^2 + 2$",
                x_min=1.05,
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
    }
    PlotBuilder(curves, False, 8, 4)


def sign_function():
    curves = {
        "sign(x)": (
            dict(
                obj_type=Curve.Type.MAIN,
                x_min=-4,
                x_max=-0.1,
                formula=np.sign,
                label="$sign(x)$",
            ),
            dict(
                obj_type=Curve.Type.MAIN,
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
                obj_type=Curve.Type.MAIN,
                x_min=-np.pi,
                x_max=np.pi,
                formula=np.sin,
                label=r"$sin(x)$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_1,
                x_min=-np.pi,
                x_max=np.pi,
                formula=np.cos,
                label=r"$sin'(x) = cos(x)$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_2,
                x_min=-np.pi,
                x_max=np.pi,
                formula=lambda x: -np.sin(x),
                label=r"$sin''(x) = -sin(x)$",
            ),
        ),
        r"$x ^ 2$": (
            dict(
                obj_type=Curve.Type.MAIN,
                x_min=-4,
                x_max=4,
                formula=np.square,
                label=r"$x ^ 2$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 2 * x,
                label=r"$x^{2}' = 2x$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: 2 + 0 * x,
                label=r"$x^{2}'' = 2$",
            ),
        ),
        f"$x^3$": (
            dict(
                obj_type=Curve.Type.MAIN,
                x_min=-4,
                x_max=4,
                formula=lambda x: x * x * x,
                label=r"$x^{3}$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_1,
                x_min=-4,
                x_max=4,
                formula=lambda x: 3 * x * x,
                label=r"$x^{3}' = 3x^2$",
            ),
            dict(
                obj_type=Curve.Type.DERIVATIVE_2,
                x_min=-4,
                x_max=4,
                formula=lambda x: 6 * x,
                label=r"$x^{3}'' = 6x$",
            ),
        ),
    }

    PlotBuilder(curves_to_analyse)


if __name__ == '__main__':
    ...
