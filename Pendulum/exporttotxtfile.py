from pendulum import Pendulum
import numpy as np
from pathlib import Path, PurePath
from itertools import chain
import pandas as pd
import openpyxl

class Resultexport(Pendulum):
    """
    This class is used to export the results of the experiment to a txt file.
    The exportlanguage is german (The task was in german and all the variables are in german, which makes it easier to understand the export better for my group members.
    it would be too complicated to translate all the variables to english)

    Args:
        Pendulum (class): all the mathmatics formular for this experiment
    """

    def equilibrium_vs_turning(self, systematic_error_time, digit):
        
        mean_equi = self.equilibrium_period_stats()[0]
        stdev_equi = self.equilibrium_period_stats()[1]
        cov_equi = self.equilibrium_period_stats()[2]
        totalerr_equi = np.round(self.equilibrium_period_total_err(systematic_error_time), digit)
        relativerr_equi = np.round(self.relative_equilibrium_error(systematic_error_time), digit)

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
        line7 = "Mittelwert mit relativer Messunsicherheit: " + str(np.round(mean_equi, digit)) + u" (1 \u00B1  " + str(np.round(relativerr_equi, digit)) + " %) s"
        line8 = " "
        line9 = " "
        line10 = "Umkehrpunkt-Werte"
        line11 = "mean: " + str(mean_turn) + " s"
        line12 = "stdev: " + str(stdev_turn) + " s"
        line13 = "cov: " + str(cov_turn) + " s"
        line14 = " "
        line15 = "Mittelwert mit absoluter Messunsicherheit: " + str(np.round(mean_turn, digit)) + u" \u00B1 " + str(np.round(totalerr_turn, digit)) + " s"
        line16 = "Mittelwert mit relativer Messunsicherheit: " + str(np.round(mean_turn, digit)) + u" (1 \u00B1 " + str(np.round(relativerr_turn, digit)) + " %) s"
        line17 = " "
        line18 = " "

        text = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17, line18]

        return text


    def length_period(self, systematic_error_length, masspointerror, systematicerror_time, reaction_error, digit):
        """This function returns the results of the experiment.

        Args:
            systematic_error_length (float): systematic error of the measuring tool
            masspointerror (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                    have to measure till the center of mass from our object -> we cant exactly tell where it is. -> this deviation)
        """

        delta_string = np.round(self.stringlength_error(systematic_error_length), digit)
        total_length_error = np.round(self.total_length_error(systematic_error_length,  masspointerror), digit) 
        deltaclock = np.round(self.delta_timer(), digit)
        deltatime = np.round(self.total_error_period(systematicerror_time, reaction_error), digit)
        singleperiod = np.round(self.singleperiod(), digit)
        deltasingleperiod = np.round(self.singleperiod_error(systematicerror_time, reaction_error), digit)
        squareperiod = np.round(self.square_period(), digit)
        squareperiod_err = np.round(self.square_period_error(systematicerror_time, reaction_error), digit)


        line0 = "_________________________________________________________________________________________"
        line1 = "Gesamtlänge des Pendels mit der Flasche und dieses ∆l_iEG habe ich nicht in diesen File mit reingetan."
        line2 = "∆li(Faden) = " + str(delta_string) + " in m"
        line3 = "∆li(ges) = " + str(total_length_error) + " in m"
        line4 = " "
        line5 = "Ah! Für ∆τ(stat) = 10 ms und ∆τ(react) = 150 ms habe ich gesetzt. obwohl vllt wenn man  ∆τ(react) = 200 ms setzt, vllt ist man näher an den wahren Wert ran"
        line6 = " "
        line7 = "∆τi(Uhr) = " + str(deltaclock) + " in s"
        line8 = "∆τi(ges) = " + str(deltatime) + " in s"
        line9 = " "
        line10 = "Ti = " + str(singleperiod) + " in s"
        line11 = "∆Ti = " + str(deltasingleperiod) + " in s"
        line12 = "yi = " + str(squareperiod) + " in s^2"
        line13 = "∆yi = " + str(squareperiod_err) + " in s^2"
        line14 = " "

        text = [line0, " ", line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, " ", line12, line13, line14, "die Plots kommens seperat als Bilder rein", " "]

        return text
    
    
    def flattenlist(self, array):
        return list(chain.from_iterable(array))
    
    
    def export(self, systematic_error_length, masspointerror, systematic_error_time, reaction_error, digit):
        """All results are exported to a txt file.

        Args:
            systematic_error_time (float): In this experiment we only measure the period 5 times for each length. That is not enough data
                                          to use the common statistical calculation.
                                          In this case we have to guess the uncertainty of the time -> the last digit of my timer.
                                          mostly it's 10 ms
            systematic_error_length (float): systematic error of the measuring tool
            masspointerror (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                    have to measure till the center of mass from our object -> we cant exactly tell where it is. -> this deviation)
            reaction_error (float): reaction time of the person who measures the time
            digit (int): number of digits after the comma

        Returns:
            None: The results are exported to a txt file.
        """
        text = [self.equilibrium_vs_turning(systematic_error_time, digit), self.length_period(systematic_error_length, masspointerror, systematic_error_time, reaction_error, digit)]
        flat_text = self.flattenlist(text)

       
        with open('F3_Results_Maksims.txt', 'w') as datei:
            for line in flat_text:
                datei.write(line + '\n')    # add a newline character

        return None
    

    def result3_to_df(self,systematic_error_length, masspointerror, systematicerror_time, reaction_error, digit):
        totallength = [(self.excel_to_df()[1]["li in m"][i] + self.excel_to_df()[1]["l0,schätz in m"][i]) for i in range(len(self.excel_to_df()[1]["li in m"]))]
        eg_length = [(0.4/1000 * totallength[i] + 0.6 / 1000) for i in range(len(totallength))]
        delta_string = np.round(self.stringlength_error(systematic_error_length), digit)
        total_length_error = np.round(self.total_length_error(systematic_error_length,  masspointerror), digit) 
        deltaclock = np.round(self.delta_timer(), digit)
        deltatime = np.round(self.total_error_period(systematicerror_time, reaction_error), digit)
        singleperiod = np.round(self.singleperiod(), digit)
        deltasingleperiod = np.round(self.singleperiod_error(systematicerror_time, reaction_error), digit)
        squareperiod = np.round(self.square_period(), digit)
        squareperiod_err = np.round(self.square_period_error(systematicerror_time, reaction_error), digit)

        dataframe = pd.DataFrame(
            {
             "li,ges in m" : totallength,
             "∆liEG in mm" : eg_length,
             "∆li(Faden)": delta_string,
             "∆li(ges)" : total_length_error,
             "∆τi(Uhr)" : deltaclock,
             "∆τi(ges)" : deltatime,
             "Ti" : singleperiod,
             "∆Ti" : deltasingleperiod,
             "yi" : squareperiod,
             "∆yi" : squareperiod_err
            }
        )

        export_excel = dataframe.to_excel(r'Results_Fadenpendel_Oscar.xlsx', index = None, header=True)

        return dataframe



excel = PurePath(str(Path.cwd()) + "/F3_Fadenpendel_oscar.xlsx")
oma = Resultexport(excel)

print(oma.result3_to_df(0.0005,0.001, 0.01, 0.15, 5))
