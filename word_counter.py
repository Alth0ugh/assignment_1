from collections import Counter
from dataset import Dataset

class WordCounter:
    @staticmethod
    def count_n_grams(data: Dataset, n: int = 1) -> Counter:
        counter = Counter()
        for i in range(len(data) - (n - 1)):
            n_gram = ()
            for j in range(n):
                n_gram += (data[i+j],)
            counter.update([n_gram])
        return counter
            