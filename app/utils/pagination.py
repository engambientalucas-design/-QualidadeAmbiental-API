from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    pagina: int = Field(default=1, ge=1)
    tamanho_pagina: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.pagina - 1) * self.tamanho_pagina


def pagination_metadata(page: int, page_size: int, total: int) -> dict:
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
    }
