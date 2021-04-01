from algo_builder import IBuilder


class MemoizationBuilder(IBuilder):

    @staticmethod
    def fib(n, memo=None):
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 2:
            return 1
        memo[n] = MemoizationBuilder.fib(n-1, memo) + MemoizationBuilder.fib(n-2, memo)
        return memo[n]

    @staticmethod
    def grid_traveller(m, n, memo=None):
        if memo is None:
            memo = {}
        key = f'{m},{n}'
        if key in memo:
            return memo[key]
        if m == 1 and n == 1:
            return 1
        if m == 0 or n == 0:
            return 0
        memo[key] = MemoizationBuilder.grid_traveller(m-1, n, memo) + MemoizationBuilder.grid_traveller(m, n-1, memo)
        return memo[key]

    @staticmethod
    def can_sum(target_sum, numbers, memo=None):
        if memo is None:
            memo = {}
        if target_sum in memo:
            return memo[target_sum]
        if target_sum == 0:
            return True
        if target_sum < 0:
            return False
        for i in numbers:
            remainder = target_sum - i
            if MemoizationBuilder.can_sum(remainder, numbers, memo):
                memo[target_sum] = True
                return True
        memo[target_sum] = False
        return False

    @staticmethod
    def how_sum(target_sum, numbers, memo=None):
        if memo is None:
            memo = {}
        if target_sum in memo:
            return memo[target_sum]
        if target_sum == 0:
            return []
        if target_sum < 0:
            return None
        for i in numbers:
            remainder = target_sum - i
            remainder_result = MemoizationBuilder.how_sum(remainder, numbers, memo)
            if remainder_result is not None:
                remainder_result.append(i)
                memo[target_sum] = remainder_result
                return memo[target_sum]
        memo[target_sum] = None
        return None

    @staticmethod
    def best_sum(target_sum, numbers, memo=None):
        if memo is None:
            memo = {}
        if target_sum in memo:
            return memo[target_sum]
        if target_sum == 0:
            return []
        if target_sum < 0:
            return None
        shortest_combination = None
        for i in numbers:
            remainder = target_sum - i
            remainder_combination = MemoizationBuilder.best_sum(remainder, numbers, memo)
            if remainder_combination is not None:
                combination = MemoizationBuilder.COPY(remainder_combination)
                combination.append(i)
                if shortest_combination is None or len(combination) < len(shortest_combination):
                    shortest_combination = combination
        memo[target_sum] = shortest_combination
        return shortest_combination

    @staticmethod
    def can_construct(target, word_bank, memo=None):
        if memo is None:
            memo = {}
        if target in memo:
            return memo[target]
        if not target:
            return True
        for w in word_bank:
            if target.startswith(w):
                suffix = target[len(w):]
                if MemoizationBuilder.can_construct(suffix, word_bank, memo):
                    memo[target] = True
                    return True
        memo[target] = False
        return False

    @staticmethod
    def count_construct(target, word_bank, memo=None):
        if memo is None:
            memo = {}
        if target in memo:
            return memo[target]
        if not target:
            return 1
        total_count = 0
        for w in word_bank:
            if target.startswith(w):
                num_ways_for_rest = MemoizationBuilder.count_construct(target[len(w):], word_bank, memo)
                total_count += num_ways_for_rest
        memo[target] = total_count
        return total_count

    @staticmethod
    def all_construct(target, word_bank, memo=None):
        if memo is None:
            memo = {}
        if target in memo:
            return memo[target]
        if not target:
            return [[]]
        result = []
        for w in word_bank:
            if target.startswith(w):
                suffix = target[len(w):]
                suffix_ways = MemoizationBuilder.all_construct(suffix, word_bank, memo)
                target_ways = list(map(lambda el: [w, *el], suffix_ways))
                result.extend(target_ways)
        memo[target] = result
        return result
