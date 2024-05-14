import os
import dlib
from secret_settings import rtsp_path

# Подключение моделей
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

SHAPE_MODEL_PATH = os.path.join(MODEL_DIR, 'shape_predictor_68_face_landmarks.dat')
FACE_MODEL_PATH = os.path.join(MODEL_DIR, 'dlib_face_recognition_resnet_model_v1.dat')

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(SHAPE_MODEL_PATH)
face_recognizer = dlib.face_recognition_model_v1(FACE_MODEL_PATH)
cutting_accuracy = 10

# Настройки отправки
timeout = 30  # Время которое мы будем ждать чтобы отправить фотографию человека заново

# rstp настройки
rtsp = False
rtsp_paths = rtsp_path
