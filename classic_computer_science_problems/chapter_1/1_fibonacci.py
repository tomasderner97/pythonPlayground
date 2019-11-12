import functools
import logging


# logging.basicConfig(level=logging.DEBUG)


def fibonacci_recursive(n):
    """ get n-th fibonacci number by recursive calls """
    logging.debug(f"Entering fibonacci_recursive with n = {n}")

    if n <= 0:
        raise ValueError("n must be a positive number.")
    if n <= 2:
        return n - 1
    return fibonacci_recursive(n - 2) + fibonacci_recursive(n - 1)


def fibonacci_recursive_memoized(n, dct=None):
    """ get n-th fibonacci number by recursive calls, every number is calculated only once """
    logging.debug(f"Entering fibonacci_recursive_lazy with n = {n}")

    if not dct:
        dct = {
            1: 0,
            2: 1,
        }

    if n <= 0:
        raise ValueError("n must be a positive number.")

    if n not in dct:
        print(f"{n} not in dct")
        dct[n] = fibonacci_recursive_memoized(n - 1, dct) + fibonacci_recursive_memoized(n - 2, dct)

    return dct[n]


@functools.lru_cache(maxsize=None)
def fibonacci_recursive_automemoized(n):
    """ get n-th fibonacci number by recursive calls with automatic memoization """
    logging.debug(f"Entering fibonacci_recursive_automemoized with n = {n}")

    if n <= 0:
        raise ValueError("n must be a positive number.")
    if n <= 2:
        return n - 1
    return fibonacci_recursive_automemoized(n - 2) + fibonacci_recursive_automemoized(n - 1)


def fibonacci_iterative(n):
    """ get n-th fibonacci number by iteration """
    if n <= 0:
        raise ValueError("n must be a positive number.")
    if n == 1:
        return 0

    result = 1
    result_minus_1 = 0
    for i in range(2, n):
        result, result_minus_1 = result + result_minus_1, result

    return result


def fibonacci_list(n):
    """ generate list of first n Fibonacci numbers """
    if n <= 0:
        raise ValueError("n must be a positive number.")
    if n == 1:
        return [0]

    nums = [0, 1]
    for i in range(2, n):
        nums.append(nums[i-1] + nums[i-2])

    return nums


def fibonacci_generator(n):
    """ generator producing first n fibonacci numbers """
    yield 0

    if n > 0:
        yield 1

    num = 1
    previous = 0

    for i in range(2, n):
        num, previous = num + previous, num
        yield num