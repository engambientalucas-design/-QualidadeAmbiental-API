from datetime import date

from fastapi import HTTPException, status


def validate_date_range(data_inicio: date | None, data_fim: date | None) -> None:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )
