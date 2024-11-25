from probability import *
from dataset import Dataset
import numpy as np

class Entropy:
    @staticmethod
    def compute_entropy(conditional_probability: ConditionalProbability, dataset: Dataset) -> float:
        log_sum = 0
        for i in range(len(dataset) - 1):
            log_sum += np.log2(conditional_probability[(dataset[i + 1], dataset[i])])
        
        return -(1 / len(dataset)) * log_sum