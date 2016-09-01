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
    def get(pipeline_id):
        if pipeline_id == 1:
            from service.compute.pipelines.statistics.classification.training import ClassifierTrainingPipeline
            return ClassifierTrainingPipeline()
        if pipeline_id == 2:
            from service.compute.pipelines.statistics.classification.prediction import ClassifierPredictionPipeline
            return ClassifierPredictionPipeline()
        return None
