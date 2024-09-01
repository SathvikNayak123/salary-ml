from components.data_transform import JobDataProcessor
from components.model_training import ModelTrainer

class TrainingPipeline:
    def __init__(self, clean_path, transform_path):
        self.clean_data= clean_path
        self.transformed_data= transform_path
        self.job_data_processor = JobDataProcessor(self.clean_data)
        self.model_trainer = ModelTrainer(self.transformed_data)

    def DataTransform(self):
        self.job_data_processor.process_data()
        self.job_data_processor.save_data(self.transformed_data)

    def TrainModel(self):
        self.model_trainer.run()