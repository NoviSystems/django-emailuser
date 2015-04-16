
django-emailuser
================

Email-based user model for Django 1.8ish+. 


Setup
-----

1. Use pip or otherwise install the package into your environment. PyPi package coming probably never.

    ```
    $ pip install git+git://github.com/ITNG/django-emailuser.git
    ```


2. Set `AUTH_USER_MODEL` to `EmailUser`:

    ```python
    AUTH_USER_MODEL = 'emailuser.EmailUser'
    ```


3. Add ``'emailuser',`` under the ``INSTALLED_APPS`` setting:

    ```python
    INSTALLED_APPS = (
        ...
        'emailuser',
    )
    ```


4. Migrate your database.

    ```shell
    $ python manage.py migrate
    ```


Usage
-----

Usage details are provided in the [Django documentation](https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#referencing-the-user-model). In summary, there are two rules:


1. Do not reference the ``User`` class directly. Instead, use ``django.contrib.auth.get_user_model()`` to get the currently active user model. 


2. When defining a relation to the User model, you should specify the custom model using the AUTH_USER_MODEL setting.

    ```python
    from django.conf import settings
    from django.db import models

    class Article(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL)
    ```


Additionally
------------

`EmailUser` can be extended by inheriting from `AbstractEmailUser`. `EmailUserAdmin` will also need to be extended.

It is the de facto standard that emails are case insensitive. This package does so when possible. Currently the only supported database is PostgreSQL.


License & Copyright
-------------------

django-emailuser is released under the BSD 3-Clause license.

&copy; 2013 North Carolina State University.
