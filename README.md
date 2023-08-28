## Web App Template README

![image](https://github.com/john-markowsky/Web-App-Template/assets/123923257/5567f06d-0487-41b4-a4f2-60dcc5d1e432)

### Overview:
This is a web template built using FastAPI, a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Features:

- **User Authentication**: The template includes registration and login functionality using FastAPI's dependency injection system. It uses the `passlib` library for password hashing and also provides session management.
  
- **Database Integration**: Integrated with SQLAlchemy, it provides an example of how to use the ORM to interact with databases. The template includes an example model (`UserDB`) representing users and their details.

- **Styling with Semantic UI**: The webpages are styled using Semantic UI, a development framework that helps create beautiful, responsive layouts using human-friendly HTML. Custom styles can be found in the `base.css` file.

- **Responsive Navbar**: The navigation bar is dynamic and changes based on the authentication status of the user. For authenticated users, it provides a dropdown menu with additional options.

### Getting Started:

1. **Setup**: Create a virtual environment using `python3 -m venv .env`.
2. **Install Dependencies**: Install the required packages listed in `requirements.txt`.
3. **Run**: Start the FastAPI application and navigate to the provided localhost URL in your browser.
