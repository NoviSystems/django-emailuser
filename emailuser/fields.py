
from django.db.models import fields


class EmailField(fields.EmailField):

    def __init__(self, *args, **kwargs):
        self.case_insensitive = kwargs.pop('case_insensitive', True)
        return super(EmailField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        if self.case_insensitive:
            if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
                return 'citext'

        return super(EmailField, self).db_type(connection)
