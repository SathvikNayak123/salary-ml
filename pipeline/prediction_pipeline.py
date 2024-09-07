from components.predict import Predict

class PredictPipeline:
    def __init__(self):
        self.encoder_path= 'artifacts/onehot_encoder.p'
        self.model_path = 'artifacts/model_file.p'
        self.scalar_path= 'artifacts/scaler_file.p'
        self.preprocess_data=None
    
    def give_prediction(self, input_data):
        obj=Predict(self.encoder_path ,self.model_path, self.scalar_path)
        obj.load_all()
        preprocess_data=obj.preprocess(input_data)
        return obj.predict(preprocess_data)


