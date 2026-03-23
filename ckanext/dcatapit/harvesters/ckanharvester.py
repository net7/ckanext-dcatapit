#!/usr/bin/env python3

import json
import logging

from ckanext.dcatapit.harvesters.utils import map_ckan_license, map_ckan_frequency, map_top_level_to_extras
from ckanext.dcatapit.mapping import map_nonconformant_groups
from ckanext.harvest.harvesters.ckanharvester import CKANHarvester

log = logging.getLogger(__name__)


class CKANMappingHarvester(CKANHarvester):

    def info(self):
        return {
            'name': 'CKAN-DCATAPIT',
            'title': 'CKAN harvester for DCATAPIT',
            'description': 'Special version of CKANHarvester, which will map groups to themes',
            'form_config_interface': 'Text'
        }

    # Campi che dcatapit gestisce tramite convert_to_extras (IDatasetForm schema).
    # Devono stare come top-level nel pkg_dict, non dentro extras, altrimenti
    # il validator CKAN li scarta perché la chiave è "riservata" dallo schema.
    TOPLEVEL_FIELDS = ['holder_identifier', 'holder_name']

    def import_stage(self, harvest_object):
        map_nonconformant_groups(harvest_object)
        data = map_ckan_license(harvest_object=harvest_object)
        data = map_ckan_frequency(pkg_dict=data)
        data = map_top_level_to_extras(data)
        harvest_object.content = json.dumps(data)
        return super(CKANMappingHarvester, self).import_stage(harvest_object)

    def modify_package_dict(self, package_dict, harvest_object):
        package_dict = super(CKANMappingHarvester, self).modify_package_dict(package_dict, harvest_object)
        # Sposta holder_identifier e holder_name dagli extras al top-level
        # così il validator convert_to_extras di dcatapit li processa correttamente.
        extras_to_remove = []
        for i, extra in enumerate(package_dict.get('extras', [])):
            if extra['key'] in self.TOPLEVEL_FIELDS:
                package_dict[extra['key']] = extra['value']
                extras_to_remove.append(i)
        for i in reversed(extras_to_remove):
            package_dict['extras'].pop(i)
        log.warning('DCATAPIT modify_package_dict v2: holder_identifier=%s holder_name=%s',
                    package_dict.get('holder_identifier'), package_dict.get('holder_name'))
        return package_dict
