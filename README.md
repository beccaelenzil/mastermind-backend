# Mastermind API

This repo has the source code for the Mastermind API, created for the LinkedIn Reach Software Engineering Apprenticeship Application. The API is written in Python using the Flask framework.

~~To play the game, go to https://beccaelenzil.github.io/mastermind-frontend/~~

## Deployment

~~The Mastermind API is deployed here: https://becca-mastermind.herokuapp.com/~~. 

~~The Mastermind Web Application (the game!) that uses this API is deployed here: https://beccaelenzil.github.io/mastermind-frontend/~~
- The repo for the front-end can be found here: https://github.com/beccaelenzil/mastermind-frontend.


## Running the Server Locally [source](https://github.com/AdaGold/retro-video-store/blob/master/ada-project-docs/setup.md)

1. Fork (optional) and clone this repo. If you choose to fork the repo, make sure to include all branches.
    - Navigate to the repo on your computer
1. Check out the `local` branch.
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

    Future instructions will show `(venv) $` in front of terminal commands as a reminder that commands should be run in the terminal with an activated `venv`. 

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
        
        `(venv) $ flask db upgrade`

1. Run the server.
    
    `FLASK_ENV=development flask run`

1. Navigate to `http://127.0.0.1:5000/` in the browser. You should see the following response:

    ```{"name":"Mastermind API"}```

## Playing the Game with the Command Line Interface (CLI)

To play the game with the locally running server, we will use the provided CLI.

1. Run the CLI with the command `(venv) $ python3 cli/main.py`.

1. You may also play using the CLI and the deployed API here: [https://replit.com/@BeccaElenzil/mastermind-cli](https://replit.com/@BeccaElenzil/mastermind-cli)

1. Below is an example game run for a new logged-in user `becca`.

![CLI Game Instructions](./project-docs/cli1.png)
![CLI Game Play](./project-docs/cli2.png)

## Playing the Game with the React Web App

~~The Mastermind Web Application that uses this API can be found here: https://beccaelenzil.github.io/mastermind-frontend/.~~

You may also choose to clone this react app and run it locally. You first need to run the CLI to make sure that the database is seeded with the level information.

To run the React App with the locally running Flask server, complete the following steps:

1. Fork (optional) and clone the repo: [https://github.com/beccaelenzil/mastermind-frontend](https://github.com/beccaelenzil/mastermind-frontend)
1. Navigate into the repo and run `npm install` and `npm start`
1. Navigate to the `Constants.js` file and make the following change:
    ```js
    //const url = "https://becca-mastermind.herokuapp.com/";
    const url = "http://127.0.0.1:5000/";
    ```
1. Navigate to `http://localhost:3000/` and enjoy the 🦄s, 💚s, and 🥳s! :)

## Testing

Comprehensive unit tests can be run with the command `(venv) $ pytest`.

A code coverage report was created with the following command:

```bash
(venv) $ pytest --cov=app --cov-report html --cov-report term
```

The coverage report is available in `htmlcov/index.html`.

## Enhancements

### Levels
Players can play in easy (code length: 4, digit options: 4), standard (code length: 4, digit options: 8), or hard (code length: 6, digit options: 8) mode. These level parameters are hardcoded in the `level.py` model file. 

A future enhancement would add configurability to the level parameters. This could be achieved through additional routes that allow users to update the level parameters.

### Users

Players can choose to login and track their progress. A performance summary provides the total number of games played, the number of games won, the most recent number of games won in a row (win streak), the win percentage, and the distribution of the number of plays used on winning games.

Authentication is not implemented. You can log in with any username you like! You can log in as your friend and go on a winning streak on their behalf (or a losing streak, for that matter). But remember to play nice, or an admin might delete you ;)

**`username` vs. `email`.** 
`email` is the attribute stored in the `User` table, but the CLI and React App use the term `username` since it is not required that you use a valid email address. `email` was chosen as the attribute with Google authentication in mind.

While authentication is not implemented, the routes for Google authentication with oauth can be viewed in the `login_routes.py` on the `google-auth` branch.

### Graphics

The React app ~~[https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/)~~ translates the number sequence into fun emojis!

## Mastermind API Routes

Below, find a high-level summary of the endpoints provided by the Mastermind API.

**Plays**
| Method | URL | Request Body Example | Response Body Example| Description |
|--|--|--|--|--|
| `POST` |`/plays` |`{"game_id": null, "user_id": 1, "level": "easy", "code": "1111"}` |`{ "answer": "hidden", "code": "1111", "correct_nums": 0,"correct_pos": 0,"game_id": 1,"id": 1, "win": false}` | The first play of a game creates a new game. The id for that new game is returned in the response body. The answer is hidden until the player wins or runs out of tries. |
| `POST` |`/plays` |`{"game_id": 1, "user_id": 1, "level": "easy", "code": "1234"}` |`{ "answer": "1234", "code": "1234", "correct_nums": 4,"correct_pos": 4,"game_id": 1,"id": 2, "win": true}` | This example second play of a game is a winning play. |

**Games**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| `GET`| `/games/1`|`-`|`{"code": "hidden","id": 1, "level": "easy","level_params": {...},"plays": [{},...],"user_id": null}` | Returns details about the game with `id` `1`. The code is hidden until the game is won or the max number of guesses is used.|
| `GET`| `/games`|`-` |`[List of game dictionaries]` | Returns details about all the games in the database as a list of dictionaries. |
| `DELETE`| `/games/1`| `{"admin_key": "secret key"}` |`{"error": "must be admin to delete games"}, 400`  `{"success": f"delete game 1"}, 200` |Deletes one game with `id` `1` and associated plays. The secret key is stored in the environment variables. |
| `DELETE`| `/games`|`{"admin_key": "secret key"}` | `{"error": "must be admin to delete games"}, 400` or `{"success": "delete all games"}, 200`|Deletes all games and associated plays. The secret key is stored in the environment variables. |

**Users**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| `POST`| `/users/login`|`{"email": "becca"}` |`{}` | If there is not a user with the email passed in the request body, a new user is created. The request returns details about the logged-in user. |
| `GET`| `/users`|`-`|`[{"num games": 11,"uid": 1, "username": "becca", "wins": 1},...]`| Returns abbreviated details about all users.|
| `GET`| `/users/1`|`-`|`{games: [{game details},...], "performance summary": {}, "uid": 1, "username": "becca"`| Returns details for the user with `uid` `1`. Details include all the games played and a summary of performance. The performance summary includes guess distribution, games won, total games, win percentage, and current win streak. |
| `DELETE`| `/users/1`| `{"admin_key": "secret key"}` |`{"error": "must be admin to delete users"}, 400`  `{"success": f"delete user 1"}, 200` |Deletes one user with `uid` `1` and associated games. The secret key is stored in the environment variables. |
| `DELETE`| `/users`|`{"admin_key": "secret key"}` | `{"error": "must be admin to delete users"}, 400` or `{"success": "delete all users"}, 200`|Deletes all users and associated games. The secret key is stored in the environment variables. |

**Levels**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| `POST`| `/levels`|`-` |`{"easy":{params}, "standard":{params}, "hard":{params}}` |Seeds the database with the level parameters coded in the `levels.py` file. |
| `GET`| `/levels`|`-`|`{"easy":{params}, "standard":{params}, "hard":{params}}` |Returns the parameters for all levels. |
| `GET`| `/levels/1`|`-` |`{"name": "easy", "params": {...}` |Returns the parameters for one level with `id` `1`. |

## Thank You

I hope you enjoyed this implementation of Mastermind!
