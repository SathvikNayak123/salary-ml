from pipeline.training_pipeline import TrainingPipeline

try:
    obj = TrainingPipeline()
    
    print("Running Data Ingestion...")
    obj.DataIngest()
    
    print("Running Data Transformation...")
    obj.DataTransform()
    
    print("Training Model...")
    obj.TrainModel()

    print("Pipeline completed successfully.")

except FileNotFoundError as fnf_error:
    print(f"Error: {fnf_error}")
except Exception as e:
    print(f"error occurred: {e}")
    raise
