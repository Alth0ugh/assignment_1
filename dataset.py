PAD = "<PAD>"

class Dataset:
    """Class representing a dataset"""
    def from_list(self, arr: list, pad: int = 1):
        """
        Creates a dataset from a list
        arr: the list to create dataset from
        pad: how many times to pad in the begining
        """
        self.data = arr
        padding = ["<PAD>" for _ in range(pad)]
        self.data = padding + self.data
    
    def from_file(self, path: str, pad: int = 1):
        """
        Creates a dataset from file
        path: path to a source file
        pad: how many times to pad in the begining and at the end
        """
        with open(path, encoding="iso-8859-2") as f:
            self.data = f.readlines()
        self.data = list(map(lambda x: x.rstrip(), self.data))
        padding = ["<PAD>" for _ in range(pad)]
        self.data = padding + self.data + padding

    def __getitem__(self, key):
        return self.data[key]
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if len(self.data) <= self.n:
            raise StopIteration
        item = self.data[self.n]
        self.n += 1
        return item

    def __len__(self):
        return len(self.data)