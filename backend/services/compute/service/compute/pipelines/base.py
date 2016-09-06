import importlib
from flask import Config


# ----------------------------------------------------------------------------------------------------------------------
class Pipeline(object):

    def run(self, params):
        raise NotImplementedError()

    @staticmethod
    def config():
        config_ = Config(None)
        config_.from_object('service.compute.settings')
        return config_


# ----------------------------------------------------------------------------------------------------------------------
class PipelineRegistry(object):

    @staticmethod
    def get(pipeline_name):
        config = Config(None)
        config.from_object('service.compute.settings')
        pipelines = config['PIPELINES']
        if pipeline_name not in pipelines.keys():
            return None
        pipeline_cls = getattr(importlib.import_module(
            pipelines[pipeline_name]['module_path']), pipelines[pipeline_name]['class_name'])
        pipeline_obj = pipeline_cls()
        return pipeline_obj

    @staticmethod
    def get_all():
        config = Config(None)
        config.from_object('service.compute.settings')
        return config['PIPELINES']
