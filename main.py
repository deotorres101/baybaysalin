from flask import Flask, render_template, request
#from flask_ngrok import run_with_ngrok
from model_processing import Model
from image_processing import ImageProcessing
from tts_api import TTSHandler
from PIL import Image
import base64
import io
import tensorflow as tf

DETECT_PATH = 'models/detect_dialect.h5'
#MODEL_PATH = ['models/hanunuo_model_vgg16.h5', 'models/tagalog_model_vgg16.h5', 'models/tagbanwa_model_vgg16.h5']
MODEL_PATH = ['models/hanunuo_model.h5', 'models/tagalog_model.h5', 'models/tagbanwa_model.h5']
CLASS_PATH = ['hanunuo_classes.txt', 'tagalog_classes.txt', 'tagbanwa_classes.txt']
DIALECT = ['Hanunuo', 'Tagalog', 'Tagbanwa']
API_KEY = '14f3d8372a47419ca51681c347744614'
app = Flask(__name__)
#run_with_ngrok(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        f = request.files['img']
        img = Image.open(io.BytesIO(f.read()))
        out, dialect = process_input(img)
        i = io.BytesIO()
        img.save(i, "PNG")
        enc_img = base64.b64encode(i.getvalue())
        tts = TTSHandler(API_KEY)
        speech = tts.convert_to_speech(out)
        return render_template('display.html', img=enc_img.decode('utf-8'), out=out, tts=speech, dialect=dialect)
    else:
        return render_template('capture.html')

def process_input(input_img):
    img = ImageProcessing()

    # Comment out below if you want to test models manually
    #Convert Image to Array
    bounding_boxes = img.get_rect(input_img)
    char = img.separate_chars(input_img, bounding_boxes, True)

    # Comment out below if you want to test models manually
    #Detect Dialect
    #dialect_detect = Model(DETECT_PATH)

    #detect dialect using the first character
    #dialect = dialect_detect.get_prediction(char[0])
    dialect = 1

    # change dialect var to corresponding index number for MODEL_PATH and CLASS_PATH
    #OCR
    ocr = Model(MODEL_PATH[dialect])
    print(MODEL_PATH[dialect])

    chars = img.separate_chars(input_img, bounding_boxes)
    translation = ocr.get_prediction(chars, class_file=CLASS_PATH[dialect])

    return translation, DIALECT[dialect]

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()       # tried with debug=true but not working with ngrok
