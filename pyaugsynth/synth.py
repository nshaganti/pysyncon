from typing import Union, Optional, Literal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds, LinearConstraint

from .dataprep import Dataprep


class Synth:
    def __init__(self) -> None:
        self.dataprep = None
        self.W = None
        self.loss_W = None
        self.V = None
        self.loss_V = None

    def fit(
        self,
        dataprep: Optional[Dataprep] = None,
        X0: Optional[pd.DataFrame] = None,
        X1: Optional[Union[pd.Series, pd.DataFrame]] = None,
        Z0: Optional[pd.DataFrame] = None,
        Z1: Optional[Union[pd.Series, pd.DataFrame]] = None,
        custom_V: Optional[np.ndarray] = None,
        optim_method: Literal["Nelder-Mead", "BFGS"] = "Nelder-Mead",
        optim_initial: Literal["equal", "ols"] = "equal",
        optim_options: dict = {"maxiter": 1000},
    ):
        if dataprep:
            self.dataprep = dataprep
            X0, X1 = dataprep.compute_X0_X1()
            Z0, Z1 = dataprep.compute_Z0_Z1()
        else:
            if X0 is None or X1 is None or Z0 is None or Z1 is None:
                raise ValueError(
                    "dataprep must be set or (X0, X1, Z0, X1) must all be set."
                )

        X = pd.concat([X0, X1], axis=1)
        X_scaled = X.divide(X.var(axis=1).pow(0.5), axis=0)
        X0_scaled, X1_scaled = X_scaled.drop(columns=X1.name), X_scaled[X1.name]

        X0_arr = X0_scaled.to_numpy()
        X1_arr = X1_scaled.to_numpy()
        Z0_arr = Z0.to_numpy()
        Z1_arr = Z1.to_numpy()

        if custom_V is not None:
            W, loss_W, loss_V = self.optimize_W(
                V=custom_V, X0=X0_arr, X1=X1_arr, Z0=Z0_arr, Z1=Z1_arr
            )
            self.W, self.loss_W, self.V, self.loss_V = W, loss_W, custom_V, loss_V

        n_r, _ = X0_arr.shape

        if optim_initial == "equal":
            x0 = [1 / n_r] * n_r
        elif optim_initial == "ols":
            X_arr = np.hstack([X0_arr, X1_arr.reshape(-1, 1)])
            X_arr = np.hstack([np.array([1] * X_arr.shape[1], ndmin=2).T, X_arr.T])
            Z_arr = np.hstack([Z0_arr, Z1_arr.reshape(-1, 1)])
            beta = np.linalg.inv(X_arr.T @ X_arr) @ X_arr.T @ Z_arr.T
            beta = beta[1:,]

            x0 = np.diag(beta @ beta.T)
            x0 = x0 / sum(x0)
        else:
            raise ValueError("Unknown option for `optim_initial`.")

        def fun(x):
            V = np.diag(np.abs(x)) / np.sum(np.abs(x))
            _, _, loss_V = self.optimize_W(
                V=V, X0=X0_arr, X1=X1_arr, Z0=Z0_arr, Z1=Z1_arr
            )
            return loss_V

        res = minimize(fun=fun, x0=x0, method=optim_method, options=optim_options)
        V = np.diag(np.abs(res["x"])) / np.sum(np.abs(res["x"]))
        W, loss_W, loss_V = self.optimize_W(
            V=V, X0=X0_arr, X1=X1_arr, Z0=Z0_arr, Z1=Z1_arr
        )
        self.W, self.loss_W, self.V, self.loss_V = W, loss_W, V, loss_V

    @staticmethod
    def optimize_W(
        V: np.ndarray,
        X0: np.ndarray,
        X1: np.ndarray,
        Z0: np.ndarray,
        Z1: np.ndarray,
        qp_method: Literal["SLSQP"] = "SLSQP",
        qp_options: dict = {"maxiter": 1000},
    ):
        _, n_c = X0.shape

        P = X0.T @ V @ X0
        q = -1.0 * X1.T @ V @ X0

        def fun(x):
            return q.T @ x + 0.5 * x.T @ P @ x

        bounds = Bounds(lb=np.array([0.0] * n_c).T, ub=np.array([1.0] * n_c).T)
        constraints = LinearConstraint(A=np.array([1.0] * n_c), lb=1.0, ub=1.0)

        x0 = np.array([1 / n_c] * n_c)
        res = minimize(
            fun=fun,
            x0=x0,
            bounds=bounds,
            constraints=constraints,
            method=qp_method,
            options=qp_options,
        )
        W, loss_W = res["x"], res["fun"]
        loss_V = (Z1 - Z0 @ W).T @ (Z1 - Z0 @ W) / len(Z0)
        return W, loss_W, loss_V

    def path_plot(self, treatment_time: Optional[int] = None, grid: bool = True):
        if self.dataprep is None:
            raise ValueError("dataprep must be set for automatic plots.")
        if self.W is None:
            raise ValueError("Fit data before plotting.")

        ts_all = self.dataprep.foo.pivot(
            index=self.dataprep.time_variable,
            columns=self.dataprep.unit_variable,
            values=self.dataprep.dependent,
        )

        ts_treated = ts_all[self.dataprep.treatment_identifier]
        ts_treated.name = "treated"

        ts_units = ts_all[list(self.dataprep.controls_identifier)]
        ts_synthetic = (ts_units * self.W).sum(axis=1)
        ts_synthetic.name = "synthetic"

        ts_treated.plot(ylabel=self.dataprep.dependent, color="black", linewidth=1)
        ts_synthetic.plot(
            ylabel=self.dataprep.dependent,
            color="black",
            linewidth=1,
            linestyle="dashed",
        )

        if treatment_time:
            ymin = min(min(ts_treated), min(ts_synthetic))
            ymax = max(max(ts_treated), max(ts_synthetic))
            plt.vlines(x=treatment_time, ymin=ymin, ymax=ymax, linestyle="dashed")
        plt.legend()
        plt.grid(grid)
        plt.show()

    def gaps_plot(self, treatment_time: Optional[int] = None, grid: bool = True):
        if self.dataprep is None:
            raise ValueError("dataprep must be set for automatic plots.")
        if self.W is None:
            raise ValueError("Fit data before plotting.")

        ts_all = self.dataprep.foo.pivot(
            index=self.dataprep.time_variable,
            columns=self.dataprep.unit_variable,
            values=self.dataprep.dependent,
        )

        ts_treated = ts_all[self.dataprep.treatment_identifier]
        ts_units = ts_all[list(self.dataprep.controls_identifier)]
        ts_synthetic = (ts_units * self.W).sum(axis=1)
        ts_gap = ts_treated - ts_synthetic

        ts_gap.plot(ylabel=self.dataprep.dependent, color="black", linewidth=1)

        plt.hlines(
            y=0, xmin=min(ts_gap.index), xmax=max(ts_gap.index), linestyle="dashed"
        )
        if treatment_time:
            ymin = min(min(ts_gap), min(ts_gap))
            ymax = max(max(ts_gap), max(ts_gap))
            plt.vlines(x=treatment_time, ymin=ymin, ymax=ymax, linestyle="dashed")
        plt.grid(grid)
        plt.show()