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

    def _create_or_update_package(self, package_dict, harvest_object, package_dict_form='rest'):
        # Il CKANHarvester base inietta uno schema default nel context che bypassa
        # IDatasetForm di dcatapit. Chiamiamo super() e poi forziamo il salvataggio
        # di holder_identifier e holder_name direttamente in package_extra.
        from ckan.model import Session, PackageExtra, Package
        result = super(CKANMappingHarvester, self)._create_or_update_package(
            package_dict, harvest_object, package_dict_form)

        if result and result is not False:
            holder_fields = {}
            for extra in package_dict.get('extras', []):
                if extra['key'] in ('holder_identifier', 'holder_name'):
                    holder_fields[extra['key']] = extra['value']

            if holder_fields and harvest_object.package_id:
                pkg = Session.query(Package).get(harvest_object.package_id)
                if pkg:
                    for key, value in holder_fields.items():
                        existing = Session.query(PackageExtra).filter_by(
                            package_id=pkg.id, key=key).first()
                        if existing:
                            existing.value = value
                        else:
                            Session.add(PackageExtra(package_id=pkg.id, key=key, value=value))
                    Session.flush()

        return result
