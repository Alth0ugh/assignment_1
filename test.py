from dataset import Dataset
from word_counter import WordCounter
from probability import *
from entropy import Entropy
from scrambler import WordScrambler, TextScrambler
from n_gram import NGramModel

dataset = Dataset()
dataset.from_file("TEXTEN1.txt")
print(WordCounter.count_n_grams(dataset).most_common(3))

c = Counter([("b",),("a",),("r",),("b",)])
print(c)

p = Probability()
p.compute_probability(c)

cc = Counter([("b", "a"),("a","r"),("r","b"),("b","a"),("b","b")])
pp = Probability()
pp.compute_probability(cc)

cp = ConditionalProbability()
cp.compute_conditional_probability(pp, p)

print(p.probabilities)
print(pp.probabilities)
print(cp.probabilities)

unigram_counts = WordCounter.count_n_grams(dataset)

bigram_counts = WordCounter().count_n_grams(dataset, 2)

unigram_probabilities = Probability()
bigram_probabilities = Probability()

unigram_probabilities.compute_probability(unigram_counts)
bigram_probabilities.compute_probability(bigram_counts)

conditional_probability = ConditionalProbability()
conditional_probability.compute_conditional_probability(bigram_probabilities, unigram_probabilities)

print(Entropy.compute_entropy(conditional_probability, dataset))

dataset = Dataset()
dataset.from_list(["ahoj", "Oliver", "ako", "sa", "mas"], 0)

print(dataset.data)

scrambler = TextScrambler(0.1, dataset)
new_dataset = scrambler.scramble_text()
print(new_dataset.data)

word_scrambler = WordScrambler(0.1, dataset)
print(word_scrambler.scramble_text().data)

dataset = Dataset()
dataset.from_file("TEXTEN1.txt")

model = NGramModel(3)
model.fit(dataset, dataset)