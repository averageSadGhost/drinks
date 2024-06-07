# Drinks App

This Django project allows users to manage and search for drinks.

## Features

- **User Authentication**: Users can sign up, log in, and log out.
- **Token-based Authentication**: Authentication is handled using Bearer tokens.
- **Drink Management**: Users can create, view, update, and delete drinks.
- **Search Functionality**: Users can search for drinks by title or description.

## Technologies Used

- **Django**: Python web framework used for backend development.
- **Django REST Framework**: Toolkit for building Web APIs with Django.
- **SQLite**: Default database management system used to store drink data.
- **JWT (JSON Web Tokens)**: Bearer tokens are used for user authentication.
- **Python 3.12**: Programming language used for backend development.
  
## Setup Instructions

1. Clone the repository.
2. Install the necessary dependencies using pip.
3. Apply database migrations using `python manage.py migrate`.
4. Run the development server using `python manage.py runserver`.

## Usage

1. Register a new account or log in with existing credentials.
2. Use the provided API endpoints to manage drinks and perform searches.
3. Access the `/api/drinks/` endpoint to view a list of drinks, create new drinks, or search for drinks by title or description.
4. Use Bearer tokens for authentication by including the token in the Authorization header of your requests.

## Contributors

- [Mohamed Ali](https://github.com/averageSadGhost)

Feel free to contribute by submitting bug fixes or enhancements through pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
