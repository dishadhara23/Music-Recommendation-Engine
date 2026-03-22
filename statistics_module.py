
import numpy as np
from scipy import stats


class BasicStats:
#first will define the structure for stats operation
    def compute_mean(self, data):
        raise NotImplementedError("Method not implemented")

class MusicStatistics(BasicStats):
  
    def compute_mean(self, data):
        try:
# To calculate average we need to check for empty data to avoid crashing
            if not data or len(data) == 0: 
                raise ValueError("Data list is empty")
            return np.mean(data)
        except Exception as e:
            print(f"Error calculating mean: {e}")
            return 0.0

    def compute_mode(self, data):
# once average is done will calculate the most common value in the dataset        
        try:
            if not data or len(data) == 0: 
                raise ValueError("Data list is empty")
            return stats.mode(data, keepdims=True)[0][0]
        except Exception as e:
            print(f"Error calculating mode: {e}")
            return 0.0

    def compute_variance(self, data):
# variance will show how spread out the data points are from the mean and the mode
        try:
            if not data or len(data) == 0: 
                raise ValueError("Data list is empty")
            return np.var(data)
        except Exception as e:
            print(f"Error calculating variance: {e}")
            return 0.0

    def compute_std(self, data):
        try:
            if not data or len(data) == 0: 
                raise ValueError("Data list is empty")
            return np.std(data)
        except Exception as e:
            print(f"Error calculating std dev: {e}")
            return 0.0

# Default statistics engine instance
stats_engine = MusicStatistics()
