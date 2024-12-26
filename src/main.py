from settings import DB_CONFIG
from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, condecimal
from datetime import datetime
import psycopg2
import uvicorn


# def connect_to_db():
#     try:
#         with psycopg2.connect(**DB_CONFIG) as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT version();")
#                 print("Connected to:", cur.fetchone())
      
#     except psycopg2.Error as e:
#         print("Ошибка подключения к базе данных:", e)

# if __name__ == "__main__":
#     connect_to_db()



app = FastAPI()

# Database configuration


class RatingInput(BaseModel):
    user_id: int
    rating: condecimal(max_digits=2, decimal_places=1)  # Rating with one decimal place

@app.post("/api/v1/film/{film_id}/add_rating")
async def add_rating(
    film_id: int = Path(..., title="ID of the film", gt=0),
    rating_data: RatingInput = Body(...),
):
    """
    Add a rating for a film.
    """
    query = """
    INSERT INTO rating (userId, movieId, rating)
    VALUES (%s, %s, %s)
    """
    
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        rating_data.user_id,
                        film_id,
                        float(rating_data.rating),
                    )
                )
        return {"message": "Rating added successfully"}
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Rating already exists for this user and film")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add rating: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
