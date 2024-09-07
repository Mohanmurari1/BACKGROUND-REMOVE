from flask import Flask, render_template, request, send_from_directory
from rembg import remove
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)

    output_path = os.path.join(OUTPUT_FOLDER, 'output.png')
    with open(input_path, 'rb') as input_image:
        output_image = remove(input_image)

    with open(output_path, 'wb') as output_file:
        output_file.write(output_image)

    return send_from_directory(OUTPUT_FOLDER, 'output.png')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)