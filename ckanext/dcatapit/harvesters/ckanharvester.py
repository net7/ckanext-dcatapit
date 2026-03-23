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

    def import_stage(self, harvest_object):
        map_nonconformant_groups(harvest_object)
        data = map_ckan_license(harvest_object=harvest_object)
        data = map_ckan_frequency(pkg_dict=data)
        data = map_top_level_to_extras(data)
        harvest_object.content = json.dumps(data)
        return super(CKANMappingHarvester, self).import_stage(harvest_object)

    def modify_package_dict(self, package_dict, harvest_object):
        package_dict = super(CKANMappingHarvester, self).modify_package_dict(package_dict, harvest_object)
        log.warning('DCATAPIT modify_package_dict extras_keys=%s',
                    [e['key'] for e in package_dict.get('extras', [])])
        return package_dict
