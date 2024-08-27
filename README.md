<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<br />
<div align="center">
  <a href="https://github.com/VolkenoMakers/MYAPP-django"></a>

  <h3 align="center">MYAPP DJANGO SHOP API</h3>
</div>

## About The Project


<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

- [Django](https://www.djangoproject.com/)
- [djangorestframework-jwt](https://jpadilla.github.io/django-rest-framework-jwt/)
- [django-import-export](https://django-import-export.readthedocs.io/en/latest/)
- [drf-generators](https://pypi.org/project/drf-generators/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites
List things you need to use the software and how to install them.

#### 1. Install python in function of your system.

For more information about it click link below https://www.python.org/downloads/

#### 2. Create a python environment

The environement setup process depends on your system. Do some research to find out how to do it on OS.

For Ubuntu you can use the following commands

```sh
virtualenv -p python3 env
source env/bin/activate
```

For OS WINDOWS you can use the following commands

```sh
virtualenv -p python3 env
source env/bin/activate
```
### Before installation 
_If you want generate serializers, views and urls respectively in that order_ 
    
    python manage.py generate api --serializers --format apiview --force
    python manage.py generate api --views --format apiview --force
    python manage.py generate api --urls --format apiview --force

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/guissemohamedcherif/gest_shop.git
   ```
2. Install required python packages

   ```sh
   pip install -r requirements.txt

   ```

3. Apply database migrations
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run the app
   ```sh
   python manage.py runserver
   ```

The api should now be running at http://127.0.0.1:8000/

<p align="right">(<a href="#top">back to top</a>)</p>

## VERSIONNING
### DEV
1. git tag -a dev-1.0 -m "Dev release 1.0"
2. git push origin --tags
