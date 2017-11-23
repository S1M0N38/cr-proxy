import os
import json


class CrMessageDefinitions:
    @classmethod
    def read(cls):
        definitions_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "definitions")
        messages = {}
        for entry in os.scandir(definitions_path):
            if entry.is_dir() and entry.name[:1] is not ".":
                if entry.name == "component":
                    messages[entry.name] = {}
                for file in os.scandir(entry.path):
                    if file.name[:1] is not ".":
                        with open(file.path, 'r') as fh:
                            data = json.load(fh)
                            if entry.name == "component":
                                if "extensions" in data:
                                    extensions = {}
                                    for extension in data["extensions"]:
                                        extensions[extension["id"]] = extension
                                    data["extensions"] = extensions
                                messages[entry.name][data["name"]] = data
                            else:
                                messages[data["id"]] = data
        return messages
