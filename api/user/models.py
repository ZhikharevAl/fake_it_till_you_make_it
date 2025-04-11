from pydantic import BaseModel, Field


class AddToFavouritesPayload(BaseModel):
    """Модель тела запроса для POST /api/user/favourites."""

    request_id: str = Field(..., min_length=1, description="ID запроса для добавления в избранное")


FavouritesListResponse = list[str]
