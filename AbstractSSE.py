from abc import ABC, abstractmethod


class AbstractSSE(ABC):
    @abstractmethod
    def subscribe(self, observer):
        pass

    @abstractmethod
    def unsubscribe(self, observer):
        pass

    @abstractmethod
    def notify(self, data):
        pass
    