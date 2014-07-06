DEBUG = True
SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'postgresql:///sopy'

ALEMBIC_CONTEXT = {
    'compare_type': True,
    'compare_server_default': True,
    'user_module_prefix': 'user',
}
