import json
import pathlib


class FileInteraction:
    @staticmethod
    def read_info(path: str) -> dict:
        with open(path, "r") as fh:
            try:
                file_data = json.load(fh)
            except ValueError:
                return {}
            return file_data

    @staticmethod
    def save_info(path: str, data: dict) -> None:
        with open(path, mode="w") as fh:
            json.dump(data, fh)
