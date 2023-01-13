# Mastermind Backend

This repo has the source code for the Mastermind API, created for the LinkedIn Reach Software Engineering Apprenticeship Application. The API is written in Python using the Flask framework.

## Web App

The Mastermind API is deployed here: [https://becca-mastermind.herokuapp.com/](https://becca-mastermind.herokuapp.com/). 

The Mastermind Web Application that uses this API can be found here: [https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/) ([repo](https://github.com/beccaelenzil/mastermind-frontend)).


## Running the Server Locally [source](https://github.com/AdaGold/retro-video-store/blob/master/ada-project-docs/setup.md)

1. Fork (optional) and this repo. If you choose to fork the repo, make sure to include all branches.
    - Navigate to the repo on your computer
1. Checkout the `local` branch.
1. Create and activate a virtual environment
    -
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ # You're in activated virtual environment!
    ```
    - Install dependencies:
    ```bash
    (venv) $ pip install -r requirements.txt
    ```
1. Setting Up Development and Test Databases
    - Create two Postgres databases:
        - A development database named `mastermind_development_db`
        - A test database named `mastermind_test_db`

    - Create a file named `.env` in the project root directory.

        - Create two environment variables that will hold your database URLs.
        1. `SQLALCHEMY_DATABASE_URI` to hold the path to your development database
        1. `SQLALCHEMY_TEST_DATABASE_URI` to hold the path to your development database

        - Your `.env` may look like this:

        ```
        SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind_development_db

        SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind_test_db
        ```

        - Add the following environment variables to use the random API, run the CLI, and create a secret admin key.
        ```
        RANDOM_URL=http://www.random.org/integers
        API_URL=http://127.0.0.1:5000/
        SECRET_KEY=*REPLACE WITH RANDOM STRING*
        ```

    - To apply the migrations to your database run the command `flask db upgrade`.

1. Run the server using the command `FLASK_ENV=development flask run`

1. Navigate to `http://127.0.0.1:5000/`. You should see the following response:
    ```{"name":"Mastermind API"}```

## Playing the Game with the Command Line Interface (CLI)

To play the game with the locally running server, we will use the provided CLI.

1. Run the CLI with the command `python3 cli/main.py`.

1. Below is an example game run for a new logged in user `becca`.

![CLI Game Instructions](./project-docs/cli1.png)
![CLI Game Play](./project-docs/cli2.png)

## Playing the Game with the React Web App

The Mastermind Web Application that uses this API can be found here: [https://beccaelenzil.github.io/mastermind-frontend/](https://beccaelenzil.github.io/mastermind-frontend/) ([repo](https://github.com/beccaelenzil/mastermind-frontend)).

You may also choose to clone this react app and run it locally. You first need to run the CLI to make sure that the database is seeded with the levels infomration.

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

Below the 

**Games**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| | | | | |

**Plays**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| | | | | |

**Users**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| | | | | |

**Levels**
| Method | URL | Request Body | Response Body | Description |
|--|--|--|--|--|
| | | | | |


## Enhancements

### Levels

- Add a configurable “difficulty level” and adjust the number of numbers that are used
- Draw all of graphical components, add animations and sounds
- Change numbers into colored pegs, shapes, animals, etc
- Keep track of scores
- Add a timer for the entire game, or each guess attempts
- Anything else that you come up with to make the game more fun/interesting!

Submission
Please make sure your project contains a README.md. This README should explain how an
interviewer could run your code, document your thought process and/or code structure, and
describe any creative extensions attempted or implemented. There is no prescribed format for
the README, but it should be clear and unambiguous in listing all the steps in building, running,
and playing the game you built (you should make no assumptions about what software the
interviewer has, and err on the side of being explicit). Your interviewers will be engineers, so you
can assume a certain level of technical ability as relates to installing what your project requires.
Please create a new public repository in Github and