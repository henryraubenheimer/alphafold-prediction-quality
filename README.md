Welcome to my AlphaFold Prediction tool!

## Setup

After installing from requirements.txt in root with 

```bash
pip install -r requirements.txt
```

some initial setup is required with

```bash
python manage.py makemigrations
python manage.py migrate
```

The server can now be run with

```python
python manage.py runserver
```

and accessed from http://127.0.0.1:8000/ . A new user can be created at http://127.0.0.1:8000/admin. To retrain the ML model, cd into the backend and run

```python
python -m ml_model.regressor
```

## Design Choices

Here are some design decisions I took:

* I considered a prediction with a plddt above 90 to be very confident, between 90 and 70 to be confident, between 70 and 50 to be of low confidence, and below 50 to be of very low confidence.
* Baseline heuristics include statistics around plddt like the mean and median plddt and the longest low confidence segment. Plddt holds no information on how correct domain orientations are, so an approximate ptm score is calculated with a tiny regression model.
* The ptm score is approximated with a linear regressor on a tiny training set (with just 5 data points) that can be expanded. A linear regressor was chosen for its simplicity and efficiency given the small training set. Ptm is approximated from the other plddt metrics, though plddt and ptm are distinct metrics.
* The model is first trained and then saved as a .pkl file before approximating. This prevents having to train the model everytime an approximation is needed.
* I included a login to the application for any potential security needs. Login details are stored in a sqlite database, which is particularly efficient for small-scale applications like this one.

## Time Spent and Future Work

I spent around 9 hours in total on this project (excluding this readme and video recording). Unfortunately I was unable to find time for the stretch goals, though I did make some progress on a 3D viewer. With an additional 4 hours I'd be able to complete this, source additional data to approximate ptm from and expand on the structural quality notes. I assumed plddt is the most informative metric to the users of this application, and that login security was of some value.
