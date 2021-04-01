from enum import Enum
from memo_builder import MemoizationBuilder
from tabulation_builder import TabulationBuilder
from collections.abc import Iterable
from time import perf_counter
from pprint import pformat
import six


class Result:
    """The Result"""

    def __init__(self, raw):
        self._raw = raw

    def to_dict(self):
        return {"result": pformat(self._raw)}


class Director:

    OPERATION = None

    class Helper:
        @staticmethod
        def timeit(method):
            def timed(*args, **kw):
                start = perf_counter()
                result = method(*args, **kw)
                result["execution_time"] = f"{(perf_counter() - start) * 1000} milliseconds"
                return result

            return timed

    @Helper.timeit
    def construct(self, operation, *args, **kwargs):
        return Result(self.OPERATION[operation](*args, **kwargs)).to_dict()


class MemoizationDirector(Director):
    OPERATION = {"fib": MemoizationBuilder.fib,
                 "grid_traveller": MemoizationBuilder.grid_traveller,
                 "can_sum": MemoizationBuilder.can_sum,
                 "how_sum": MemoizationBuilder.how_sum,
                 "best_sum": MemoizationBuilder.best_sum,
                 "can_construct": MemoizationBuilder.can_construct,
                 "count_construct": MemoizationBuilder.count_construct,
                 "all_construct": MemoizationBuilder.all_construct}


class TabulationDirector(Director):
    OPERATION = {"fib": TabulationBuilder.fib,
                 "grid_traveller": TabulationBuilder.grid_traveller,
                 "can_sum": TabulationBuilder.can_sum,
                 "how_sum": TabulationBuilder.how_sum,
                 "best_sum": TabulationBuilder.best_sum,
                 "can_construct": TabulationBuilder.can_construct,
                 "count_construct": TabulationBuilder.count_construct,
                 "all_construct": TabulationBuilder.all_construct}


class Execute(Enum):
    MEMOIZATION = MemoizationDirector()
    TABULATION = TabulationDirector()


if __name__ == "__main__":

    """Test launch"""

    test_data_collection = {
        "fib": (6, 7, 8, 50),
        "grid_traveller": ((1, 1), (2, 3), (3, 2), (3, 3), (18, 18)),
        "can_sum": ((7, [2, 3]), (7, [5, 3, 4, 7]), (7, [2, 4]), (8, [2, 3, 5]), (300, [7, 14])),
        "how_sum": ((7, [2, 3]), (7, [5, 3, 4, 7]), (7, [2, 4]), (8, [2, 3, 5]), (300, [7, 14])),
        "best_sum": ((7, [5, 3, 4, 7]), (8, [2, 3, 5]), (8, [1, 4, 5]), (100, [1, 2, 5, 25])),
        "can_construct": (('abcdef', ['ab', 'abc', 'cd', 'def']),
                          ('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']),
                          ('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']),
                          ('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee'])),
        "count_construct": (('purple', ['purp', 'p', 'ur', 'le', 'purpl']),
                            ('abcdef', ['ab', 'abc', 'cd', 'def']),
                            ('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']),
                            ('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']),
                            ('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef', ['e', 'ee', 'eee', 'eeee', 'eeeee', 'eeeeee'])),
        "all_construct": (('purple', ['purp', 'p', 'ur', 'le', 'purpl']),
                          ('abcdef', ['ab', 'abc', 'cd', 'def']),
                          ('skateboard', ['bo', 'rd', 'ate', 't', 'ska', 'sk', 'boar']),
                          ('enterapotentpot', ['a', 'p', 'ent', 'enter', 'ot', 'o', 't']),
                          ('aaaaaaaaaaaaaaaaaaaaaaaaaaz', ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']))
    }

    for op_num, data_set in test_data_collection.items():
        for data in data_set:
            if isinstance(data, Iterable) and not isinstance(data, six.string_types):
                print(Execute.MEMOIZATION.value.construct(op_num, *data))
            else:
                print(Execute.MEMOIZATION.value.construct(op_num, data))
