# FOR THE SERVER
from flask import Flask, request, jsonify
from flask import render_template
from PIL import Image
from io import BytesIO
import base64
import json
from flask_cors import CORS
from mlq.queue import MLQ



def create_app():
    app = Flask(__name__)

    mlq = MLQ('cloth_recommendation', 'localhost', 6379, 0)
    mlq.create_reaper(call_how_often=30, job_timeout=100, max_retries=5)
    CALLBACK_URL = 'http://localhost:5000/callback'
    CORS(app)
    @app.route('/')
    def hello_world():
        return render_template('home.html')

    @app.route('/home')
    def second_version():
        return render_template('home.html')

    @app.route('/getPredictions', methods=['POST'])
    def upload():
        print("GOT REQUEST!")
        gender = request.form['gender']
        occasion = request.form['occasion']
        use_files = request.form['use_files']
        fileList = request.form.getlist('files')
        job_id = mlq.post([occasion, gender, use_files, fileList], CALLBACK_URL)
        return jsonify({'msg': 'Processing. Check back soon.', 'job_id':job_id})

    @app.route('/status/<job_id>', methods=['GET'])
    def get_progress(job_id):
        #print(job_id)
        return jsonify({'msg': mlq.get_progress(job_id)})

    @app.route('/result/<job_id>', methods=['GET'])
    def get_result(job_id):
        job = mlq.get_job(job_id)
        return jsonify({'short_result': job['short_result']})

    @app.route('/callback', methods=['GET'])
    def train_model():
        success = request.args.get('success', None)
        job_id = request.args.get('job_id', None)
        short_result = request.args.get('short_result', None)
        print("We received a callback! Job ID {} returned successful={} with short_result {}".format(
            job_id, success, short_result
        ))
        return 'ok'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
