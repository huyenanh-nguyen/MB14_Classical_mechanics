from MathKit.statsengine import Statistics
import pandas as pd
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path, PurePath
from matplotlib.ticker import FormatStrFormatter

def gravity(l, g):
        """determing acceleration with this slope:
        T^2 = ((4 * pi^2)/g) * l

        Args:
            l (float): length of the pendulum -> x-value
            g (float): value that we want to find

        Returns:
            float: returns y-Value of this function -> T^2
        """

        return ((4 * np.pi ** 2) / g) * l   

def origin_fit(x, m):
            return  m * x

def noorigin_fit(x, m, c):
            return  m * x + c



class Pendulum:
    """
    Well using Jupyter Notebook is quite annoying.

    I dont want to spend to many time on this project, I will use the Excelfile as input.
    This Excelfile is already prepared for the analysis and the layout shouldn't change.
    This code is very specific for this Excelfile in this Pendulum-folder and will not work for other Excelfiles.
    But for someone who doesn't like the layout of the Excelfile, it is possible to change the code. 

    The important Parameter is the Path to the Excelfile (And all units are SI-Units)!
    """

    def __init__(self, excelpath):
        """
        Args:
            excelpath(Path): Path to my Excelfile
        """

        self.excel = excelpath


    def excel_to_df(self):
        """
        skipping enough rows, so it begins and ends on the right row where I put the table.

        Returns:
            List: List with three Dataframes -> first Item is for task 1, second Item is for the longest and shortest length of the pendulum, where 
                  we measured 10 times 10 periods and the last Item is for task 3
        """

        excel = self.excel
        task1_excelsheeet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=2).iloc[0:10,np.arange(1,3)] 
        task3a_excelsheet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=19).iloc[0:12,np.arange(1,5)] 
        task3b_excelsheet = pd.read_excel(excel, sheet_name = "Rohdaten", skiprows=36).iloc[0:12,np.arange(1,12)]

        return [task1_excelsheeet, task3a_excelsheet, task3b_excelsheet]

    ############################
    #         task 1           #
    ############################ 

    def equilibrium_period_stats(self):
        """
        Calculation the neccessary random statistical parameters for the Period at the equilibrium point.

        Returns:
            List: [Mean of Period at the equilibrium point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]
    

    def equilibrium_period_total_err(self, systematic_error):
        """calculating the total uncertainty of the period at the equilibrium point

        Args:
            systematic_error (float, value): systematic error of the offset from my instrument. In this case the last digit of the timer

        Returns:
            Float: total uncertainty of the period at the equilibrium point
        """

        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        return stats.total_uncertainty_value(systematic_error)
    

    def relative_equilibrium_error(self, systematic_error):
        excel = self.excel_to_df()[0]["T(Nullpunkt) in s"]
        stats = Statistics(excel)

        equilibrium_relative = stats.relative_total_uncertainty(systematic_error)

        return equilibrium_relative
    

    def turningpoint_period_stats(self):
        """
        Calculation the neccessary random statistical parameters for the Period at the turning point.

        Returns:
            List: [Mean of Period at the turning point, standard deviation of the mean, confidence interval of the mean]
        """

        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)

        period_mean = stats.std_mean()
        period_stddev = stats.std_dev()
        period_cov = stats.confidence_interval()

        return [period_mean, period_stddev, period_cov]
    

    def turningpoint_period_total_err(self, systematic_error):
        """calculating the total uncertainty of the period at the turning point

        Args:
            systematic_error (float, value): systematic error of the offset from my instrument. In this case the last digit of the timer

        Returns:
            Float: total uncertainty of the period at the turning point
        """

        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)

        return stats.total_uncertainty_value(systematic_error)
    

    def relative_turningpoint_err(self, systematic_error):
        """percantage error (like T ± 0.1%)

        Args:
            systematic_error (float): offset of the instrument
        """
        
        excel = self.excel_to_df()[0]["T(Umkehrpunkt) in s"]
        stats = Statistics(excel)
        turning_stdev = stats.relative_total_uncertainty(systematic_error)

        return turning_stdev
    





    ############################
    #         task 3           #
    ############################

    # measuring 5 periods for 12 different pendulum length



    # pendulum length:

    def stringlength_error(self, guessingerror):
        """
        Args:
            guessingerror (float): how accurate can we measure the length? (systematic error, limit by the measuring tool)

        Returns:
            List: measuring unceartainty for each length
        """

        accu_class = self.excel_to_df()[2]["∆liEG in mm"]

        error_string = [np.sqrt((accu_class[i]**2) + (guessingerror**2)) for i in range(len(accu_class))]
        return error_string
    

    def total_length_error(self, guessingerror, guess_zero_length):
        """summed up the total error of the length

        Args:
            guessingerror (float): systematic error of the measuring tool
            guess_zero_length (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                        have to measure till the center of mass from our object -> we cant exactly tell where it is. -> this deviation)

        Returns:
            List: total error of the length
        """

        error_string = self.stringlength_error(guessingerror)

        total_error = [np.sqrt(((error_string[i])**2 + (guess_zero_length)**2)) for i in range(len(error_string))]
        return total_error
    



    # period:

    def delta_timer(self):
         
         fiveperiod = self.excel_to_df()[1]["τ1 = 5 Ti in s"]

         deltatimer = [(fiveperiod[i] * 0.5 + 10)/1000 for i in range(len(fiveperiod))]
         return deltatimer
    

    def total_error_period(self, systematicerror_time, reaction_error):
        """Uncertainty of the period (which was measured 5 times)

        Args:
            systematicerror_time (float): In this experiment we only measure the period 5 times for each length. That is not enough data
                                          to use the common statistical calculation.
                                          In this case we have to guess the uncertainty of the time -> the last digit of my timer.
                                          mostly it's 10 ms
            reaction_error (float): there will be always some reaction delay by stopping the time. this is round about 150 - 200 ms

        Returns:
            List: total error of the period that was measured 5 times
        """
        delta_time = self.delta_timer()

        total_period_error = [np.sqrt((delta_time[i]**2) + (systematicerror_time**2) + (reaction_error**2)) for i in range(len(delta_time))]
        
        return total_period_error
        

    def singleperiod(self):
        """
        for further analysis we only need the avaerage Period time for each length -> BEcause we measured 5 times the time, we have to 
        divide this time by 5.

        Returns:
            List: List with the time period
        """
        
        fiveperiod = self.excel_to_df()[1]["τ1 = 5 Ti in s"]
        oneperiod = [(fiveperiod[i]/5) for i in range(len(fiveperiod))] # in this script we only measure 5 times of the period

        return oneperiod
    

    def singleperiod_error(self, systematicerror_time, reaction_error):
        """
        Error of the single averaged Period

        Args:
            systematicerror_time (float): In this experiment we only measure the period 5 times for each length. That is not enough data
                                          to use the common statistical calculation.
                                          In this case we have to guess the uncertainty of the time -> the last digit of my timer.
                                          mostly it's 10 ms
            reaction_error (float): there will be always some reaction delay by stopping the time. this is round about 150 - 200 ms

        Returns:
            List: Errors for each time of the different length
        """

        fiveperiod_error = self.total_error_period(systematicerror_time, reaction_error)

        singleperiod_error = [fiveperiod_error[i] / 5 for i in range(len(fiveperiod_error))]

        return singleperiod_error
    


########


    def square_period(self):
        """
        y-value is the period square

        Returns:
            List: period square -> for the slope
        """
        
        period = self.singleperiod()

        square_period = [period[i]**2 for i in range(len(period))]

        return square_period
    

    def square_period_error(self, guessing_timeerror, reaction_error):
        period = self.singleperiod()
        period_err = self.singleperiod_error(guessing_timeerror, reaction_error)

        square_period_error = [(2 * period[i]) * period_err[i] for i in range(len(period))]

        return square_period_error
    

    #############
    #   Plot    #
    #############


    def fit_points(self):
        """
        linear regression of the data

        Args:
            length (array or list): length of pendulum

        Returns:
            List: [g-value, covariance of g , R_square]
        """

        square_period = self.square_period()

        length = self.excel_to_df()[1]["li in m"]    

        popt, pcov = curve_fit(gravity, length, square_period) 
        residuals = square_period - gravity(np.asarray(length), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((square_period - np.mean(square_period)) ** 2)

        r_square = 1 - (ss_res / ss_total)

        return popt, pcov, r_square
    

    def fit_origin(self):
        """
        forcing the slope to go through the origin.

        Returns:
            List: [slope, covariance, R_square]
        """

        square_period = self.square_period()
        length = self.excel_to_df()[2]["li,ges in m"] 
        
        popt, pcov = curve_fit(origin_fit, length, square_period)
        residuals = square_period - origin_fit(np.asarray(length), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((square_period - np.mean(square_period)) ** 2)

        r_square = 1 - (ss_res / ss_total)

        return popt, pcov, r_square
    
    def gravity(self):
        """from the slope calculating the eroor and the error of it
        -> because the pendulum swings back and forth within a small angle, we can assume that the pendulum swings with a harmonic motion.
        which leads to the following equation:
        T = 2 * pi * sqrt(l/g)
        -> square it and we get:
        T^2 = ((4 * pi^2)/g) * l
        with this form we get a linear regression and can calculate the slope.
        from the slope we can calculate the acceleration g:
        g = (4 * pi^2) / slope

        Returns:
            List: gravity, error of the gravity
        """
            
        slope = self.fit_origin()[0]
        slope_err = self.fit_origin()[1]

        g = (4 * np.pi**2) / slope
        g_err = sqrt((((4 * np.pi**2)/slope ** 2) * slope_err)**2)

        return g, g_err
    


    def plot_slope(self, guesslengtherror, guess_zero_error, guessing_timeerror, reaction_error):
        """
        forcing the plot to go through the origin.
        with the slope we can calculate the gravity acceleration g

        Args:
            guessingerror (float): systematic error of the measuring tool
            guess_zero_length (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                        have to measure up to the center of mass from our object -> we cant exactly tell where it is. -> this deviation)
            guessing_timeerror (float): In this experiment we only measure the period 5 times for each length. That is not enough data
                                        to use the common statistical calculation.
                                        In this case we have to guess the uncertainty of the time -> the last digit of my timer.
                                        mostly it's 10 ms
            reaction_error (float): there will be always some reaction delay by stopping the time. this is round about 150 - 200 ms


        Returns:
            plot: with the functionname, R_Square, g with error
        """

        grav = self.fit_points()
        square_period = np.array(self.square_period())
        square_period_err = np.array(self.square_period_error(guessing_timeerror, reaction_error))
        length =  np.array(self.excel_to_df()[2]["li,ges in m"])

        length_error = np.array(self.total_length_error(guesslengtherror, guess_zero_error))
        digit = 3

        labeltext = "y = " + str(np.round(float(grav[0]), digit)) + u" \u00B1 " + str(np.round(float(grav[1]), digit)) + "\n $R^{2}$ = " + str(np.round(grav[2], digit))

        fig = plt.figure()
        ax = fig.add_subplot()
        plt.scatter(x = length, y = square_period, marker = ".")
        plt.plot(length, gravity(length, grav[0]), label = labeltext)
       
        plt.errorbar(length ,square_period, xerr= length_error, yerr = square_period_err, fmt=' ', capsize=3, color = "slategrey")

        ax.secondary_xaxis('top').tick_params(axis = 'x', direction = 'out')
        ax.secondary_yaxis('right').tick_params(axis = 'y', direction = 'out')
        plt.legend(loc = 'upper left')
        plt.xlabel("l in m")
        plt.ylabel("$T^{2}$ in $s^{2}$")
        plt.show()

        return None
    

    def plot_through_origin(self,guesslengtherror, guess_zero_error, guessing_timeerror, reaction_error):
        """without taking the full length of the pendulum into account. -> forcing the slope to go through the origin.

        Args:
            guessingerror (float): systematic error of the measuring tool
            guess_zero_length (float): deviation of the pendulum from the center of mass (If we measure the length of the pendulum, we
                                        have to measure up to the center of mass from our object -> we cant exactly tell where it is. -> this deviation)
            guessing_timeerror (float): In this experiment we only measure the period 5 times for each length. That is not enough data
                                        to use the common statistical calculation.
                                        In this case we have to guess the uncertainty of the time -> the last digit of my timer.
                                        mostly it's 10 ms
            reaction_error (float): there will be always some reaction delay by stopping the time. this is round about 150 - 200 ms


        Returns:
            Plot: plot with the slope going through the origin
        """

        slope = self.fit_origin()
        square_period = np.array(self.square_period())
        square_period_err = np.array(self.square_period_error(guessing_timeerror, reaction_error))
        length =  np.array(self.excel_to_df()[2]["li,ges in m"])

        grav_results = self.gravity()

        length_error = np.array(self.total_length_error(guesslengtherror, guess_zero_error))
        digit = 3

        labeltext = "y(l) = " + str(np.round(float(slope[0]), digit)) + u" l \u00B1 " + str(np.round(float(slope[1]), digit)) + "\n$R^{2}$ = " + str(np.round(slope[2], digit)) +  "\n$g$ = " + str(np.round(grav_results[0][0], digit)) + u" \u00B1 " + str(np.round(grav_results[1][0][0], digit)) + " $m/s^{2}$"
        
        x_value = np.linspace(0, 2.1, 5)

        fig = plt.figure()
        ax = fig.add_subplot()
        plt.scatter(x = length, y = square_period, marker = ".")
        # plt.plot(length, origin_fit(length, slope[0]), label = labeltext)
        plt.plot(x_value, origin_fit(x_value, slope[0]), label = labeltext, color = "tab:orange")
       
        plt.errorbar(length ,square_period, xerr= length_error, yerr = square_period_err, fmt=' ', capsize=3, color = "dimgrey")
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) # set y-axis to 2 decimal places
        
        ax.yaxis.set_ticks(np.arange(0, 10, 1))
        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=0)
        # ax.secondary_xaxis('top').tick_params(axis = 'x', direction = 'out')
        # ax.secondary_yaxis('right').tick_params(axis = 'y', direction = 'out')
        # ax.spines['right'].set_visible(False)  # remove the top and right spines
        plt.legend(loc = 'upper left')
        plt.xlabel("l in m", fontsize=12)
        plt.ylabel("$T^{2}$ in $s^{2}$", fontsize=12)
        plt.show()

        return None
    


    def getting_l0(self):
        """
        plotting the data without forcing them to go through the origin.
        x_values are the length of the pendulum and the y_values are the squared period.
        with the optimized function, we can get a better gravity accerelation results, because we are keeping the errors like rotations ect in account.
        that is why we need the value l0, to make further calculation.

        Returns:
            List: [g, delta_g, l0, delta_l0]
        """

        square_period = self.square_period()
        length = self.excel_to_df()[1]["li in m"] 
        
        popt, pcov = curve_fit(noorigin_fit, length, square_period)

        g = (4 * (np.pi ** 2))/ popt[0]
        delta_g = sqrt((((4 *( np.pi**2))/popt[0] ** 2) * pcov[0][0])**2)

        l0 = (g / (4 * (np.pi **2))) * popt[1]
        delta_l0 = sqrt( ((1 / (4 * np.pi**2)) * delta_g)**2 * ((1 / (4 * np.pi ** 2)) *  pcov[1])**2 )
        residuals = square_period - noorigin_fit(np.asarray(length), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((square_period - np.mean(square_period)) ** 2)
        r_square = 1 - (ss_res / ss_total)
        return [g, delta_g, l0, delta_l0, r_square, popt, pcov]
    

    def fit_optimized(self):
        """
        optimized version to get the gravity acceleration by calculating l0 (the error of the length of the pendulum).


        Returns:
            List: g with its error
        """
        l0 = self.getting_l0()[2]
        
        l = self.excel_to_df()[1]["li in m"]
        square_period = self.square_period()

        def optimum_g(l, g):
            return ((4 * np.pi ** 2) / g) * (l + l0)

        popt, pcov = curve_fit(optimum_g, l, square_period)
        residuals = square_period - optimum_g(np.asarray(l), *popt)
        ss_res = np.sum(residuals ** 2)
        ss_total = np.sum((square_period - np.mean(square_period)) ** 2)
        r_square = 1 - (ss_res / ss_total)
        return popt, pcov, r_square
    

    def plot_withintercept(self, guessing_timeerror, reaction_error):
        grav = self.getting_l0()
        square_period = np.array(self.square_period())
        square_period_err = np.array(self.square_period_error(guessing_timeerror, reaction_error))
        length =  np.array(self.excel_to_df()[1]["li in m"])

        length_error = np.array(self.excel_to_df()[2]["∆liEG in mm"])

        digit = 3

        labeltext = "y(l) = (" + str(round(float(grav[5][0]), digit)) + u" \u00B1 " + str(round(float(grav[6][0][0]), digit)) + ") l  + (" + str(round(float(grav[5][1]), digit)) + u" \u00B1 " + str(round(float(grav[6][0][0]), digit)) + ")" + "\n$R^{2}$ = " + str(round(grav[4], digit)) +  "\n$g$ = " + '{:.3f}'.format(round(grav[0], digit)) + u" \u00B1 " + str(round(grav[1], digit)) + " $m/s^{2}$" +  "\n$l_0$ = " + str(round(grav[2], digit)) + u" \u00B1 " + str(np.format_float_scientific(grav[3][0],precision=3)) + " $m$"
        x_value = np.linspace(0, 2.1, 5)
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.scatter(x = length, y = square_period, marker = ".")
        # plt.plot(length, origin_fit(length, slope[0]), label = labeltext)
        plt.plot(x_value, noorigin_fit(x_value, grav[5][0], grav[5][1]), label = labeltext, color = "tab:orange")
       
        plt.errorbar(length ,square_period, xerr= length_error, yerr = square_period_err, fmt=' ', capsize=3, color = "dimgrey")
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) # set y-axis to 2 decimal places
        
        ax.yaxis.set_ticks(np.arange(0, 10, 1))
        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=0)
        # ax.secondary_xaxis('top').tick_params(axis = 'x', direction = 'out')
        # ax.secondary_yaxis('right').tick_params(axis = 'y', direction = 'out')
        # ax.spines['right'].set_visible(False)  # remove the top and right spines
        plt.legend(loc = 'upper left')
        plt.xlabel("l in m", fontsize=12)
        plt.ylabel("$T^{2}$ in $s^{2}$", fontsize=12)
        plt.show()

        return None


excelpath = PurePath(str(Path.cwd()) + "/F3_Fadenpendel-Maksims.xlsx")
oma = Pendulum(excelpath)


oma.plot_through_origin(0.001, 0.0012, 0.01, 0.1)
# print(oma.getting_l0())
print(oma.fit_optimized())
# print(oma.gravity())