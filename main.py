'''
параметры настройки биомов планеты

temper = "температура зоны"
located = "относительное нахождение зоны"
rainfall = "влажность зоны"

параметры карты планеты

planet_seed = "Сид планеты"
planet_type = "Вид планеты"
planet_type_like = "тип планеты"

planet_type_list = [earthLike,desertLike,waterLike,gasLike]
'''


import random, biomeClass
import numpy as np
from noise import pnoise2


def generate_perlin_noise_2d(shape, scale, octaves, seed=None):
    if seed:
        np.random.seed(seed)
    noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise[i][j] = pnoise2(i / scale, j / scale, octaves=octaves, persistence=0.5,
                                  lacunarity=2.0, repeatx=1024, repeaty=1024, base=42)
    return noise


def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)


def scale_to_range(array, new_min, new_max):
    return array * (new_max - new_min) + new_min


def generate_maps(width, height, scale, octaves, seed=None):
    # Угол вращения для разнообразия шума

    noise_temperature = generate_perlin_noise_2d((width, height), scale, octaves[0], seed)
    noise_humidity = generate_perlin_noise_2d((width, height), scale, octaves[1], seed)
    noise_height = generate_perlin_noise_2d((width, height), scale, octaves[2], seed)

    map_temperature = normalize(noise_temperature)
    map_humidity = normalize(noise_humidity)
    map_height = normalize(noise_height)

    map_temperature = scale_to_range(map_temperature, -50, 50)
    map_humidity = scale_to_range(map_humidity, 0, 5000)
    map_height = scale_to_range(map_height, 0, 2500)

    return map_humidity, map_temperature, map_height


def generate_world_map(width, height, scale, biome_list, seed=None, planet_type='earthLike'):
    octave_temp = 0
    octave_humidity = 0
    octave_mountain = 0

    # Условия для разных типов планет
    if planet_type == 'earthLike':
        octave_temp = 5
        octave_humidity = 5
        octave_mountain = 5
    elif planet_type == 'desertLike':
        octave_temp = 4
        octave_humidity = 6
        octave_mountain = 5
    elif planet_type == 'waterLike':
        octave_temp = 6
        octave_humidity = 2
        octave_mountain = 3

    humidity_map, temperature_map, height_map = generate_maps(width, height, scale,
                                                              (octave_temp, octave_humidity, octave_mountain), seed)

    world_map = np.chararray((width, height))
    world_map[:] = ' '

    for i in range(width):
        for j in range(height):
            point_humidity = round(humidity_map[i][j], 2)
            point_temperature = round(temperature_map[i][j], 2)
            point_height = round(height_map[i][j], 2)

            # Здесь должна быть обработка списка биомов и поиск по его параметрам нужного биома
            for biome in biome_list:
                if (biome.biome_min_temp <= point_temperature <= biome.biome_max_temp and
                        biome.biome_min_height <= point_height <= biome.biome_max_height and
                        biome.biome_min_precipitation <= point_humidity <= biome.biome_max_precipitation):
                    world_map[i][j] = biome.biome_char
                else:
                    world_map[i][j] = 'N'
            print(f"Позиция {i} {j} температура {point_temperature} влажность {point_humidity} высота {point_height} "
                  f"Символ {world_map[i][j]}")
    return world_map


def print_world_map(world_map):
    for row in world_map:
        print("".join(row.decode('utf-8')))


if __name__ == "__main__":
    width, height = 10, 20
    scale = 100.0
    seed = random.randint(0, 1000)
    biomelist = biomeClass.Biomes.list_from_json("biomes.json")
    planet_type = 'desertLike'  # Можно изменить на 'earthLike', 'desertLike', 'waterLike', 'gasLike'
    world_map = generate_world_map(width, height, scale, biomelist, seed, planet_type)
    print_world_map(world_map)
