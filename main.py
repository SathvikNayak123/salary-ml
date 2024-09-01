from src.pipeline.training_pipeline import TrainingPipeline

try:
    obj = TrainingPipeline("artifacts/data_clean.csv", "artifacts/data_transformed.csv")
    obj.DataTransform()
    obj.run()
except Exception as e:
    raise e