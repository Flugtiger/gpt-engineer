import os
import json
import jsonschema

class RequirementsLoader:
    def __init__(self, requirements_dir: str, schema_path: str):
        self.requirements_dir = requirements_dir
        self.schema_path = schema_path
        self.schema = self._load_schema()

    def _load_schema(self):
        with open(self.schema_path, 'r') as schema_file:
            return json.load(schema_file)

    def load_requirements(self, base_path: str) -> str:
        requirements_path = os.path.join(base_path, self.requirements_dir)
        if not os.path.isdir(requirements_path):
            raise ValueError(f"The path {requirements_path} is not a directory.")

        prompt_str = ""
        for filename in sorted(os.listdir(requirements_path)):
            if filename.endswith(".json"):
                file_path = os.path.join(requirements_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            # Validate JSON against schema
                            jsonschema.validate(instance=data, schema=self.schema)
                            requirement_text = data.get("requirementText", "")
                            prompt_str += requirement_text + "\n"
                        except jsonschema.exceptions.ValidationError as e:
                            print(f"Warning: {filename} does not comply with the schema. {e.message}")
                        except json.JSONDecodeError:
                            print(f"Warning: {filename} is not a valid JSON file.")
        return prompt_str
