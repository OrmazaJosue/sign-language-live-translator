import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response
import webbrowser
from threading import Timer

app = Flask(__name__)

# Configuración de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Inicialización de la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

# Función para calcular la distancia euclidiana entre dos puntos
def distancia_euclidiana(punto1, punto2):
    return np.sqrt((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2)

# Función para generar el video en tiempo real
def generar_video():
    with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        max_num_hands=2) as hands:
        while True:
            success, image = cap.read()
            if not success:
                break

            # Preprocesar la imagen para MediaPipe
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Convertir la imagen de nuevo a BGR para OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            image_height, image_width, _ = image.shape
            center_x = image_width // 2

            # Si se detectan manos, analizar la posición de los dedos
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Dibujar los puntos de la mano
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    # Obtener las coordenadas de los puntos de interés
                    index_finger_tip = (int(hand_landmarks.landmark[8].x * image_width),
                                        int(hand_landmarks.landmark[8].y * image_height))
                    pinky_tip = (int(hand_landmarks.landmark[20].x * image_width),
                                 int(hand_landmarks.landmark[20].y * image_height))
                    thumb_tip = (int(hand_landmarks.landmark[4].x * image_width),
                                 int(hand_landmarks.landmark[4].y * image_height))
                    middle_finger_tip = (int(hand_landmarks.landmark[12].x * image_width),
                                         int(hand_landmarks.landmark[12].y * image_height))
                    middle_finger_pip = (int(hand_landmarks.landmark[10].x * image_width),
                                         int(hand_landmarks.landmark[10].y * image_height))

                    # Gesto personalizado: "Darwin es discapacitado" (Detecta la ausencia de dedo medio completo)
                    # Se verifica si el dedo medio está extendido (simulando la falta del dedo)
                    if thumb_tip[1] < index_finger_tip[1] and \
                       thumb_tip[1] < pinky_tip[1] and \
                       distancia_euclidiana(middle_finger_tip, middle_finger_pip) < 20:  # Dedo medio más corto
                        cv2.putText(image, 'Darwin es discapacitado', (center_x - 200, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.2, (255, 0, 0), 2)

            # Codificar la imagen en formato JPEG
            _, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Ruta para mostrar la página web con el video
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para generar el video
@app.route('/video_feed')
def video_feed():
    return Response(generar_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Función para abrir automáticamente el navegador en http://localhost:5000
def open_browser():
    webbrowser.open_new("http://localhost:5000")

if __name__ == '__main__':
    # Ejecutar el navegador después de iniciar el servidor
    Timer(1, open_browser).start()
    app.run(debug=True)
