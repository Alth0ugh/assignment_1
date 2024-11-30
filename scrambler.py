from dataset import Dataset, PAD
from concurrent.futures import ThreadPoolExecutor
import random

class WordScrambler:
    """Class used for scrabling characters inside a word"""
    def __init__(self, probability: float, dataset: Dataset):
        self.probability = probability
        self.dataset = dataset

    def __extract_characters(self, characters: set, word: str):
        """
        Extracts all characters from a words
        characters: an output set of characters
        word: word from wich we extract characters
        """
        for c in word:
            characters.add(c)

    def __get_characters_from_text(self) -> list:
        """Extracts all unique characters present in a text"""
        characters = set()
        for word in self.dataset:
            if word != PAD:
                self.__extract_characters(characters, word)

        return list(characters)

    def __scramble_word(self, word: str, vocabulary: list) -> str:
        """
        Scrambles a word - with given probability map each character in the word to a random character present in the text
        word: the word to be scrambled
        vocabulary: a list of characters present in the text
        """
        if word == PAD:
            return word
        
        word = list(word)
        for i in range(len(word)):
            if random.random() < self.probability:
                random_character_index = random.randint(0, len(vocabulary) - 1)
                word[i] = vocabulary[random_character_index]
        return "".join(word)

    def scramble_text(self) -> Dataset:
        """Scrables the whole dataset and returns scrabled dataset"""
        characters = self.__get_characters_from_text()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda word: self.__scramble_word(word, characters), self.dataset))
        new_dataset = Dataset()
        new_dataset.from_list(results, 0)
        return new_dataset
    
class TextScrambler:
    """Class for scrambling words in dataset"""
    def __init__(self, probability: float, dataset: Dataset):
        self.probability = probability
        self.dataset = dataset

    def __get_vocabulary(self) -> list:
        """Returns a list of all unique words present in the dataset"""
        vocabulary = set()
        for word in self.dataset:
            vocabulary.add(word)

        return list(vocabulary)
    
    def __scramble_word(self, word: str, vocabulary: list):
        """
        Scrambles the word with given probability by mapping the word to a random word present in the dataset
        word: word to be scrambled
        vocabulary: list of unique words present in the dataset
        """
        if word == PAD:
            return word
        
        if random.random() < self.probability:
            new_index = random.randint(0, len(vocabulary) - 1)
            return vocabulary[new_index]
        
        return word

    def scramble_text(self) -> Dataset:
        """Scrambles all words with a given probability by mapping the word to a random word present in the dataset"""
        vocabulary = self.__get_vocabulary()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda word: self.__scramble_word(word, vocabulary), self.dataset))
        new_dataset = Dataset()
        new_dataset.from_list(results, 0)
        return new_dataset