import matplotlib.pyplot as plt

# Will handle plotting for Simulator objects
class Plotter():
    def __init__(self, data) -> None:
        self.data = data
    
    # Plotting
    def show_plots_overlapping(self):
        """
        Show overlapping plots of timepoints
        """
        if self.data is None:
            print("Data is not defined, please call generate_data() first")