from abc import ABC, abstractmethod


class AbstractSSE(ABC):
    @abstractmethod
    def subscribe(self):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass

    @abstractmethod
    def notify(self):
        pass
    