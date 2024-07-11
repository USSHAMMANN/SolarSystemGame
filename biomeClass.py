import json

class Biomes:
    def __init__(self,
                 biome_name: str,
                 biome_char: str,
                 biome_habitability: float,
                 biome_min_height: float,
                 biome_max_height: float,
                 biome_min_temp: float,
                 biome_max_temp: float,
                 biome_min_precipitation: float,
                 biome_max_precipitation: float) -> None:

        self.biome_name = biome_name
        self.biome_char = biome_char
        self.biome_habitability = biome_habitability
        self.biome_min_height = biome_min_height
        self.biome_max_height = biome_max_height
        self.biome_min_temp = biome_min_temp
        self.biome_max_temp = biome_max_temp
        self.biome_min_precipitation = biome_min_precipitation
        self.biome_max_precipitation = biome_max_precipitation

    @classmethod
    def list_to_json(cls, biomes: list['Biomes'], filename: str) -> None:
        """Сериализация списка объектов в файл формата JSON"""
        with open(filename, 'w') as file:
            json.dump([biome.__dict__ for biome in biomes], file, indent=4)

    @classmethod
    def list_from_json(cls, filename: str) -> list['Biomes']:
        """Десериализация списка объектов из файла формата JSON"""
        with open(filename, 'r') as file:
            data_list = json.load(file)
        return [cls(**data) for data in data_list]


# Пример использования
if __name__ == "__main__":
    # Создание списка объектов
    biomes = [
        Biomes(
            biome_name="Forest",
            biome_char="F",
            biome_habitability=0.8,
            biome_min_height=100.0,
            biome_max_height=2000.0,
            biome_min_temp=-5.0,
            biome_max_temp=30.0,
            biome_min_precipitation=500.0,
            biome_max_precipitation=2000.0
        ),
        Biomes(
            biome_name="Desert",
            biome_char="D",
            biome_habitability=0.2,
            biome_min_height=0.0,
            biome_max_height=1000.0,
            biome_min_temp=20.0,
            biome_max_temp=50.0,
            biome_min_precipitation=0.0,
            biome_max_precipitation=250.0
        )
    ]

    # Сериализация списка объектов в файл формата JSON
    filename = 'biomes.json'
    Biomes.list_to_json(biomes, filename)
    print(f"Serialized list to {filename}")

    # Десериализация списка объектов из файла формата JSON
    deserialized_biomes = Biomes.list_from_json(filename)
    print("\nDeserialized Objects:")
    for biome in deserialized_biomes:
        print(biome.__dict__)