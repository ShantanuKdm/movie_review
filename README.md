# movie_review

## API Document
* [Click here for API reference](https://opalescent-mink-676.notion.site/API-Documentation-265bfc1148a345c597526ee32a880890?pvs=4)
  
## Setup
* Install python and pip

* Create a virtual environment:
```sh 
pip install virtualenv
```
```sh 
mkdir venvs
```
```sh 
cd venvs
```
```sh 
virtualenv --python=<path-to-python-3.10.1> <virtual-env-path>
```
```
source <virtual-env-path>/bin/activate
```

* OR If using PYCharm, set up an interpreter that will automatically create and activate the virtual environment

* * Clone the repo
```sh 
git clone git@github.com:devShantanu-Kadam/movie_review.git
```
* Install mysql on machine if not installed already
  
```sh 
run pip install -r requirements.txt
```

## Running 
* Add an .env file at project level 

```sh 
python manage.py migrate
```
```sh 
python manage.py runserver
```
* pull inital data

```sh 
hit "localhost:8000/movies/getmovies"
```
