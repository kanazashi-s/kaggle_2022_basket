from typing import Dict
from mlflow.tracking import MlflowClient


class MlflowWriter():
    def __init__(self, experiment_name, **kwargs):
        self.client = MlflowClient(**kwargs)
        try:
            self.experiment_id = self.client.create_experiment(experiment_name)
        except:
            self.experiment_id = self.client.get_experiment_by_name(experiment_name).experiment_id

        self.run_id = self.client.create_run(self.experiment_id).info.run_id

    def log_params_from_dict(self, params):
        for param_parent, param in params.items():
            for param_child, element in param.items():
                self.client.log_param(self.run_id, f'{param_parent}.{param_child}', element)


    def log_param(self, key, value):
        self.client.log_param(self.run_id, key, value)

    def log_metric(self, key, value):
        self.client.log_metric(self.run_id, key, value)

    def log_artifact(self, local_path):
        self.client.log_artifact(self.run_id, local_path)

    def set_terminated(self):
        self.client.set_terminated(self.run_id)


def write_mlflow(
        writer: MlflowWriter,
        cfg: Dict):
    writer.log_artifact(cfg["mljar_params"]["results_path"])