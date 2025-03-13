import os
import json
import jsonschema

class RequirementsLoader:
    def __init__(self, repo_path: str):
        self.requirements_dir = "requirements"
        self.repo_path = repo_path
        self.model_schema = self._load_schema('model_requirements_schema.json')
        self.application_schema = self._load_schema('application_requirements_schema.json')

    def _load_schema(self, name: str):
        schema_path = os.path.join(os.path.dirname(__file__), '..', name)
        with open(schema_path, 'r') as schema_file:
            return json.load(schema_file)

    def load_requirements(self) -> str:
        requirements_path = os.path.join(self.repo_path, self.requirements_dir, "model")
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
                            jsonschema.validate(instance=data, schema=self.model_schema)
                            requirement_text = data.get("requirementText", "")
                            prompt_str += requirement_text + "\n"
                        except jsonschema.exceptions.ValidationError as e:
                            print(f"Warning: {filename} does not comply with the schema. {e.message}")
                        except json.JSONDecodeError:
                            print(f"Warning: {filename} is not a valid JSON file.")
        return prompt_str
        
    def load_application_requirements(self) -> str:
        """
        Load application requirements from the 'requirements/application' directory.
        
        Returns
        -------
        str
            A string containing all the application requirements.
        """
        requirements_path = os.path.join(self.repo_path, self.requirements_dir, "application")
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
                            jsonschema.validate(instance=data, schema=self.application_schema)
                            prompt_str += f"{data['type']} '{data['name']}': {data["requirementText"]}\n"
                        except jsonschema.exceptions.ValidationError as e:
                            print(f"Warning: {filename} does not comply with the schema. {e.message}")
                        except json.JSONDecodeError:
                            print(f"Warning: {filename} is not a valid JSON file.")
        return prompt_str
