import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        path_to_artifacts = '../../research/'
        self.values_fill_missing = joblib.load(path_to_artifacts + 'X_train_modes.joblib')
        self.encoders = joblib.load(path_to_artifacts + 'encoders.joblib')
        self.model = joblib.load(path_to_artifacts + 'random_forest.joblib')

    def preprocessing(self, input_data):
        # JSON to pandas dataframe
        input_data = pd.DataFrame(input_data, index=[0])
        # fill missing values
        input_data.fillna(self.values_fill_missing)
        # convert categoricals
        for col in ["workclass", "education", "marital-status", "occupation",
                    "relationship", "race", "sex", "native-country"]:
            encoder = self.encoders[col]
            input_data[col] = encoder.transform(input_data[col])

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, predicted_proba):
        if predicted_proba[1] > 0.5:
            label = ">50K"
            return {"probability": predicted_proba[1], "label": label, "status": "OK"}
        else:
            label = "<=50K"
            return {"probability": predicted_proba[0], "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
