import yaml
from drf_spectacular.utils import extend_schema


def extend_schema_from_yaml(yaml_file_path, operation_id=None):
    def decorator(view_func):
        with open(yaml_file_path, "r") as file:
            schema = yaml.safe_load(file)

        kwargs_labels = ["summary", "description", "responses", "tags"]
        extend_schema_kwargs = dict()

        for label in kwargs_labels:
            if schema.get(label):
                extend_schema_kwargs[label] = schema[label]

        return extend_schema(**extend_schema_kwargs)(view_func)

    return decorator
