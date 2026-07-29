import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blue_team_portal.settings")

from blue_team_portal.wsgi import application

app = application
