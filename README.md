# django-shop

E-commerce web-app implemented using Django and Stripe. Comes ready to be deployed on heroku with minimum initial configuration!

***

**Build with:**

* Django
* Python
* SQLite (Development/Testing)
* PostgreSQL (Production)
* [Python Social Auth - Django](https://github.com/python-social-auth/social-app-django)
* Bootstrap

***

## Documentation

### Developer Section
***

**Installation**

Clone repository and cd inside downloaded folder

```
$ git clone https://github.com/aakatev/django-shop.git && cd django-shop
```

Configure virtual environment (In this example, I am using [Virtualenv](https://virtualenv.pypa.io/en/stable/), but you are free to do it your own way!)


First, check Python version installed

On Linux, one of the possible ways is to enter <code>$ /usr/bin/python</code> in your terminal and hit <code>Tab</code> key twice

This would show all the available vesrsions 

```
python             python3            python3.6m         python3m
python2            python3.6          python3.6m-config  python3m-config
python2.7          python3.6-config   python3-config     
```


Now, create environment with desired version of Python specified, as <code>--python=PY_VERSION</code> (Note: Django 2.x.. requres Python 3.x.. version!) 


```
$ virtualenv MY_ENV --python=python3.6
```


Activate your environment, and install Django and other dependencies

Note: If your environment name differs from <code>MY_ENV</code>, you would have to use <code>source YOUR_ENV_NAME/bin/activate</code> as first command

```
$ source activate &&  pip install -r requirements_dev.txt
```

Migrate SQLite

```
$ python manage.py migrate
```

In my_app directory, create <code>developemnt.py</code> file with the following content

``` python
import os
# Turn on debug mode
DEBUG = True
# Keys
SECRET_KEY = <your_secret_key>
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = <your_google_oauth2_key>
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = <your_google_oauth2_secret>
# Database (sqlite3)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

   }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_app.wsgi.application'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Deployment use ROOT!
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Development use DIRS!
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Redirect URLs
LOGIN_REDIRECT_URL = '/shop'
LOGIN_URL = '/auth/login/google-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Google Oauth2
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
```

You also need to add localhost:8000 to the list of Authorized redirect URIs at your Google Developer Console. 

***

**Development**


Start development server

```
(MY_ENV)$ python manage.py runserver
```

Success! Your development server is now accessible at <code>http<span></span>://127.0.0.1:8000/</code> or <code>http:/<span></span>/localhost:8000/</code>. However, I recommend to use <code>http<span></span>://localhost:8000/</code> as it is easier to setup to work with Google OAuth.  

First, go to your [Google Developers Console](https://console.developers.google.com). After you enabled Google+ API, create a new project (or use existing project), and add Credentials with Authorized redirect URIs <code>http:<span></span>//localhost:8000/complete/google-oauth2/</code>. This should allow you to have  


Django-admin superuser credentials are admin/hello_password


In case, you want to save your current dependencies in a text file 

```
(MY_ENV)$ pip freeze > requirements_dev.txt
```

***


**Deployment on Heroku**

Most of Django configuration has already been preset, and you only need to modify <code>setting.py</code> file to use deployment(heroku) settings instead of development one

```python
# Development settings
#from .development import *
# Deployment settings (heroku)
from .deployment_heroku import *
```

Now, create a new heroku app, add environmental variables to your app(use same names as in Python), and push django-shop folder to heroku master. Don't forget to migrate database after you push! 

**Deployment on linux server**

[How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 16.04 ](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

#### Official Docs & References


[Getting started with Django](https://www.djangoproject.com/start/)


[Django Documentation](https://docs.djangoproject.com/en/2.1/)

[Pip Documentation](https://pip.pypa.io/en/stable)

[Virtualenv User Guide](https://virtualenv.pypa.io/en/stable/userguide/)

[Gunicorn Documentation](http://docs.gunicorn.org/en/stable/)

[Nginx Documentation](https://nginx.org/en/docs/)
