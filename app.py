from flask import Flask, render_template, request, send_file
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        operation = request.form.get('operation')
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            img = cv2.imread(file_path)

            if operation == 'grayscale':
                processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif operation == 'blur':
                processed_img = cv2.GaussianBlur(img, (15,15), 0)
            elif operation == 'edge':
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                processed_img = cv2.Canny(gray, 100, 200)
            else:
                processed_img = img

            processed_path = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)
            cv2.imwrite(processed_path, processed_img)

            return send_file(processed_path, mimetype='image/jpeg')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)