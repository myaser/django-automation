from south.management.commands.schemamigration import Command as SouthCommand
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''
    detect apps that has initial migrations and automatically schemamigrate
    them
    '''
    _schemamigration = SouthCommand()

    def handle(self, **options):
        for app in _get_migrated_apps():
            self._schemamigration.handle(app=app, auto=True, **options)


def _get_migrated_apps():
    '''
    automatically detect apps that needs migration
    coppied from south
    '''

    from django.db import models
    from south import migration
    from south.management.commands.syncdb import get_app_label
    from south.exceptions import NoMigrations

    for app in models.get_apps():
        app_label = get_app_label(app)
        try:
            migration.Migrations(app_label)
        except NoMigrations:
            # It needs syncing
            continue
        else:
            # This is a migrated app, leave it
            yield app_label
