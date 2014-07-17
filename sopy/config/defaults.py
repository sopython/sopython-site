DEBUG = True
SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'postgresql:///sopy'

ALEMBIC_CONTEXT = {
    'compare_type': True,
    'compare_server_default': True,
    'user_module_prefix': 'user',
}

# OAUTH_SO_APPLICATION_ID = ''
# OAUTH_SO_CONSUMER_KEY = ''
# OAUTH_SO_CONSUMER_SECRET = ''
