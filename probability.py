from collections import Counter

class Probability:
    """Class representing a probability distribution"""
    def __init__(self):
        self.probabilities = {}

    def compute_probability(self, counts: Counter):
        """Computes the probability distribution using counted elementary events"""
        all_sum = sum(counts.values())
        for i in counts:
            self.probabilities[i] = counts[i] / all_sum

    def __iter__(self):
        self.n = 0
        self.iterate_array = list(self.probabilities.keys())
        return self
    
    def __next__(self):
        if len(self.iterate_array) <= self.n:
            raise StopIteration
        item = self.iterate_array[self.n]
        self.n += 1
        return item

    def __getitem__(self, key):
        if key not in self.probabilities:
            return 0
        return self.probabilities[key]
    
class UniformProbability:
    """Class representing a uniform probability distribution"""
    def __init__(self, n: int):
        self.probability = 1 / n

    def __getitem__(self, key):
        return self.probability
    
class ConditionalProbability:
    """Class representing conditional probability distribution"""
    def __init__(self):
        self.probabilities = {}
    def compute_conditional_probability(self, intersection_probabilities: Probability | Counter, single_probabilities: Probability | Counter, vocabulary_size: int = None):
        self.intersection_probabilities = intersection_probabilities
        self.single_probabilities = single_probabilities
        self.vocabulary_size = vocabulary_size

    # def compute_conditional_probability(self, intersection_probabilities: Probability | Counter, single_probabilities: Probability | Counter):
    #     """
    #     Computes the conditional probability distribution
    #     intersection_probabilities: the probabilities of an intersection
    #     single_probabilities: the probabilities of the conditioning event
    #     """
    #     for *i, j in intersection_probabilities:
    #         self.probabilities[(j,) + tuple(i)] = intersection_probabilities[tuple(i) + (j,)] / single_probabilities[tuple(i)]

    def __iter__(self):
        self.n = 0
        self.iterate_array = list(self.probabilities.keys())
        return self
    
    def __next__(self):
        if len(self.iterate_array) <= self.n:
            raise StopIteration
        item = self.iterate_array[self.n]
        self.n += 1
        return item

    def __getitem__(self, key):
        old = list(key)
        word = old.pop(0)
        history = tuple(old)

        if self.single_probabilities[history] > 0 and self.intersection_probabilities[history + (word,)] == 0:
            return 0
        elif self.single_probabilities[history] == 0 and self.intersection_probabilities[history + (word,)] == 0:
            if self.vocabulary_size is None:
                return 0
            return 1 / self.vocabulary_size
        else:
            return self.intersection_probabilities[history + (word,)] / self.single_probabilities[history]

        # if key not in self.probabilities:
        #     return 0
        # return self.probabilities[key]