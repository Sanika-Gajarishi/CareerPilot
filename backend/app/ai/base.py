from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ):
        pass