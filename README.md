Welcome to my AlphaFold Prediction tool!

## Setup

After installing from requirements.txt in root with 

```bash
pip install -r requirements.txt
```

the server can be run with

```python
python manage.py runserver
```

and accessed from http://127.0.0.1:8000/ . A new user can be created at http://127.0.0.1:8000/admin. To retrain the ML model, cd into the backend and run

```python
python -m ml_model.regressor
```
