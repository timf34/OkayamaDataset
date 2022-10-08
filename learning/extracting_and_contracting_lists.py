import scipy
import numpy as np
import pandas as pd


# Note that I will need to plot whatever the results are of interpolating the larger array... to ensure that they are
# actually correct.



class ExtendArrayUsingInterpolation:
    def __init__(self):
        self.test_array = np.array([0, 1, 2, 3, 3.5, 5])
        self.test_list = [0, 1, 2, 3, 3.5, 5]
        self.test_dataframe = pd.DataFrame(self.test_array)

    def extend_array_using_interpolation(self, array: np.array, length_of_new_array: int) -> None:
        """
        This extends an array using interpolation
        """
        x = np.arange(len(array))
        f = scipy.interpolate.interp1d(x, array)
        x_new = np.linspace(0, len(array) - 1, length_of_new_array)
        print("extended array using np.linspace and scipy.interploate: \n", f(x_new))

        # Now lets use np.interp
        x_new = np.linspace(0, len(array) - 1, length_of_new_array)
        print(x_new)
        print("extended array using np.linspace and np.interp: \n", np.interp(x_new, x, array))

        # Now lets use test_list
        x_new = np.linspace(0, len(self.test_list) - 1, length_of_new_array)
        print("extended list array using np.linspace and np.interp: \n", np.interp(x_new, x, self.test_list))  # Yep it works on lists grand.

        # Now lets contract the array into a smaller one
        x_new = np.linspace(0, len(array) - 1, len(array) - 1)
        print("contracted array using np.linspace and np.interp: \n", np.interp(x_new, x, array))

        # Now lets try to use pandas.interpolate to extend the test_dataframe
        # Note: this won't work as the number of indices (length) of the dataframe is the same as the number of values
        # And its just not working rn... but it doens't matter, I'll be using one of the methods above.
        # print("extended dataframe using pandas.interpolate: \n", self.test_dataframe.interpolate("quadratic"))



def main() -> None:
    """
    This is the main function
    """
    x = ExtendArrayUsingInterpolation()
    x.extend_array_using_interpolation(x.test_array, 10)


if __name__ == "__main__":
    main()
