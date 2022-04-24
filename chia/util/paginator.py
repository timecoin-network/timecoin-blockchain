import dataclasses
from math import ceil
from typing import Sequence, Tuple


class EmptyPageSizesError(Exception):
    def __init__(self) -> None:
        super().__init__("page_sizes can't be empty.")


class InvalidPageSizeError(Exception):
    def __init__(self, page_size: int) -> None:
        super().__init__(f"Invalid page size {page_size}. Available sizes: {Paginator.page_sizes}")


class PageOutOfBoundsError(Exception):
    def __init__(self, page_size: int, max_page_size: int) -> None:
        super().__init__(f"Page {page_size} out of bounds. Available pages: 1-{max_page_size}")


@dataclasses.dataclass
class Paginator:
    _source: Sequence[object]
    _page_size: int
    _page_sizes: Tuple[int, ...] = (5, 10, 25, 50, 100)

    def __post_init__(self) -> None:
        if len(self._page_sizes) == 0:
            raise EmptyPageSizesError()
        if self._page_size not in self._page_sizes:
            raise InvalidPageSizeError(self._page_size)

    def page_size(self) -> int:
        return self._page_size

    def page_sizes(self) -> Tuple[int, ...]:
        return self._page_sizes

    def page_count(self) -> int:
        return max(1, ceil(len(self._source) / self._page_size))

    def get_page(self, page: int) -> Sequence[object]:
        if page <= 0 or page > self.page_count():
            raise PageOutOfBoundsError(page, self.page_count())
        offset = (page - 1) * self._page_size
        return self._source[offset : offset + self._page_size]
