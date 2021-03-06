from dataclasses import dataclass
from itertools import chain, permutations, product
from numbers import Real
from os.path import dirname, join
from queue import PriorityQueue
from string import ascii_letters, ascii_uppercase
from typing import Callable, Generator, Generic, Mapping, TypeVar


def mutate(word: str) -> Generator[str, None, None]:
    mutation_funcs = [scrambles, additions, deletions, swaps]
    mutation_iter = chain.from_iterable(m(word) for m in mutation_funcs)
    for w in mutation_iter:
        yield w


def backtrack_path(
    start: str, end: str, history: Mapping[str, str]
) -> Generator[str, None, None]:
    word = start
    while word != end:
        yield word
        word = history[word]
    yield end
    return


def find_path(
    start: str, end: str, mutator: Callable = mutate
) -> Generator[str, None, None]:
    start = start.upper()
    end = end.upper()
    words = get_words()
    history: Mapping[str, str] = {}
    pq: PriorityQueue[Priority[str]] = PriorityQueue()
    pq.put(Priority(0, end))
    while not pq.empty():
        current = pq.get()
        word = current.value
        for mut in mutator(word):
            if mut == start:
                history[mut] = word
                return backtrack_path(start, end, history)
            elif mut not in words:
                continue
            elif mut not in history:
                heur = 1 + current.priority
                pq.put(Priority(heur, mut))
                history[mut] = word
    raise Exception(f"Could not find path from {start} to {end}")


def find_doublet_path(start: str, end: str) -> Generator[str, None, None]:
    return find_path(start, end)


def find_swap_path(start: str, end: str) -> Generator[str, None, None]:
    return find_path(start, end, mutator=swaps)


T = TypeVar("T")


@dataclass(frozen=True, order=True)
class Priority(Generic[T]):
    priority: Real
    value: T


def additions(word: str) -> Generator[str, None, None]:
    for i, c in product(range(len(word) + 1), ascii_uppercase):
        yield word[:i] + c + word[i:]


def deletions(word: str) -> Generator[str, None, None]:
    for i in range(len(word)):
        yield word[:i] + word[i + 1 :]


def swaps(word: str) -> Generator[str, None, None]:
    for i, c in product(range(len(word)), ascii_uppercase):
        yield word[:i] + c + word[i + 1 :]


def scrambles(word: str) -> Generator[str, None, None]:
    for w in permutations(word):
        yield w


def get_words() -> set[str]:
    with open(join(dirname(__file__), "words.txt")) as f:
        return {
            w.upper()
            for w in f.read().split("\n")
            if all(c in ascii_letters for c in w)
        }
