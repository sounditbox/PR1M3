from typing import Callable, List, Tuple, Union

from requests import get

from main import func

num: int = 42
num = str(num)
print(num)

print(get('https://api.chucknorris.io/jokes/random').json()['value'])


def my_func(a: int, b: int) -> int:
    return a + b


def my_func2(numbers: Union[List[int], Tuple[int, ...]]) -> int:
    """Принимает коллекцию и выводит сумму её элементов"""
    return sum(numbers)


def my_dec(func: Callable) -> Callable:
    return 42


print(my_func2([1, 2, 3, 4, "5"]))
print(my_func2((1, 2, 3)))
