class Rounding:
    def __init__(self):
        self.interval: float = 0.25
        self.num1: float = 4.36

    def round_numer(self) -> None:
        """
        This rounds a number to the nearest multiple of self.interval using self.interval
        """
        # Round the number to the nearest multiple of self.interval
        # Note: this is so that the last value is always a multiple of 0.25
        print(1/self.interval)

        rounded_num = round(self.num1 * 4) / 4
        print(rounded_num)

        # This is a better way to do it
        rounded_num = round(self.num1 / self.interval) * self.interval
        print(rounded_num)

        # This way doesn't work (it actually does!)
        rounded_num = round(self.num1 * (1/self.interval)) * self.interval
        print(rounded_num)

        # This is what I was doing when I was making a mistake... see the / and * in the wrong places.
        # And it's unnecessarily complicated.
        # last_value = round(last_value * (1/self.timing_interval)) / self.timing_interval




def main():
    x = Rounding()
    x.round_numer()


if __name__ == "__main__":
    main()
