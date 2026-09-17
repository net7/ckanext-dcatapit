# this is a namespace package
import logging

from sqlalchemy import inspect

from ckan.model import meta

from ckanext.dcatapit.model.license import License, LocalizedLicenseName

from ckanext.dcatapit.model.subtheme import ThemeToSubtheme, Subtheme, SubthemeLabel

from ckanext.dcatapit.model.vocabulary import *
from ckanext.dcatapit.model.license import *

log = logging.getLogger(__name__)

__all__ = ['setup']


def setup_db():
    log.debug('Setting up DCATAPIT tables...')
    created = setup_vocabulary_models()
    created = setup_subtheme_models() or created
    created = setup_license_models() or created

    return created


def setup_vocabulary_models():
    created = False

    # Setting up tag multilang table
    if inspect(meta.engine).has_table(dcatapit_vocabulary_table.name):
        log.debug(f'DCATAPIT: table {dcatapit_vocabulary_table.name} already exists')
    else:
        try:
            log.info(f'DCATAPIT: creating table {dcatapit_vocabulary_table.name}')
            dcatapit_vocabulary_table.create(bind=meta.engine)
            created = True
        except Exception as err:
            # Make sure the table does not remain incorrectly created
            if inspect(meta.engine).has_table(dcatapit_vocabulary_table.name):
                meta.Session.execute('DROP TABLE dcatapit_vocabulary')
                meta.Session.commit()
            raise err

        log.debug('DCATAPIT Tag Vocabulary table created')

    return created


def setup_subtheme_models():
    created = False
    for t in (Subtheme.__table__,
              SubthemeLabel.__table__,
              ThemeToSubtheme.__table__,
              ):
        if not inspect(meta.engine).has_table(t.name):
            log.info(f'DCATAPIT: creating table {t.name}')
            t.create(bind=meta.engine)
            created = True
        else:
            log.debug(f'DCATAPIT: table {t.name} already exists')

    return created


def setup_license_models():
    created = False
    for t in (License.__table__,
              LocalizedLicenseName.__table__,
              ):
        if not inspect(meta.engine).has_table(t.name):
            log.info(f'DCATAPIT: creating table {t.name}')
            t.create(bind=meta.engine)
            created = True
        else:
            log.debug(f'DCATAPIT: table {t.name} already exists')

    return created
