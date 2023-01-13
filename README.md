# Mastermind Backend

This repo has the source code for the Mastermind API, created for the LinkedIn Reach Software Engineering Apprenticeship Application. The API is written in Python using the Flask framework.

## Web App

The Mastermind API is deployed here: [https://becca-mastermind.herokuapp.com/](https://becca-mastermind.herokuapp.com/). 

The Mastermind Web Application that uses this API can be found here: [https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/) ([repo](https://github.com/beccaelenzil/mastermind-frontend)).


## Running the Server Locally [source](https://github.com/AdaGold/retro-video-store/blob/master/ada-project-docs/setup.md)

1. Fork (optional) and clone this repo. If you choose to fork the repo, make sure to include all branches.
    - Navigate to the repo on your computer
1. Checkout the `local` branch.
1. Create and activate a virtual environment
    
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ # You're in activated virtual environment!
    ```
    - Install dependencies:
    ```bash
    (venv) $ pip install -r requirements.txt
    ```
1. Set up the development and test databases
    - Create two Postgres databases:
        - A development database named `mastermind_development_db`
        - A test database named `mastermind_test_db`

    - Create a file named `.env` in the project root directory.

        - Create two environment variables that will hold your database URLs.

            - `SQLALCHEMY_DATABASE_URI` to hold the path to your development database
            - `SQLALCHEMY_TEST_DATABASE_URI` to hold the path to your development database

        - Your `.env` may look like this:

        ```bash
        SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind_development_db

        SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind_test_db
        ```

        - Add the following environment variables to use the random API, run the CLI, and create a secret admin key.
        
        ```bash
        RANDOM_URL=http://www.random.org/integers
        API_URL=http://127.0.0.1:5000/
        SECRET_KEY=*REPLACE WITH RANDOM STRING*
        ```

    - Apply migrations to your database.
        `flask db upgrade`.

1. Run the server.
    `FLASK_ENV=development flask run`

1. Navigate to `http://127.0.0.1:5000/` in the browser. You should see the following response:

    ```{"name":"Mastermind API"}```

## Playing the Game with the Command Line Interface (CLI)

To play the game with the locally running server, we will use the provided CLI.

1. Run the CLI with the command `python3 cli/main.py`.

1. Below is an example game run for a new logged in user `becca`.

![CLI Game Instructions](./project-docs/cli1.png)
![CLI Game Play](./project-docs/cli2.png)

## Playing the Game with the React Web App

The Mastermind Web Application that uses this API can be found here: [https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/) (https://github.com/beccaelenzil/mastermind-frontend).

You may also choose to clone this react app and run it locally. You first need to run the CLI to make sure that the database is seeded with the levels information.

To run the React App with the locally running Flask server, complete the following steps:

1. Fork (optional) and clone the repo: [https://github.com/beccaelenzil/mastermind-frontend](https://github.com/beccaelenzil/mastermind-frontend)
1. Navigate into the repo and run `npm install` and `npm start`
1. Navigate to the `Constants.js` file and make the following change:
    ```js
    //const url = "https://becca-mastermind.herokuapp.com/";
    const url = "http://127.0.0.1:5000/";
    ```
1. Navigate to `http://localhost:3000/` and enjoy the 🦄s, 💚s, and 🥳s ! :)

## Mastermind API Routes

**Plays**
| Method | URL | Request Body Example | Response Body Example| Description |
|--|--|--|--|--|
| `POST` |`/plays` |`{game_id: 1, "level": "easy", "user_id": 1}` | | |

**Games**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| `GET`| `/games`| | | |
| `GET`| `/games/1`| | | |
| `DELETE`| `/games`| | | |
| `DELETE`| `/games/1`| | | |

**Users**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
|--|--|--|--|--|
| `GET`| `/users/login`|`{"email": "becca"}` | | |
| `GET`| `/users`| | | |
| `GET`| `/users/1`| | | |
| `DELETE`| `/users`| | | |
| `DELETE`| `/users/1`| | | |

**Levels**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| `POST`| `/levels`| | | |
| `GET`| `/levels`| | | |
| `GET`| `/levels/1`| | | |

## Enhancements

### Levels
Playes can play in easy (code length: 4, digit options: 4), standard (code length: 4, digit options: 8), or hard (code length: 6, digit options: 8) mode. These level parameters are hardcoded in the `level.py` model file. 

A future enhancement would add configurability to the level parameters. This could be achieved through additional routes that allow users to update the level paramters.

### Users

Players can choose to login and track their progress. A performance summary provides total number of games played, number of games won, the most recent number of games won in a row (win streak), the win percentage, and the distribution of the number of plays used on winning games.

Authentication is not fully implemented. The routes for Google authentication with oauth can be viewed in the `login_routes.py` on the `google-auth` branch.

### Graphics

The React app [https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/) translates the number sequence into fun emojis!

## Thank You

I hope you enjoyed this implementation of Mastermind !