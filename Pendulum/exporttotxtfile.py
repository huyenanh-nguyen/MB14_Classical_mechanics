from pendulum import Pendulum
import numpy as np

class Resultexport(Pendulum):

    def equilibrium_vs_turning(self, systematic_error, digit):
        
        mean_equi = self.equilibrium_period_stats()[0]
        stdev_equi = self.equilibrium_period_stats()[1]
        cov_equi = self.equilibrium_period_stats()[2]
        totalerr_equi = np.round(self.equilibrium_period_total_err(systematic_error), digit)
        relativerr_equi = np.round(self.relative_equilibrium_error(systematic_error))

        mean_turn = self.turningpoint_period_stats()[0]
        stdev_turn = self.turningpoint_period_stats()[1]
        cov_equi = self.turningpoint_period_stats()[2]
        totalerr_turn = np.round(self.turningpoint_period_total_err(systematic_error), digit)
        relativerr_turn = np.round(self.relative_turningpoint_err(systematic_error, digit))

        




