from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ Uploads go inside static/uploads/
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Optional: clear previous uploads
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    uploaded_files = request.files.getlist('images')
    title = request.form.get('title')
    theme = request.form.get('theme')
    description = request.form.get('description')

    image_filenames = []
    for file in uploaded_files:
        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_filenames.append(filename)

    return render_template('gallery.html',
                           title=title,
                           theme=theme,
                           description=description,
                           images=image_filenames)

if __name__ == '__main__':
    app.run(debug=True)
