from algo_builder import IBuilder


class TabulationBuilder(IBuilder):

    @staticmethod
    def fib(n):
        table = [0] * (n + 2)
        table[1] = 1
        for i in range(n):
            table[i + 1] += table[i]
            table[i + 2] += table[i]
        return table[n]

    @staticmethod
    def grid_traveller(m, n):
        table = [TabulationBuilder.COPY([0] * (n + 1)) for _ in range(m + 1)]
        table[1][1] = 1
        for i in range(m + 1):
            for j in range(n + 1):
                current = table[i][j]
                if j + 1 <= n:
                    table[i][j + 1] += current
                if i + 1 <= m:
                    table[i + 1][j] += current
        return table[m][n]

    @staticmethod
    def can_sum(target_sum, numbers):
        table = [False] * (target_sum + max(numbers))
        table[0] = True
        for i in range(target_sum):
            if table[i]:
                for n in numbers:
                    table[i + n] = True
        return table[target_sum]

    @staticmethod
    def how_sum(target_sum, numbers):
        table = [None] * (target_sum + max(numbers))
        table[0] = []
        for i in range(target_sum):
            if table[i] is not None:
                for num in numbers:
                    if len(table) >= i + num:
                        table[i + num] = [*table[i], num]
        return table[target_sum]

    @staticmethod
    def best_sum(target_sum, numbers):
        table = [None] * (target_sum + max(numbers))
        table[0] = []
        for i in range(target_sum):
            if table[i] is not None:
                for num in numbers:
                    combination = [*table[i], num]
                    if table[i + num] is None or len(table[i + num]) > len(combination):
                        table[i + num] = combination
        return table[target_sum]

    @staticmethod
    def can_construct(target, word_bank):
        table = [False] * (len(target) + max(len(w) for w in word_bank))
        table[0] = True
        for i in range(len(target)):
            if table[i]:
                for w in word_bank:
                    if target[i:i+len(w)] == w:
                        table[i+len(w)] = True
        return table[len(target)]

    @staticmethod
    def count_construct(target, word_bank):
        table = [0] * (len(target) + max(len(w) for w in word_bank))
        table[0] = 1
        for i in range(len(target)):
            for w in word_bank:
                if target[i:i+len(w)] == w:
                    table[i+len(w)] += table[i]
        return table[len(target)]

    @staticmethod
    def all_construct(target, word_bank):
        table = [TabulationBuilder.COPY([]) for _ in range(len(target) + max(len(w) for w in word_bank))]
        table[0] = [[]]
        for i in range(len(target)):
            for w in word_bank:
                if target[i:i + len(w)] == w:
                    new_combinations = [[*sub_list, w] for sub_list in table[i]]
                    table[i + len(w)].extend(new_combinations)
        return table[len(target)]
