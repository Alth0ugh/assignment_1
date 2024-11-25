from collections import Counter

class Probability:
    def __init__(self):
        self.probabilities = {}

    def compute_probability(self, counts: Counter):
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
        return self.probabilities[key]
    
class ConditionalProbability:
    def __init__(self):
        self.probabilities = {}

    def compute_conditional_probability(self, union_probabilities: Probability | Counter, single_probabilities: Probability | Counter):
        for *i, j in union_probabilities:
            self.probabilities[(j,) + tuple(i)] = union_probabilities[tuple(i) + (j,)] / single_probabilities[tuple(i)]

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
        return self.probabilities[key]