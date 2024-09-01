from components.predict import Predict

class PredictPipeline:
    def __init__(self):
        self.model_path = 'artifacts/model_file.p'
        self.scalar_path= 'artifacts/scalar_file.p'
        self.preprocess_data=None
    
    def give_prediction(self, input_data):
        obj=Predict(self.model_path, self.scalar_path)
        obj.load_model()
        self.preprocess_data = obj.preprocess(input_data)
        return obj.predict(self.preprocess_data)


