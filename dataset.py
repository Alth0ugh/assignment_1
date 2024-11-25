PAD = "<PAD>"

class Dataset:
    def from_list(self, arr: list, pad: int = 1):
        self.data = arr
        padding = ["<PAD>" for _ in range(pad)]
        self.data = padding + self.data + padding
    
    def from_file(self, path: str, pad: int = 1):
        with open(path) as f:
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