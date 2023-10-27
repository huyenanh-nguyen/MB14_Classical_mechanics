from pendulum import Pendulum
import numpy as np
from pathlib import Path, PurePath

class Resultexport(Pendulum):

    def equilibrium_vs_turning(self, systematic_error_time, digit):
        
        mean_equi = self.equilibrium_period_stats()[0]
        stdev_equi = self.equilibrium_period_stats()[1]
        cov_equi = self.equilibrium_period_stats()[2]
        totalerr_equi = np.round(self.equilibrium_period_total_err(systematic_error_time), digit)
        relativerr_equi = np.round(self.relative_equilibrium_error(systematic_error_time))

        mean_turn = self.turningpoint_period_stats()[0]
        stdev_turn = self.turningpoint_period_stats()[1]
        cov_turn = self.turningpoint_period_stats()[2]
        totalerr_turn = np.round(self.turningpoint_period_total_err(systematic_error_time), digit)
        relativerr_turn = np.round(self.relative_turningpoint_err(systematic_error_time), digit)

        line1 = "Nullpunkt-Werte"
        line2 = "mean: " + str(mean_equi) + " s"
        line3 = "stdev: " + str(stdev_equi) + " s"
        line4 = "cov: " + str(cov_equi) + " s"
        line5 = " "
        line6 = "Mittelwert mit absoluter Messunsicherheit: " + str(np.round(mean_equi, digit)) + u" \u00B1 " + str(np.round(totalerr_equi, digit)) + " s"
        line7 = "Mittelwert mit relativer Messunsicherheit: " + str(np.round(mean_equi, digit)) + u" \u00B1 " + str(np.round(relativerr_equi, digit)) + " s"
        line8 = " "
        line9 = " "
        line10 = "Umkehrpunkt-Werte"
        line11 = "mean: " + str(mean_turn) + " s"
        line12 = "stdev: " + str(stdev_turn) + " s"
        line13 = "cov: " + str(cov_turn) + " s"
        line14 = " "
        line15 = "Mittelwert mit absoluter Messunsicherheit: " + str(np.round(mean_turn, digit)) + u" \u00B1 " + str(np.round(totalerr_turn, digit)) + " s"
        line16 = "Mittelwert mit relativer Messunsicherheit: " + str(np.round(mean_turn, digit)) + u" \u00B1 " + str(np.round(relativerr_turn, digit)) + " s"
        line17 = " "
        line18 = " "

        text = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17, line18]

        return text


    def length_period(self, systematic_error_length, masspointerror):
        """_summary_

        Args:
            systematic_error_length (float): _description_
            masspointerror (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                    have to measure till the center of mass from our object -> we cant exactly tell where it is. -> this deviation)
        """

        delta_string = self.stringlength_error(systematic_error_length)
        total_length_error = self.total_length_error(systematic_error_length,  masspointerror)

        



        line1 = "Gesamtlänge des Pendels mit der Flasche und dieses ∆l_iEG habe ich nicht mit reingenommen."


excel = PurePath(str(Path.cwd()) + "/F3_Fadenpendel.xlsx")
oma = Resultexport(excel)

print(oma.equilibrium_vs_turning(0.001, 4))
