from typing import Callable, TypeVar

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def compose(a: Callable[[A], B], b: Callable[[B], C]) -> Callable[[A], C]:
    return lambda i:b(a(i))

def map_fst(m: Callable[[A], C], t: tuple[A, B]) -> tuple[C, B]:
    return (m(t[0]), t[1])
def map_snd(m: Callable[[B], C], t: tuple[A, B]) -> tuple[A, C]:
    return (t[0], m(t[1]))

def filter_fst(m: Callable[[A], bool], t: tuple[A, B]) -> Callable[[tuple[A, B]], bool]:
    return lambda t:m(t[0])
def filter_snd(m: Callable[[B], bool], t: tuple[A, B]) -> Callable[[tuple[A, B]], bool]:
    return lambda t:m(t[1])
