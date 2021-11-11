#*******************************IMPORT MODULE***********************************

import pandas
import folium

#*******************************GET DATA***********************************

data = pandas.read_excel("world_coronavirus_cases.xlsx")

#*******************************lIST GROUP***********************************

latitudes = list(data["Enlem"])
longitudes = list(data["Boylam"])
names = list(data["Ülke"])
total_cases = list(data["Toplam Vaka"])
deaths = list(data["Vefat Edenler"])
actives = list(data["Aktif Vakalar"])
total_test = list(data["Toplam Test"])
population = list(data["Nüfus"])

#*******************************FEATURE GROUP***********************************

case_count_map = folium.FeatureGroup(name="Total Case Count Map")
death_rate_map = folium.FeatureGroup(name=" Death Rate Map")
active_case_map = folium.FeatureGroup(name=" Active Case Map")
test_rate_map = folium.FeatureGroup(name="Test Rate Map")
population_distribution_map = folium.FeatureGroup(name="Population Distribution Map")

#*******************************FUNCTION GROUP***********************************

def case_count_color(case):
    if case < 100000:
        return "green"
    elif case < 300000:
        return "white"
    elif case < 750000:
        return "orange"
    else:
        return "red"

def case_count_radius(case):
    if case < 100000:
        return 40000
    elif case < 300000:
        return 100000
    elif case < 750000:
        return 200000
    else:
        return 400000

def death_rate_color(case, death):
    if (death / case) * 100 < 2.5:
        return "green"
    elif (death / case) * 100 < 5:
        return "white"
    elif (death / case) * 100 < 7.5:
        return "orange"
    else:
        return "red"

def death_rate_radius(case, death):
    if (death / case) * 100 < 2.5:
        return 40000
    elif (death / case) * 100 < 5:
        return 100000
    elif (death / case) * 100 < 7.5:
        return 200000
    else:
        return 400000

def active_case_color(active):
    if active < 100000:
        return "green"
    elif active < 300000:
        return "white"
    elif active < 750000:
        return "orange"
    else:
        return "red"

def active_case_radius(active):
    if active < 100000:
        return 40000
    elif active < 300000:
        return 100000
    elif active < 750000:
        return 200000
    else:
        return 400000

def test_rate_color(population, test):
    if (test / population) * 100 < 2.5:
        return "red"
    elif (test / population) * 100 < 5:
        return "white"
    elif (test / population) * 100 < 7.5:
        return "orange"
    else:
        return "green"

def test_rate_raidus(population, test):
    if (test / population) * 100 < 2.5:
        return 400000
    elif (test / population) * 100 < 5:
        return 200000
    elif (test / population) * 100 < 7.5:
        return 100000
    else:
        return 40000

#*******************************CREATE WORLD MAP***********************************

world_map = folium.Map(tiles="Cartodb dark_matter")

#*******************************CREATE MARKER***********************************

for latitude, longitude, name, case in zip(latitudes, longitudes, names, total_cases):
    case_count_map.add_child(folium.Circle(location=(latitude, longitude),
                                      radius=case_count_radius(case),
                                      color=case_count_color(case),
                                      fill_color=case_count_color(case),
                                      fill_opacity=0.3,
                                      popup=name))

for latitude, longitude, name, case, death in zip(latitudes, longitudes, names, total_cases, deaths):
    death_rate_map.add_child(folium.Circle(location=(latitude, longitude),
                                      radius=death_rate_radius(case, death),
                                      color=death_rate_color(case, death),
                                      fill_color=death_rate_color(case, death),
                                      fill_opacity=0.3,
                                      popup=name))

for latitude, longitude, name, active in zip(latitudes, longitudes, names, actives):
    active_case_map.add_child(folium.Circle(location=(latitude, longitude),
                                      radius=active_case_radius(active),
                                      color=active_case_color(active),
                                      fill_color=active_case_color(active),
                                      fill_opacity=0.3,
                                      popup=name))

for latitude, longitude, name, test, country_population in zip(latitudes, longitudes, names, total_test, population):
    test_rate_map.add_child(folium.Circle(location=(latitude, longitude),
                                      radius=test_rate_raidus(country_population, test),
                                      color=test_rate_color(country_population, test),
                                      fill_color=test_rate_color(country_population, test),
                                      fill_opacity=0.3,
                                      popup=name))

#*******************************ADD COUNTRY BORDER***********************************

population_distribution_map.add_child(folium.GeoJson(data=(open("world.json", "r", encoding="utf-8-sig").read()),
                                                     style_function= lambda x: {'fillColor':'green'
                                                     if x["properties"]["POP2005"] < 20000000 else 'white'
                                                     if 20000000 <= x["properties"]["POP2005"] <= 50000000 else 'orange'
                                                     if 50000000 <= x["properties"]["POP2005"] <= 100000000 else 'red'}))


#*******************************DEFINE LAYERS TO MAP***********************************

world_map.add_child(case_count_map)
world_map.add_child(death_rate_map)
world_map.add_child(active_case_map)
world_map.add_child(test_rate_map)
world_map.add_child(population_distribution_map)

#*******************************LAYER CONTROL***********************************

world_map.add_child(folium.LayerControl())

#*******************************SAVE THE MAP***********************************

world_map.save("world_map.html")