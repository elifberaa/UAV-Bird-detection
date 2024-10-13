from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from ultralytics import YOLO
import os
import shutil
import glob
import base64
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', max_http_buffer_size=10 * 2000 * 1024)


file_path = r"best.pt"

if os.path.exists(file_path):
    print("File exists")
    model = YOLO(file_path)
else:
    print(f"File not found: {file_path}")

os.makedirs("upload", exist_ok=True)

ZIP_PATH = 'static/images.zip'
EXTRACT_PATH = 'static/'  

if not os.path.exists('static/images'):
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)  
            print(f"{ZIP_PATH} başarıyla çıkarıldı.")
    except zipfile.BadZipFile:
        print(f"{ZIP_PATH} geçersiz bir ZIP dosyası.")
    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")
else:
    print("static/images zaten mevcut. İşlem yapılmadı.")

def get_image_paths(folder_name):
    folder_path = os.path.join('static', 'images', folder_name)  # static/images dizinini kontrol et
    if os.path.exists(folder_path):
        return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('jpg', 'jpeg', 'png'))]
    else:
        print(f"{folder_path} klasörü bulunamadı.")
        return []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/captcha')
def captcha():
    bird_images = get_image_paths('bird')
    drone_images = get_image_paths('drone')
    other_images = get_image_paths('other')

    return render_template('captcha.html', bird_images=bird_images, drone_images=drone_images, other_images=other_images)


@app.route('/components/<component_name>')
def load_component(component_name):
    return render_template(f'components/{component_name}.html')


@app.route('/upload/predict/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join("upload", "predict"), filename)

@socketio.on('upload_image')
def handle_image(data):
    filename = data['filename']
    img_data = data['image'].split(",")[1]  
    img_path = os.path.join("upload", filename)

    # Decode the base64 image and save it to the server
    with open(img_path, "wb") as f:
        f.write(base64.b64decode(img_data))

    try:
        path = "upload"
        folder = glob.glob(os.path.join(path, '*predict*'))

        if folder:
            shutil.rmtree(folder[0])

        # Perform YOLO prediction
        start_time = time.time()
        results = model.predict(source=img_path, save=True, project="upload", name="predict")
        end_time = time.time()
        processing_time = end_time - start_time

        os.remove(img_path)

        if not results or len(results[0].boxes) == 0:
            socketio.emit('no_detection', {'message': 'İHA veya Kuş tespit edilemedi.'})
            return

    except Exception as e:
        socketio.emit('error', {'message': f"Error during prediction: {e}"})
        return

    # Rename the predicted image
    dir_path = "upload\\predict"
    pred_img = os.listdir(dir_path)[0]  # Get the predicted image name
    name, ext = os.path.splitext(pred_img)
    new_name = f"{name}_pred{ext}"  # Create new name with _pred suffix

    old_img_path = os.path.join(dir_path, pred_img)
    new_img_path = os.path.join(dir_path, new_name)

    # Rename the predicted image
    os.rename(old_img_path, new_img_path)

    # Emit the processed image URL back to the client
    socketio.emit('image_processed', {
        'url': f'/upload/predict/{new_name}',
        'processing_time': processing_time 
    })

    
if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5500, debug=True)  

