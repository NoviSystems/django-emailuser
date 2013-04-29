Pay no attention to the unfinished project
==========================================


django-emailuser
================

Email-based users for Django 1.5. Mimics Django's default User class, but without usernames. 


Behavior Differences
--------------------

- ``get_full_name()`` returns the user's full name or their full email address. 
- ``get_short_name()`` returns the user's first name or the local part of their email address. 
- ``get_absolute_url()`` replaces username with the user email address and swaps @ with _


Quick start
-----------

1. Use pip or otherwise clone the repository into your environment. PyPi package coming shortly. 


2. Set ``AUTH_USER_MODEL`` to ``EmailUser``:

.. code-block:: python

    AUTH_USER_MODEL = 'emailuser.EmailUser'


3. Add ``'emailuser',`` under the ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'emailuser',
    )


4. Sync your database.

.. code-block:: python

    python manage.py syncdb

or use South and migrate an existing database

.. code-block:: python

    python manage.py migrate thingsandstuff


Usage
-----

Usage details are provided in the [Django documentation](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#referencing-the-user-model). In summary, there are two rules:


1. Do not reference the ``User`` class directly. Instead, use ``django.contrib.auth.get_user_model()`` to get the currently active user model. 


2. When defining a relation to the User model, you should specify the custom model using the AUTH_USER_MODEL setting.

.. code-block:: python

    from django.conf import settings
    from django.db import models

    class Article(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL)


``EmailUser`` can be extending by inheriting from ``AbstractEmailUser``.
