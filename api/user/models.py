from pydantic import BaseModel, Field


class AddToFavouritesPayload(BaseModel):
    """Модель тела запроса для POST /api/user/favourites."""

    request_id: str = Field(
        ..., min_length=1, alias="requestId", description="ID запроса для добавления в избранное"
    )

    model_config = {
        "populate_by_name": True,
    }


FavouritesListResponse = list[str]
