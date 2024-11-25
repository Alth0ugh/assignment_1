from dataset import Dataset
from probability import *
from word_counter import WordCounter
from tqdm import tqdm

class NGramModel:
    def __init__(self, n: int):
        self.n = n
        self.lambdas = [1/(self.n + 1) for _ in range(self.n + 1)]
    
    def predict(self, word: str, history: tuple) -> float:
        result = 0
        for lmbda, probability in zip(self.lambdas[::-1], self.probabilities[::-1]):
            result += lmbda * probability[(word,) + history]
            new_history = list(history)
            if len(new_history) > 0:
                new_history.pop(0)
            history = tuple(new_history)
        return result
    
    def __get_vocabulary(self, dataset: Dataset) -> list:
        vocabulary = set()
        for word in dataset:
            vocabulary.add(word)

        return list(vocabulary)
    
    def __fit_probabilities(self, train_data: Dataset):
        word_counters = [WordCounter().count_n_grams(train_data, i) for i in range(1, self.n + 1)]
        probabilities = [ConditionalProbability() for _ in range(1, len(word_counters))]

        for i in range(len(probabilities)):
            probabilities[i].compute_conditional_probability(word_counters[i + 1], word_counters[i])

        probabilities.insert(0, Probability())
        probabilities[0].compute_probability(word_counters[0])

        uniform_dataset = Dataset()
        uniform_dataset.from_list(self.__get_vocabulary(train_data), 0)
        uniform_counter = WordCounter().count_n_grams(uniform_dataset)

        probabilities.insert(0, Probability())
        probabilities[0].compute_probability(uniform_counter)

        self.probabilities = probabilities

    def __fit_lambdas(self, heldout_data: Dataset):
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
        for i in range(len(self.lambdas)):
            self.lambdas[i] = expected_counts[i] / expected_counts_sum
    
    def fit(self, train_data: Dataset, heldout_data: Dataset):
        self.__fit_probabilities(train_data)
        for _ in tqdm(range(10)):
            self.__fit_lambdas(heldout_data)
            print(self.lambdas)
