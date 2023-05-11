from abc import ABC, abstractmethod

from requests import Response


class Limiter(ABC):
    @abstractmethod
    def rate_limiter(self, response: Response) -> None:
        pass
