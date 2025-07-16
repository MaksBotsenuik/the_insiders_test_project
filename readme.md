# Location Reviews API

A Django REST Framework project for managing locations, categories, and user reviews with like/dislike functionality.

## Features

- CRUD for Locations, Categories, Addresses, and Reviews
- Many-to-many relationship between Locations and Categories
- Users can leave one review per location
- Like/Dislike system for reviews
- Filtering locations by rating and categories
- Search locations by name and description
- Pagination for all list endpoints
- Authenticated API access

## Quick Start

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd inseders_test_task
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Apply migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (optional, for admin access)

```sh
python manage.py createsuperuser
```

### 5. Run the development server

```sh
python manage.py runserver
```

## API Usage

### Authentication

All endpoints require authentication. Use session or basic authentication.

### Endpoints

- **Locations:**  
  `GET /api/v1/location/`  
  `POST /api/v1/location/`  
  Supports filtering: `?rating=4&categories=1`  
  Supports search: `?search=park`

- **Categories:**  
  `GET /api/v1/category/`  
  `POST /api/v1/category/` (admin only)

- **Reviews:**  
  `GET /api/v1/review/`  
  `POST /api/v1/review/`  
  - Only one review per user per location

- **Like/Dislike Review:**  
  `POST /api/v1/review/<id>/like/`  
  `POST /api/v1/review/<id>/dislike/`

## Example: Create a Review

```json
POST /api/v1/review/
{
  "rating": 5,
  "comment": "Great place!",
  "location": 1
}
```
*The user is set automatically from the authenticated user.*

## Filtering & Search

- Filter by rating: `/api/v1/location/?rating=4`
- Filter by category: `/api/v1/location/?categories=2`
- Search by name/description: `/api/v1/location/?search=park`

## Pagination

All list endpoints are paginated by default (10 items per page).

## Requirements

- Python 3.10+
- Django 5.x
- Django REST Framework
- django-filter
- psycopg2s

