# Rocky Mountain Forager
Rocky Mountain Forager is an app that contains a library of edible and medicinal plants of the Rocky Mountain
region, as well as a flashcards game to aid memorization.

### Warning!
This app is not intended to be used as the sole means of plant identification. Always consult an expert
before consuming wild plants.

## Setup
RMF is a Python/Django application and requires the following steps to setup and use:

#### Create and activate Python virtual environment
- ``python3 -m venv <choose_environment_path_here>``
- ``source <chosen_env_path>/bin/activate``
#### Install the requirements and initialize the database
- ``pip install -r requirements.txt``
- ``python manage.py migrate``
#### Load data and run the server
- ``python manage.py loaddata library/fixtures/test_data.yaml``
- ``python manage.py runserver``
- Visit http://127.0.0.1:8000/
