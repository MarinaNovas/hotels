from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description='Номер страницы (>=1)')]
    per_page: Annotated[int, Query(12, ge=1, le=12, description='Элементов на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]
