from dataset import Dataset
from probability import *
from word_counter import WordCounter

class NGramModel:
    """n-gram model"""

    def __init__(self, n: int):
        """
        n - maximum n-grams to use
        """
        self.n = n
        self.lambdas = [1/(self.n + 1) for _ in range(self.n + 1)]

    def __getitem__(self, key):
        new_key = list(key)
        word = new_key.pop()
        history = tuple(new_key)
        return self.predict(word, history)
       
    def predict(self, word: str, history: tuple) -> float:
        """Runs the prediction of the model and returns the probability of a word given its history"""
        result = 0
        for lmbda, probability in zip(self.lambdas[::-1], self.probabilities[::-1]):
            result += lmbda * probability[(word,) + history]
            new_history = list(history)
            if len(new_history) > 0:
                new_history.pop(0)
            history = tuple(new_history)
        return result
    
    def __fit_probabilities(self, train_data: Dataset, vocabulary: list):
        """Fits the probabilities and conditional probabilities used by the model"""
        word_counters = [WordCounter().count_n_grams(train_data, i) for i in range(1, self.n + 1)]
        probabilities = [ConditionalProbability() for _ in range(1, len(word_counters))]

        for i in range(len(probabilities)):
            probabilities[i].compute_conditional_probability(word_counters[i + 1], word_counters[i], len(vocabulary))

        probabilities.insert(0, Probability())
        probabilities[0].compute_probability(word_counters[0])

        probabilities.insert(0, UniformProbability(len(vocabulary)))

        self.probabilities = probabilities

    def __fit_lambdas(self, heldout_data: Dataset) -> float:
        """Fits lambdas using EM algorithm"""
        expected_counts = [0 for _ in range(len(self.lambdas))]
        for i in range(len(heldout_data) - self.n):
            history = ()
            for j in range(self.n - 1):
                history += (heldout_data[i + j],)
            word = heldout_data[i + self.n - 1]
            prediction = self.predict(word, history)
            for i in range(len(self.lambdas) - 1, -1, -1):
                expected_counts[i] += (self.lambdas[i] * self.probabilities[i][(word,) + history]) / prediction
                new_history = list(history)
                if len(new_history) > 0:
                    new_history.pop(0)
                history = tuple(new_history)
        expected_counts_sum = sum(expected_counts)
        difference = 0
        for i in range(len(self.lambdas)):
            difference = max(difference, abs((expected_counts[i] / expected_counts_sum) - self.lambdas[i]))
            self.lambdas[i] = expected_counts[i] / expected_counts_sum

        return difference

    def increase_lambda(self, lambda_index: int, amount: float):
        """
        Encreases lambda a proportionally decreases the rest of lambdas
        lambda_index: the index of lambda to be increased
        amount: the percentage of the difference between 1.0 and lambda
        """
        lambda_difference = (1.0 - self.lambdas[lambda_index]) * amount
        self.lambdas[lambda_index] += lambda_difference

        lambda_sum = 0

        for i in range(len(self.lambdas)):
            if i == lambda_index:
                continue
            lambda_sum += self.lambdas[i]

        one_part_difference = lambda_difference / lambda_sum
        for i in range(len(self.lambdas)):
            if i == lambda_index:
                continue
            self.lambdas[i] -= one_part_difference * self.lambdas[i]

    def decrease_lambda(self, lambda_index: int, amount: float):
        """
        Decreases lambda a proportionally increases the rest of lambdas
        lambda_index: the index of lambda to be decreased
        amount: the percentage of the original lambda value
        """
        lambda_difference = self.lambdas[lambda_index] - (self.lambdas[lambda_index] * amount)
        self.lambdas[lambda_index] *= amount

        lambda_sum = 0

        for i in range(len(self.lambdas)):
            if i == lambda_index:
                continue
            lambda_sum += self.lambdas[i]

        one_part_difference = lambda_difference / lambda_sum
        for i in range(len(self.lambdas)):
            if i == lambda_index:
                continue
            self.lambdas[i] += one_part_difference * self.lambdas[i]

    
    def fit(self, train_data: Dataset, heldout_data: Dataset, vocabulary: list, stopping_condition: float):
        """
        Fits the n-gram model
        train_data: train data to estimate the probabilities from
        heldout_data: the data that is used to find lambda coefficients
        vocabulary: the vocabulary of the dataset
        stopping_condition: the minimum threshold to perform another lambda update
        """
        self.__fit_probabilities(train_data, vocabulary)
        difference = 1.
        iterations = 0
        while difference > stopping_condition:
            print(f"Training iteration {iterations}")
            difference = self.__fit_lambdas(heldout_data)
            iterations += 1