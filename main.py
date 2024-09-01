from pipeline.training_pipeline import TrainingPipeline

try:
    obj = TrainingPipeline("artifacts/data_cleaned.csv", "artifacts/data_transformed.csv")
    obj.DataTransform()
    obj.TrainModel()
except Exception as e:
    raise e