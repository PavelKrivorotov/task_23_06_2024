from fastapi import Query


class ListMemesFilter:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=5, ge=1, le=20)
    ) -> None:
    
        self._page = page
        self._page_size = page_size

    @property
    def limit(self) -> int:
        return self._page_size
    
    @property
    def offset(self) -> int:
        return self._page_size * (self._page - 1)

