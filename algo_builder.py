from abc import ABCMeta, abstractmethod
from copy import deepcopy


class IBuilder(metaclass=ABCMeta):
    """The Builder Interface"""
    COPY = deepcopy

    @staticmethod
    @abstractmethod
    def fib(*args, **kwargs):
        """Build fib"""

    @staticmethod
    @abstractmethod
    def grid_traveller(*args, **kwargs):
        """Build grid_traveller"""

    @staticmethod
    @abstractmethod
    def can_sum(*args, **kwargs):
        """Build can_sum"""

    @staticmethod
    @abstractmethod
    def how_sum(*args, **kwargs):
        """Build how_sum"""

    @staticmethod
    @abstractmethod
    def best_sum(*args, **kwargs):
        """Build best_sum"""

    @staticmethod
    @abstractmethod
    def can_construct(*args, **kwargs):
        """Build can_construct"""

    @staticmethod
    @abstractmethod
    def count_construct(*args, **kwargs):
        """Build count_construct"""

    @staticmethod
    @abstractmethod
    def all_construct(*args, **kwargs):
        """Build all_construct"""
