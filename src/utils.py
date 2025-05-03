from typing import Callable, TypeVar

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def compose(a: Callable[A, B], b: Callable[B, C]) -> Callable[A, C]:
    return lambda i:b(a(i))

def map_fst(m: Callable[A, C], t: tuple[A, B]) -> tuple[C, B]:
    return (m(t[0]), t[1])
def map_snd(m: Callable[B, C], t: tuple[A, B]) -> tuple[A, C]:
    return (t[0], m(t[1]))
