from dataset import Dataset, PAD
from concurrent.futures import ThreadPoolExecutor
import random

class WordScrambler:
    def __init__(self, probability: float, dataset: Dataset):
        self.probability = probability
        self.dataset = dataset

    def __extract_characters(self, characters: set, word: str):
        for c in word:
            characters.add(c)

    def __get_characters_from_text(self) -> list:
        characters = set()
        for word in self.dataset:
            if word != PAD:
                self.__extract_characters(characters, word)

        return list(characters)

    def __scramble_word(self, word: str, vocabulary: list) -> str:
        if word == PAD:
            return word
        
        word = list(word)
        for i in range(len(word)):
            if random.random() < self.probability:
                random_character_index = random.randint(0, len(vocabulary) - 1)
                word[i] = vocabulary[random_character_index]
        return "".join(word)

    def scramble_text(self) -> Dataset:
        characters = self.__get_characters_from_text()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda word: self.__scramble_word(word, characters), self.dataset))
        new_dataset = Dataset()
        new_dataset.from_list(results, 0)
        return new_dataset
    
class TextScrambler:
    def __init__(self, probability: float, dataset: Dataset):
        self.probability = probability
        self.dataset = dataset

    def __get_vocabulary(self) -> list:
        vocabulary = set()
        for word in self.dataset:
            vocabulary.add(word)

        return list(vocabulary)
    
    def __scramble_word(self, word: str, vocabulary: list):
        if word == PAD:
            return word
        
        if random.random() < self.probability:
            new_index = random.randint(0, len(vocabulary) - 1)
            return vocabulary[new_index]
        
        return word

    def scramble_text(self) -> Dataset:
        vocabulary = self.__get_vocabulary()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda word: self.__scramble_word(word, vocabulary), self.dataset))
        new_dataset = Dataset()
        new_dataset.from_list(results, 0)
        return new_dataset