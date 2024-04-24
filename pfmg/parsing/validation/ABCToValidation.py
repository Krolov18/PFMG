from abc import abstractmethod


class ABCToValidation[T]:
    @abstractmethod
    def to_validation(self) -> T:
        """TODO : Write some doc."""
