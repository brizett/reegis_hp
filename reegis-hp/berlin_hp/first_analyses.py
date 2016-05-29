# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:35:28 2016

@author: uwe
"""

import logging
import time
import os
import pandas as pd

# from oemof import db
from oemof.tools import logger


logger.define_logging()
# conn = db.connection()
start = time.time()

basic_path = '/home/uwe/chiba/RLI/data'
logging.info("Datapath: {0}:".format(basic_path))

wt_demand = pd.read_csv(os.path.join(basic_path, 'waermetool_demand.csv'),
                        index_col=0)
print(wt_demand['unsaniert'].values)
print(wt_demand['saniert'].values)

gebaeudetypen = ['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']

df = pd.read_csv(os.path.join(basic_path, 'haus_plr_test.csv'), index_col=0)
iwu_typen = pd.read_csv(os.path.join(basic_path, 'iwu_typen.csv'), index_col=0)
blocktype = pd.read_csv(os.path.join(basic_path, 'blocktype.csv'), ';',
                        index_col=0)
stadtstrukturtypen = pd.read_csv(
    os.path.join(basic_path, 'stadtnutzung_erweitert.csv'), index_col=0)

buildings = df.query(
    "building_function == 1000" +
    "or building_function == 1010"
    "or building_function == 1020"
    "or building_function == 1024"
    # "or building_function == 1120"
    )
# buildings = df
# print(buildings.blocktype)

iwu_by_blocktype = iwu_typen.merge(blocktype, left_index=True, right_index=True)

buildings_full = buildings.merge(iwu_by_blocktype, on='blocktype')
stadtstruktur_full = stadtstrukturtypen.merge(iwu_by_blocktype,
                                              right_on='blocktype',
                                              left_on='typklar')

print(stadtstruktur_full.columns)
# demand_by_type_unsaniert = pd.DataFrame(
#     buildings_full[['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
#         buildings_full['living_area'], axis="index").values *
#     wt_demand['unsaniert'].values,
#     columns=['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte'])
# sum_by_type_unsaniert = demand_by_type_unsaniert.sum()
#
# demand_by_type_saniert = pd.DataFrame(
#     buildings_full[['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
#         buildings_full['living_area'], axis="index").values *
#     wt_demand['saniert'].values,
#     columns=['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte'])
# sum_by_type_saniert = demand_by_type_saniert.sum()

area = stadtstruktur_full[[
        'EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
            stadtstruktur_full.ew * stadtstruktur_full.wohnflaeche_pro_ew,
            axis="index")

print('Area', area.sum())
# Area EFHv84    2.108395e+07
# EFHn84    2.676466e+06
# MFHv84    7.980254e+07
# MFHn84    1.330757e+07
# Platte    2.111442e+07

print(wt_demand)
sanierungsquote = pd.Series(data=[0.12, 0.03, 0.08, 0.01, 0.29],
                            index=wt_demand.index)
print(sanierungsquote)

print(type(stadtstruktur_full[[
        'EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
            stadtstruktur_full.ew * stadtstruktur_full.wohnflaeche_pro_ew,
            axis="index").values * wt_demand['unsaniert'].values))

# TODO Überprüfe ob die Operation die Reihenfolge erhält
demand_by_type_unsaniert = pd.DataFrame(
    (stadtstruktur_full[[
        'EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
            stadtstruktur_full.ew * stadtstruktur_full.wohnflaeche_pro_ew,
            axis="index").values *
        wt_demand['unsaniert'].values *
        (1 - sanierungsquote).values),
    columns=['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']).merge(
        stadtstruktur_full[['spatial_na', 'schluessel_planungsraum']],
        left_index=True, right_index=True)

demand_by_type_saniert = pd.DataFrame(
    (stadtstruktur_full[[
        'EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']].multiply(
            stadtstruktur_full.ew * stadtstruktur_full.wohnflaeche_pro_ew,
            axis="index").values *
        wt_demand['saniert'].values *
        sanierungsquote.values),
    columns=['EFHv84', 'EFHn84', 'MFHv84', 'MFHn84', 'Platte']).merge(
        stadtstruktur_full[['spatial_na', 'schluessel_planungsraum']],
        left_index=True, right_index=True)

sum_by_type_unsaniert = demand_by_type_unsaniert.sum()
sum_by_type_saniert = demand_by_type_saniert.sum()
print(sum_by_type_unsaniert[gebaeudetypen].sum())
print(sum_by_type_saniert[gebaeudetypen].sum())

print(sum_by_type_saniert.sum() / buildings_full['living_area'].sum())
print(sum_by_type_unsaniert.sum() / buildings_full['living_area'].sum())
print(sum_by_type_saniert.sum() / (stadtstruktur_full.ew *
                                   stadtstruktur_full.wohnflaeche_pro_ew).sum())
print(sum_by_type_unsaniert.sum() / (
    stadtstruktur_full.ew * stadtstruktur_full.wohnflaeche_pro_ew).sum())
print(buildings_full['total_loss_pres'].sum())
print(buildings_full['total_loss_contemp'].sum())
print(buildings_full['living_area'].sum())
print('Area', area.sum().sum())

print(buildings_full['living_area'].sum())

# print(buildings_full[['MFHv84', 'EFHv84']].values * buildings_full[[
#     'living_area', 'flatroof_area']].values)


