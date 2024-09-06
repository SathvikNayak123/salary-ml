from components.data_transform import JobDataProcessor
from components.model_training import ModelTrainer
from components.data_cleaning import JobDataClean

class TrainingPipeline:
    def __init__(self):
        self.job_data_cleaner = JobDataClean()
        self.job_data_processor = JobDataProcessor()
        self.model_trainer = ModelTrainer()

    def DataIngest(self):
        self.job_data_cleaner.clean_data()

    def DataTransform(self):
        self.job_data_processor.process_data()
        self.job_data_processor.save_data()

    def TrainModel(self):
        self.model_trainer.run()