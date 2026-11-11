# Human vs AI: Income Prediction Game

A Django web application where users guess the income bracket (>50K or <=50K) of a randomly selected person from the UCI Adult dataset, competing against a Neural Network ML model. 

## Features
- **User Authentication:** Register, login, and track your score.
- **ML Pipeline:** Uses a Scikit-Learn `Pipeline` with `ColumnTransformer` and `MLPClassifier` to handle raw categorical/numeric data directly.
- **Scoreboard:** Saves every round to the database comparing the Human's guess vs the AI's confidence and correctness.

## Setup
    pip install -r requirements.txt
    cd income_lab
    python manage.py migrate
    python manage.py runserver

Open http://127.0.0.1:8000

## Structure
- `Trained Model/` — Training notebooks and exported `.pkl` pipeline.
- `income_lab/` — Django project containing the app, auth views, and scoreboard models.