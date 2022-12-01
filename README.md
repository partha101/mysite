# Django application for safe path finder using osmnx

## Modules used:
* [osmnx](https://osmnx.readthedocs.io/en/stable/)
* [networkx](https://networkx.org/)
* [Django](https://www.djangoproject.com/)
* [pickle](https://docs.python.org/3/library/pickle.html)
* [folium](https://python-visualization.github.io/folium/)
* [geopy](https://geopy.readthedocs.io/en/stable/)
* [geopandas](https://geopandas.org/en/stable/)


## Project installation guide

* Run `python --version` to check if you have python installed. If yes make sure you have python 3 installed. If not install python. Download python from [here](https://www.python.org/downloads/).
* Run `pip --version` to check if you have pip installed. If not install pip from [here](https://pip.pypa.io/en/stable/installation/).

* Create a virtual environment in the directory you want to work on. [Here](https://docs.python.org/3/tutorial/venv.html) is a tutorial on how to use python venv to create virutal environments.
* Now make a folder for your spatial project inside your current directory.
* Clone the repository using the command (make sure you have git installed). If not install git by following [this](https://git-scm.com/).
> `git clone https://github.com/partha101/mysite.git`
* Run the following pip command to install the required packages
> `pip install -r requirements.txt`
* Now run `py manage.py runserver` to run the project.
* Now go to this [link](http://127.0.0.1:8000/maps/) and hopefully you'll be able to see the website.
