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

class FilmResponse(BaseModel):
    title: str
    genres: str
    overview: str
    production_countries: str
    runtime: int
    spoken_languages: str
    vote_average: float
    vote_count: int

@app.get("/api/v1/film/{film_id}")
async def get_film(
    film_id: int = Path(..., title="ID of the film", gt=0)
):
    """
    Get detailed information about a specific film.
    """
    query = """
    SELECT title, genres, overview, production_countries, 
           runtime, spoken_languages, vote_average, vote_count
    FROM movies
    WHERE movieId = %s
    """
    
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (film_id,))
                result = cur.fetchone()
                
                if not result:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Film with id {film_id} not found"
                    )
                
                return FilmResponse(
                    title=result[0],
                    genres=result[1],
                    overview=result[2],
                    production_countries=result[3],
                    runtime=result[4],
                    spoken_languages=result[5],
                    vote_average=result[6],
                    vote_count=result[7]
                )
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch film data: {str(e)}"
        )


class FilmListItem(BaseModel):
    movieId: int
    title: str
    vote_average: float
    vote_count: int

@app.get("/api/v1/films/")
async def get_films(
    films: int = Query(..., title="Number of films to return", gt=0)
):
    """
    Get a list of films with basic information.
    The number of films is specified in the query parameter 'films'.
    """
    query = """
    SELECT movieId, title, vote_average, vote_count
    FROM movies
    ORDER BY vote_count DESC
    LIMIT %s
    """
    
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (films,))
                results = cur.fetchall()
                
                return [
                    FilmListItem(
                        movieId=row[0],
                        title=row[1],
                        vote_average=row[2], 
                        vote_count=row[3]
                    ) for row in results
                ]
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch films: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
