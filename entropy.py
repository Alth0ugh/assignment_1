from probability import *
from dataset import Dataset
import numpy as np
from n_gram import NGramModel

class Entropy:
    @staticmethod
    def compute_entropy(conditional_probability: ConditionalProbability | NGramModel, dataset: Dataset) -> float:
        """
        Computes entropy of data using probability distribution
        conditional_probability: probability distribution for entropy computation
        dataset: the data to compute entropy on
        """
        log_sum = 0
        for i in range(len(dataset) - 1):
            log_sum += np.log2(conditional_probability[(dataset[i + 1], dataset[i])]).item()
        
        return -(1 / len(dataset)) * log_sum