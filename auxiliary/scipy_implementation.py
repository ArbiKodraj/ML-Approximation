import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

from matplotlib import gridspec
from scipy.optimize import curve_fit
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score


# --------------------------------------------------------------------------- Approximations

def g(x):
    """``Benchmark function.``

    Args:
        x (int, float): Input.

    Returns:
        float: Output. :math:`sin(\\frac{1}{2}x) - 2 cos(2x)`
    """
    return np.sin(0.5 * x) - 2 * np.cos(2 * x)


def five_interp(x, a0, a1, a2, a3, a4):
    """``Approximation degree = 5``
    """
    return a0 + a1 * x + a2 * (x ** 2) + a3 * (x ** 3) + a4 * (x ** 4)


def six_interp(x, a0, a1, a2, a3, a4, a5):
    """``Approximation degree = 6``
    """
    return a0 + a1 * x + a2 * (x ** 2) + a3 * (x ** 3) + a4 * (x ** 4) + a5 * (x ** 5)


def seven_interp(x, a0, a1, a2, a3, a4, a5, a6):
    """``Approximation degree = 7``
    """
    return (
            a0
            + a1 * x
            + a2 * (x ** 2)
            + a3 * (x ** 3)
            + a4 * (x ** 4)
            + a5 * (x ** 5)
            + a6 * (x ** 6)
    )


def eight_interp(x, a0, a1, a2, a3, a4, a5, a6, a7):
    """``Approximation degree = 8``
    """
    return (
            a0
            + a1 * x
            + a2 * (x ** 2)
            + a3 * (x ** 3)
            + a4 * (x ** 4)
            + a5 * (x ** 5)
            + a6 * (x ** 6)
            + a7 * (x ** 7)
    )


def nine_interp(x, a0, a1, a2, a3, a4, a5, a6, a7, a8):
    """``Approximation degree = 9``
    """
    return (
            a0
            + a1 * x
            + a2 * (x ** 2)
            + a3 * (x ** 3)
            + a4 * (x ** 4)
            + a5 * (x ** 5)
            + a6 * (x ** 6)
            + a7 * (x ** 7)
            + a8 * (x ** 8)
    )


def ten_interp(x, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9):
    """``Approximation degree = 10``
    """
    return (
            a0
            + a1 * x
            + a2 * (x ** 2)
            + a3 * (x ** 3)
            + a4 * (x ** 4)
            + a5 * (x ** 5)
            + a6 * (x ** 6)
            + a7 * (x ** 7)
            + a8 * (x ** 8)
            + a9 * (x ** 9)
    )


# --------------------------------------------------------------------------- 3.2.1 Benchmark Exercise: Naive Approximation SciPy

class FCMethod:
    """This object uses the scipy ``curve fit`` method to naively approximate a specific
    function. It plots the interpolation and the real function for different nodes and
    tables the approximation accuracy.

    Args:
        a (int): Lower bound of interval.
        b (int): Upper bound of interval.
        n (int): Number of interpolation nodes.
        func (function): Benchmark function.
        degree (int): Degree of approximation.
    """

    def __init__(self, a, b, n, func, degree):
        """Constructor method. It uses the exact same arguments as the :class:`PMethod`
        constructor method. This could be achieved by inheritance as well.
        """
        self.a = a
        self.b = b
        self.n = n
        self.func = func
        self.degree = degree

    def check_degree(self, increase):
        """Increases approximation degree if degree lies between 5 and 10.

        Args:
            increase (bool): Increases approximation degree by one unit if True.
        """
        if increase == True and self.degree < 10:
            self.degree += 1
        elif self.degree < 5 or self.degree > 10:
            print("Degree must be between 5 and 10!")

    def choose_approx(self):
        """Chooses approximation function by its degree.
        """
        if self.degree == 5:
            self.approx = five_interp
        elif self.degree == 6:
            self.approx = six_interp
        elif self.degree == 7:
            self.approx = seven_interp
        elif self.degree == 8:
            self.approx = eight_interp
        elif self.degree == 9:
            self.approx = nine_interp
        elif self.degree == 10:
            self.approx = ten_interp

    def fit_curve(self):
        """Implementation of scipy curve fit method. Uses least square method to find 
        optimal weight. This yield to the interpolation.
        """
        self.xa = np.linspace(self.a, self.b, self.n)
        self.xb = np.linspace(self.a, self.b, 3 * self.n)
        self.xc = np.linspace(self.a, self.b, 9 * self.n)

        self.popta = curve_fit(self.approx, self.xa, self.func(self.xa))[0]
        self.poptb = curve_fit(self.approx, self.xb, self.func(self.xb))[0]
        self.poptc = curve_fit(self.approx, self.xc, self.func(self.xc))[0]

    def plot_naive_interp(self, N, fs, number_1, number_2):
        """Plots true function and approximation as well as approximation error.

        Args:
            N (int): Number of evaluation nodes.
            fs (tuple): Figuresize
            number_1 (int, float): Number of first figure.
            number_2 (int, float: Number of second figure.
        """
        self.x = np.linspace(self.a, self.b, N)
        fig = plt.figure(figsize=fs)
        gs = gridspec.GridSpec(2, 1, height_ratios=[1.8, 1])
        ax0 = plt.subplot(gs[0])
        ax0.plot(self.x, self.func(self.x), label="Real Function")
        ax0.plot(
            self.x,
            self.approx(self.x, *self.popta),
            label=str(self.n) + " Nodes Approximation",
        )
        ax0.plot(
            self.x,
            self.approx(self.x, *self.poptb),
            label=str(3 * self.n) + " Nodes Approximation",
        )
        ax0.plot(
            self.x,
            self.approx(self.x, *self.poptc),
            label=str(9 * self.n) + " Nodes Approximation",
        )
        ax0.set_title(
            f"Figure {number_1}: Naive Approximation Output "
            + str(self.degree)
            + " Degree"
        )
        plt.grid()
        plt.legend(
            title="Naive Approximation for different Nodes",
            bbox_to_anchor=(1.04, 0.5),
            loc="center left",
            shadow=True,
            fancybox=True,
            borderaxespad=0,
            title_fontsize=12,
        )

        plt.setp(ax0.get_xticklabels(), visible=False)

        ax1 = plt.subplot(gs[1], sharex=ax0)
        ax1.plot(
            self.x,
            self.approx(self.x, *self.popta) - self.func(self.x),
            label=str(self.n) + " Nodes Error",
        )
        ax1.plot(
            self.x,
            self.approx(self.x, *self.poptb) - self.func(self.x),
            label=str(3 * self.n) + " Nodes Error",
        )
        ax1.plot(
            self.x,
            self.approx(self.x, *self.poptc) - self.func(self.x),
            label=str(9 * self.n) + " Nodes Error",
        )
        ax1.set_title(
            f"Figure {number_2}: Naive Approximation Error "
            + str(self.degree)
            + " Degree"
        )
        plt.subplots_adjust(hspace=0.0)
        plt.grid()
        plt.legend(
            title="Error for different Nodes",
            bbox_to_anchor=(1.04, 0.5),
            loc="center left",
            shadow=True,
            fancybox=True,
            borderaxespad=0,
            title_fontsize=12,
        )

        plt.tight_layout()
        plt.show()

    def table_error(self, number):
        """Returns approximation accuracy.

        Args:
            number (int): Number of table.

        Returns:
            pd.DataFrame: Approximation accuracy.
        """
        mae = mean_absolute_error(self.approx(self.x, *self.popta), self.func(self.x))
        maea = mean_absolute_error(self.approx(self.x, *self.poptb), self.func(self.x))
        maeb = mean_absolute_error(self.approx(self.x, *self.poptc), self.func(self.x))

        mse = mean_squared_error(self.approx(self.x, *self.popta), self.func(self.x))
        msea = mean_squared_error(self.approx(self.x, *self.poptb), self.func(self.x))
        mseb = mean_squared_error(self.approx(self.x, *self.poptc), self.func(self.x))

        ev = explained_variance_score(
            self.approx(self.x, *self.popta), self.func(self.x)
        )
        eva = explained_variance_score(
            self.approx(self.x, *self.poptb), self.func(self.x)
        )
        evb = explained_variance_score(
            self.approx(self.x, *self.poptc), self.func(self.x)
        )

        r2 = r2_score(self.approx(self.x, *self.popta), self.func(self.x))
        r2a = r2_score(self.approx(self.x, *self.poptb), self.func(self.x))
        r2b = r2_score(self.approx(self.x, *self.poptc), self.func(self.x))

        df = pd.DataFrame(
            [mae, mse, ev, r2],
            index=[
                "Mean Squared Error",
                "Mean Absolute Error",
                "Explained Variance",
                "$R^2$ Score",
            ],
            columns=[str(self.n) + " Nodes"],
        )
        dfa = pd.DataFrame(
            [maea, msea, eva, r2a],
            index=[
                "Mean Squared Error",
                "Mean Absolute Error",
                "Explained Variance",
                "$R^2$ Score",
            ],
            columns=[str(3 * self.n) + " Nodes"],
        )
        dfb = pd.DataFrame(
            [maeb, mseb, evb, r2b],
            index=[
                "Mean Squared Error",
                "Mean Absolute Error",
                "Explained Variance",
                "$R^2$ Score",
            ],
            columns=[str(9 * self.n) + " Nodes"],
        )

        rslt = pd.concat([df, dfa, dfb], axis=1).style.set_caption(
            f"Table {number}: Accuracy of Naive Approximation for "
            + str(self.degree)
            + " Degrees"
        )
        return rslt


