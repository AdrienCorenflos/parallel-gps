import gpflow
import tensorflow as tf

from pssgp.kernels.base import ContinuousDiscreteModel, SDEKernelMixin
from pssgp.kernels.matern.common import get_matern_sde


class Matern12(gpflow.kernels.Matern12, SDEKernelMixin):
    __doc__ = gpflow.kernels.Matern12.__doc__

    def __init__(self, variance=1.0, lengthscales=1.0, **kwargs):
        self._order = kwargs.pop('order', 3)
        gpflow.kernels.Matern12.__init__(self, variance, lengthscales, **kwargs)
        SDEKernelMixin.__init__(self, **kwargs)

    def get_sde(self) -> ContinuousDiscreteModel:
        F, L, H, Q = get_matern_sde(self.variance, self.lengthscales, 1)
        variance = tf.reduce_sum(self.variance)

        P_infty = tf.linalg.diag([variance])
        return ContinuousDiscreteModel(P_infty, F, L, H, Q)