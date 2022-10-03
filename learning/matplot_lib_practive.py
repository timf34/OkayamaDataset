import matplotlib.pyplot as plt
import numpy as np

# This file will be for practice plotitng some purely numerical data


class PlottingPractice:
    def __init__(self):
        self.x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
        self.all_ones = np.ones(10)
        self.all_zeros = np.zeros(10)
        self.one_to_ten = np.arange(1, 11)

    def plot_sin(self):
        print("self.x: ", self.x)
        print("np.sin(self.x): ", np.sin(self.x))
        plt.plot(self.x, np.sin(self.x))  # Plot the sine of each x point
        plt.show()

    def plot_linear_long(self):
        print("self.x: ", self.x)
        plt.plot(self.x, self.x)
        plt.show()

    def plot_linear_short(self):
        print("self.one_to_ten: ", self.one_to_ten)
        plt.plot(self.one_to_ten, self.one_to_ten)
        plt.show()

    def plot_x_axis_ones(self):
        print("self.all_ones: ", self.all_ones)
        print("self.one_to_ten: ", self.one_to_ten)
        plt.plot(self.all_ones, self.one_to_ten)
        plt.show()


def main():
    plot = PlottingPractice()
    # plot.plot_linear_short()
    plot.plot_x_axis_ones()


if __name__ == '__main__':
    main()


