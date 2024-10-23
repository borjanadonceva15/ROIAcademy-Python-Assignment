# Cryptocurrency Portfolio Tracker

This project is a **Cryptocurrency Portfolio Tracker** built with **Flask-RESTx**, designed to manage users, transactions, and portfolios of cryptocurrencies. It provides functionality for user registration, authentication (with JWT tokens), and transaction management, allowing users to track the value of their cryptocurrency investments.

## Features

### User Management:
- User registration, login, and logout.
- Password hashing and validation.
- JWT-based authentication for securing user sessions.

### Transaction Management:
- Create, update, and delete transactions for buying and selling cryptocurrencies.
- Secure transactions using JWT authentication.

### Portfolio Management:
- Calculate the current value of a user's cryptocurrency portfolio.
- Fetch historical portfolio values for the last N days.
- Provide a portfolio summary including the current and purchase values of different cryptocurrencies.

---

## Technologies Used

- **Backend Framework**: Flask
- **API Framework**: Flask-RESTx
- **Database**: PostgreSQL (using SQLAlchemy for ORM)
- **Authentication**: JWT (Flask-JWT-Extended)
- **Cryptocurrency Data**: CoinGecko API for real-time and historical price data.

---

## Project Structure

The project follows a **layered architecture**:

- **Controllers**: Handle HTTP requests and map them to services.
- **Services**: Contain the business logic for managing users, transactions, and portfolios.
- **Repositories**: Interact with the database for CRUD operations.
- **DTOs**: Define the structure for input/output data.
- **Exceptions**: Custom exceptions for handling errors consistently.

---

## API Endpoints

### User Endpoints

| Method | Endpoint            | Description                         |
|--------|---------------------|-------------------------------------|
| POST   | `/user/create`       | Create a new user                   |
| POST   | `/user/login`        | Log in and receive JWT token        |
| POST   | `/user/logout`       | Log out of the session              |
| GET    | `/user/<username>`   | Get user details by username        |
| GET    | `/user/`             | Get a list of all users             |

### Transaction Endpoints

| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| GET    | `/transactions/`        | Get all transactions for the user    |
| POST   | `/transactions/`        | Add a new transaction                |
| PATCH  | `/transactions/<id>`    | Update a transaction                 |
| DELETE | `/transactions/<id>`    | Delete a transaction                 |

### Portfolio Endpoints

| Method | Endpoint                           | Description                                      |
|--------|------------------------------------|--------------------------------------------------|
| GET    | `/portfolio/value`                 | Get the current portfolio value                  |
| GET    | `/portfolio/summary`               | Get a summary of the user's portfolio            |
| GET    | `/portfolio/historical_analysis/<days>` | Get the historical value of the portfolio over N days |

---

