#  This work is based on original code developed and copyrighted by TNO 2020.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

from application.esdl import esdl
from application.esdl.esh import EnergySystemHandler


class EnergySystemStatistics:

    def __init__(self):
        self.esh = EnergySystemHandler()
        self.es = None
        self.area = None

    def calculate(self, esdl_string):
        self.esh.load_from_string(esdl_string, 'calc_stats')
        self.es = self.esh.get_energy_system()

        result = dict()
        self.get_energysystem_info(result)

        instances = self.es.instance
        if instances:
            inst = instances[0]
            if inst:
                self.area = inst.area
                if self.area:
                    self.get_all_areas_info(result)
                    self.get_number_of_assets_info(result)
                    self.get_power_of_assets_info(result)

        return result

    def get_energysystem_info(self, res_dict):
        res_dict['energysystem'] = {
            'es_id': self.es.id,
            'es_name': self.es.name,
            'es_description': self.es.description,
            'inst_id': self.es.instance[0].id,
            'inst_name': self.es.instance[0].name
        }

    def _get_area_info(self, area):
        res = {
            'id': area.id,
            'name': area.name,
            'scope': str(area.scope),
            'sub_areas': [],
            'bld_info': {}
        }

        for sub_area in area.area:
            ar_info = self._get_area_info(sub_area)
            res['sub_areas'].append(ar_info)

        res['bld_info'] = self._building_statistiscs_per_area(area)

        return res

    def get_all_areas_info(self, res_dict):
        res_dict['areas'] = self._get_area_info(self.area)

    def _get_number_of_assets_in_building(self, building, res):
        for content in building.eContents:
            if isinstance(content, esdl.AbstractBuilding):
                self._get_number_of_assets_in_building(content, res)
            if isinstance(content, esdl.Asset):
                if content.__class__.__name__ in res:
                    res[content.__class__.__name__]['cnt'] += 1
                    res[content.__class__.__name__]['aggr_cnt'] += content.aggregationCount
                else:
                    res[content.__class__.__name__] = {'cnt': 1, 'aggr_cnt': content.aggregationCount}

    def _get_number_of_assets_in_area(self, area, res):
        for content in area.eContents:
            if isinstance(content, esdl.Area):
                self._get_number_of_assets_in_area(content, res)
            if isinstance(content, esdl.AbstractBuilding):
                self._get_number_of_assets_in_building(content, res)
            if isinstance(content, esdl.Asset):
                if content.__class__.__name__ in res:
                    res[content.__class__.__name__]['cnt'] += 1
                    res[content.__class__.__name__]['aggr_cnt'] += content.aggregationCount
                else:
                    res[content.__class__.__name__] = {'cnt': 1, 'aggr_cnt': content.aggregationCount}

    def get_number_of_assets_info(self, res_dict):
        res = dict()
        self._get_number_of_assets_in_area(self.area, res)
        res_dict['number_of_assets'] = res

    def _get_power_of_assets_in_building(self, building, res):
        for content in building.eContents:
            if isinstance(content, esdl.AbstractBuilding):
                self._get_power_of_assets_in_building(content, res)
            if isinstance(content, esdl.EnergyAsset):
                if 'power' in dir(content):
                    if content.__class__.__name__ in res:
                        res[content.__class__.__name__] += content.power
                    else:
                        res[content.__class__.__name__] = content.power

    def _get_power_of_assets_in_area(self, area, res):
        for content in area.eContents:
            if isinstance(content, esdl.Area):
                self._get_power_of_assets_in_area(content, res)
            if isinstance(content, esdl.AbstractBuilding):
                self._get_power_of_assets_in_building(content, res)
            if isinstance(content, esdl.EnergyAsset):
                if 'power' in dir(content):
                    if content.__class__.__name__ in res:
                        res[content.__class__.__name__] += content.power
                    else:
                        res[content.__class__.__name__] = content.power

    def get_power_of_assets_info(self, res_dict):
        res = dict()
        self._get_power_of_assets_in_area(self.area, res)
        res_dict['power_of_assets'] = res

    def _building_statistiscs_per_area(self, area):
        type_number_area = dict()
        for asset in area.asset:
            if isinstance(asset, esdl.Building):
                for bld_asset in asset.asset:
                    if isinstance(bld_asset, esdl.BuildingUnit):
                        bldu_gbd = bld_asset.type
                        gbds = list()
                        for gbd in bldu_gbd:
                            gbds.append(str(gbd))
                        gbds_str = ",".join(gbds)

                        bldu_floor_area = bld_asset.floorArea

                        if gbds_str in type_number_area:
                            gbd_stats = type_number_area[gbds_str]
                        else:
                            gbd_stats = dict()
                            type_number_area[gbds_str] = gbd_stats

                        if 'number' in gbd_stats:
                            gbd_stats['number'] += 1
                        else:
                            gbd_stats['number'] = 1

                        if 'floor_area' in gbd_stats:
                            gbd_stats['floor_area'] += bldu_floor_area
                        else:
                            gbd_stats['floor_area'] = bldu_floor_area

        return type_number_area
