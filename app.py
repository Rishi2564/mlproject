from flask import Flask, request, render_template
import os
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

predict_pipeline = PredictPipeline()  # load once

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method == 'GET':
            return render_template('home.html')

        print("FORM DATA:", request.form)

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score', 0)),
            writing_score=float(request.form.get('writing_score', 0))
        )

        pred_df = data.get_data_as_data_frame()
        print("DATAFRAME:", pred_df)

        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])

    except Exception as e:
        print("ERROR:", e)
        return str(e), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
