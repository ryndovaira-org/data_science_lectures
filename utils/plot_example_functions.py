from .imports import *

from scipy.interpolate import interp1d


def plot_curve_by_points(x, y):
    x_text = x - 0.4
    y_text = y - 0.7

    x_new = np.linspace(x.min(), x.max(), 500)

    f = interp1d(x, y, kind='quadratic')
    y_smooth = f(x_new)

    plt.plot(x_new[2:], y_smooth[2:], marker=' ', c='g')
    plt.scatter(x[0], y[0], s=80, marker='o', facecolors='none', edgecolors='g')
    plt.scatter(x[-1], y[-1], s=80, marker='o', facecolors='g', edgecolors='g')
    plt.scatter(x[1:-1], y[1:-1], s=15, c='g')
    for i in range(len(x)):
        plt.annotate(f'({x[i]}, {y[i]})', xy=(x[i], y[i]), xytext=(x_text[i], y_text[i]), c='r')

    plt.grid()
    lim_offset = 1
    plt.xlim(min(x) - lim_offset, max(x) + lim_offset)
    plt.ylim(min(y) - lim_offset, max(y) + lim_offset)


def analyse_curve_by_dots(x, y):
    print(f'D(y) = ({min(x)}, {max(x)}]')
    print(f'E(y) = [{min(y)}, {max(y)}]')

    x_y_equal_0 = x[y == 0]
    print(f'y = 0 where x = {x_y_equal_0.tolist()}')

    x_y_above_0 = x[y > 0]
    x_y_below_0 = x[y < 0]
    print(f'y > 0 where x = [{min(x_y_above_0)}, {max(x_y_above_0)}]')
    print(f'y < 0 where x = [{min(x_y_below_0)}, {max(x_y_below_0)}]')


def curve_up(x_start, x_end):
    up_arrow = u'\u2191'
    print(f'y{up_arrow} where x = [{x_start}, {x_end}]')


def curve_down(x_start, x_end):
    down_arrow = u'\u2193'
    print(f'y{down_arrow} where x = [{x_start}, {x_end}]')


def general_function():
    print('General function')
    x = np.array([-3, -1, 0, 1, 2, 3, 4])
    y = np.array([-1, 2, 4, 2, 0, 2, 3])

    plot_curve_by_points(x, y)

    curve_up(x[0], x[2])
    curve_up(x[4], x[-1])
    curve_down(x[2], x[4])


def even_function():
    print('Even function')


def odd_function():
    print('Odd function')


if __name__ == '__main__':
    general_function()
