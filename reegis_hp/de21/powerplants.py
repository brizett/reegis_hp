import pandas as pd
import os.path as path

GROUPED = path.join('data', 'powerplants', 'grouped', '{0}_cap.csv')


class PowerPlantsDE21:

    def __init__(self):
        self.cpp = pd.read_csv(GROUPED.format('conventional'),
                               index_col=[0, 1, 2])
        self.repp = pd.read_csv(GROUPED.format('renewable'),
                                index_col=[0, 1, 2, 3])

    def fuels(self):
        return list(self.cpp.index.get_level_values(0).unique())

    def cpp_region_fuel(self, year):
        return self.cpp.groupby(level=(1, 2, 0)).sum().loc[year]

    def repp_region_fuel(self, year):
        return self.repp.groupby(level=(1, 2, 0)).sum().loc[year]


if __name__ == "__main__":
    pp = PowerPlantsDE21()
    print(pp.cpp_region_fuel(2016))
    print(pp.repp_region_fuel(2016))
    cpp = pd.read_csv('/home/uwe/git_local/reegis-hp/reegis_hp/de21/data/powerplants/prepared/conventional_power_plants_DE_prepared.csv')
    cpp.loc[cpp.fuel == 'Biomass and biogas'].to_csv('cpp_bio.csv')
    repp = pd.read_csv('/home/uwe/git_local/reegis-hp/reegis_hp/de21/data/powerplants/prepared/renewable_power_plants_DE_prepared.csv')
    repp.loc[
        (repp.energy_source_level_2 == 'Bioenergy') &
        (repp.electrical_capacity > 1)].to_csv('repp_bio.csv')
