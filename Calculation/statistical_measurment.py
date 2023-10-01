import numpy as np
import pandas as pd

class Statistics:
    """
    Some common used statistical measures for an array-like data.
    It contains a few function like:

        std_mean() : calculate the mean of the data
        std_dev() : calculate the standard deviation of all the data without keeping the degree of freedom in count
        std_dev_mean() : is something that was asked in the task -> shows how random the errors are(?)
                       ∆x_Stat = s_m (s_m: standard deviation of the mean)
    """

    def __init__(self, valueset):
        """
        Args:
            valueset (list or array): list or array-like data
        """
        self.value_set = valueset


    def std_mean(self):
        """
        Args:
            value_set (list or array): one dimensional set of values

        Returns:
            int: sum of the values divided by the number of the values. 
        """

        return sum(self.value_set) / len(self.value_set)  # sum is a function, that sums up all the elements in the list


    def std_dev(self):
        """calculate the standard deviation of the data. (how disperse are the data in relation to the mean)
        Args:
            value_set (list or array): one dimensional set of values

        Returns:
            int: return a single integer 
        """

        mean = self.std_mean()
        difference = []

        for i in range(len(self.value_set)):

            difference.append(self.value_set[i] - mean)   # appending the difference of the value from mean
        
        std_dev = np.sqrt(sum(np.square(difference))/ (len(self.value_set) - 1))

        return std_dev


    def std_dev_mean(self):
        """actually.. I dont really know the purpose of this.. but i guess the standard deviation is divided by the
        root of the number of values

        Args:
            value_set (list or array): one dimensional set of values

        Returns:
            int: return how random the errors are. 
        """
        std_dev = self.std_dev()

        return std_dev / np.sqrt(len(self.value_set))
