from typing import Dict, List
import os.path as path
import json


class Data(List):
    """ A wrapper around a list to make more understanding/intuitive sounding methods """

    def does_not_contain(self, value):
        return value not in self

    def add(self, value):
        self.append(str(value))


class DataWriter:
    """ A wrapper around a dictionary class that does some file loading and saving. """

    def __init__(self, output_path):
        self.json_path = path.join(output_path, 'data.json')
        self.changed = False

        if path.exists(self.json_path):
            self.data = self._load_data()
        else:
            self.data = {}
            self.save()

    def __getitem__(self, item) -> Data:
        if item not in self.data.keys():
            self.data[item] = Data()
        return self.data[item]

    def __str__(self) -> str:
        return str(self.data)

    def _load_data(self) -> Dict:
        with open(self.json_path, 'r') as file:
            return {key: Data(value) for key, value in dict(json.load(file)).items()}

    def save(self) -> None:
        with open(self.json_path, 'w') as file:
            json.dump(self.data, file, sort_keys=True, separators=(',', ':'), ensure_ascii=False, indent=4)
