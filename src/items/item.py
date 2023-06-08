from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def __init__(self):
        self.name = ""
