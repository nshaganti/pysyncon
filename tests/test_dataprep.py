import unittest
import numpy as np
import pandas as pd

from pyaugsynth import Dataprep


class TestDataprep(unittest.TestCase):
    def setUp(self):
        self.foo = pd.DataFrame(
            {
                "time": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
                "name": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                "dependent": np.random.random(12),
                "predictor1": np.random.random(12),
                "predictor2": np.random.random(12),
            }
        )
        self.predictors = ["predictor1"]
        self.predictors_op = "mean"
        self.time_predictors_prior = [2, 3]
        self.dependent = "dependent"
        self.unit_variable = "name"
        self.time_variable = "time"
        self.treatment_identifier = 1
        self.controls_identifier = [2, 3]
        self.time_optimize_ssr = [1, 2, 3]
        self.special_predictors = [
            ("predictor1", [2], "mean"),
            ("predictor2", [1, 2], "median"),
            ("predictor2", [1, 2], "std"),
        ]

    def test_foo(self):
        kwargs = {
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(TypeError, Dataprep, foo=np.array([]), **kwargs)
        self.assertRaises(TypeError, Dataprep, foo=list(), **kwargs)
        self.assertRaises(TypeError, Dataprep, foo=tuple(), **kwargs)

    def test_predictors(self):
        kwargs = {
            "foo": self.foo,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(TypeError, Dataprep, predictors="badarg", **kwargs)
        self.assertRaises(ValueError, Dataprep, predictors=["badval"], **kwargs)

    def test_predictors_op(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(ValueError, Dataprep, predictors_op="badval", **kwargs)

    def test_time_predictors_prior(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(TypeError, Dataprep, time_predictors_prior="badarg", **kwargs)

    def test_dependent(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(ValueError, Dataprep, dependent="badval", **kwargs)

    def test_unit_variable(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(ValueError, Dataprep, unit_variable="badval", **kwargs)

    def test_time_variable(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(ValueError, Dataprep, time_variable="badval", **kwargs)

    def test_treatment_identifier(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(ValueError, Dataprep, treatment_identifier="badval", **kwargs)

    def test_controls_identifier(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(TypeError, Dataprep, controls_identifier="badarg", **kwargs)
        self.assertRaises(ValueError, Dataprep, controls_identifier=[1], **kwargs)
        self.assertRaises(ValueError, Dataprep, controls_identifier=[5], **kwargs)

    def test_time_optimize_ssr(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "special_predictors": self.special_predictors,
        }

        self.assertRaises(TypeError, Dataprep, time_optimize_ssr="badarg", **kwargs)

    def test_special_predictors(self):
        kwargs = {
            "foo": self.foo,
            "predictors": self.predictors,
            "predictors_op": self.predictors_op,
            "time_predictors_prior": self.time_predictors_prior,
            "dependent": self.dependent,
            "unit_variable": self.unit_variable,
            "time_variable": self.time_variable,
            "treatment_identifier": self.treatment_identifier,
            "controls_identifier": self.controls_identifier,
            "time_optimize_ssr": self.time_optimize_ssr,
        }

        self.assertRaises(TypeError, Dataprep, special_predictors="badarg", **kwargs)
        self.assertRaises(
            ValueError, Dataprep, special_predictors=[("predictor1", [1])], **kwargs
        )
        self.assertRaises(
            TypeError,
            Dataprep,
            special_predictors=[("predictor1", "badarg", "mean")],
            **kwargs
        )
        self.assertRaises(
            ValueError,
            Dataprep,
            special_predictors=[("predictor1", [1], "badval")],
            **kwargs
        )