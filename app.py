import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response

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
                for num, hand_landmarks in enumerate(results.multi_hand_landmarks):
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
                    middle_finger_tip = (int(hand_landmarks.landmark[12].x * image_width),
                                         int(hand_landmarks.landmark[12].y * image_height))
                    middle_finger_pip = (int(hand_landmarks.landmark[10].x * image_width),
                                         int(hand_landmarks.landmark[10].y * image_height))
                    ring_finger_tip = (int(hand_landmarks.landmark[16].x * image_width),
                                       int(hand_landmarks.landmark[16].y * image_height))
                    ring_finger_pip = (int(hand_landmarks.landmark[14].x * image_width),
                                       int(hand_landmarks.landmark[14].y * image_height))
                    pinky_tip = (int(hand_landmarks.landmark[20].x * image_width),
                                 int(hand_landmarks.landmark[20].y * image_height))
                    pinky_pip = (int(hand_landmarks.landmark[18].x * image_width),
                                 int(hand_landmarks.landmark[18].y * image_height))

                    thumb_tip = (int(hand_landmarks.landmark[4].x * image_width),
                                 int(hand_landmarks.landmark[4].y * image_height))
                    thumb_ip = (int(hand_landmarks.landmark[3].x * image_width),
                                int(hand_landmarks.landmark[3].y * image_height))
                    thumb_pip = (int(hand_landmarks.landmark[2].x * image_width),
                                 int(hand_landmarks.landmark[2].y * image_height))
                    index_finger_pip = (int(hand_landmarks.landmark[6].x * image_width),
                                        int(hand_landmarks.landmark[6].y * image_height))

                    # Gesto "BIEN" (Pulgar hacia arriba, otros dedos hacia abajo)
                    if thumb_pip[1] - thumb_tip[1] > 0 and thumb_pip[1] - index_finger_tip[1] < 0 \
                        and thumb_pip[1] - middle_finger_tip[1] < 0 and thumb_pip[1] - ring_finger_tip[1]<0 \
                        and thumb_pip[1] - pinky_tip[1] < 0:
                        cv2.putText(image, 'BIEN', (center_x - 50, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.5, (0, 0, 255), 2) 

                    # Gesto "MAL" (Pulgar hacia abajo, otros dedos hacia arriba)
                    elif thumb_pip[1] - thumb_tip[1] < 0 and thumb_pip[1] - index_finger_tip[1] > 0 \
                        and thumb_pip[1] - middle_finger_tip[1] > 0 and thumb_pip[1] - ring_finger_tip[1]>0 \
                        and thumb_pip[1] - pinky_tip[1] > 0:
                        cv2.putText(image, 'MAL', (center_x - 50, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.5, (0, 0, 255), 2)

                    # Gesto "TE AMO" (Pulgar, índice y meñique levantados, otros dedos hacia abajo)
                    elif thumb_pip[1] - thumb_tip[1] > 0 and \
                         index_finger_pip[1] - index_finger_tip[1] > 0 and \
                         middle_finger_tip[1] > middle_finger_pip[1] and \
                         ring_finger_tip[1] > ring_finger_pip[1] and \
                         pinky_pip[1] - pinky_tip[1] > 0:
                        cv2.putText(image, 'TE AMO', (center_x - 100, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.5, (0, 0, 255), 2)

                    # Gesto "PAZ" (Pulgar hacia abajo, índice y medio levantados, otros dedos hacia abajo)
                    elif thumb_pip[1] > thumb_tip[1] and \
                         index_finger_tip[1] < index_finger_pip[1] and \
                         middle_finger_tip[1] < middle_finger_pip[1] and \
                         ring_finger_tip[1] > ring_finger_pip[1] and \
                         pinky_tip[1] > pinky_pip[1]:
                        cv2.putText(image, 'PAZ', (center_x - 50, 200),
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.5, (0, 255, 0), 2)

                    # Gesto "OK" (Pulgar e índice formando un círculo, otros dedos levantados)
                    elif distancia_euclidiana(thumb_tip, index_finger_tip) < 30 and \
                         middle_finger_tip[1] > middle_finger_pip[1] and \
                         ring_finger_tip[1] > ring_finger_pip[1] and \
                         pinky_tip[1] > pinky_pip[1]:
                        cv2.putText(image, 'OK', (center_x - 50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.5, (0, 255, 0), 2)

                    # Gesto "GRACIAS" (Mano abierta con todos los dedos juntos y extendidos)
                    elif thumb_tip[1] < thumb_ip[1] and \
                         index_finger_tip[1] < index_finger_pip[1] and \
                         middle_finger_tip[1] < middle_finger_pip[1] and \
                         ring_finger_tip[1] < ring_finger_pip[1] and \
                         pinky_tip[1] < pinky_pip[1]:
                        cv2.putText(image, 'GRACIAS', (center_x - 100, 200), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                     1.5, (255, 0, 0), 2)

                    # Gesto "ADIOS" (Mano abierta en la frente)
                    elif thumb_tip[1] < thumb_ip[1] and \
                         index_finger_tip[1] < index_finger_pip[1] and \
                         middle_finger_tip[1] < middle_finger_pip[1] and \
                         ring_finger_tip[1] < ring_finger_pip[1] and \
                         pinky_tip[1] < pinky_pip[1]:

                        # Verificar si la mano está en la frente (cerca de la parte superior de la imagen)
                        frente_threshold = image_height * 0.1  # Aproximadamente 10% de la altura de la imagen
                        
                        # Coordenada y del centro de la mano (aproximadamente en la palma)
                        center_hand_y = (thumb_tip[1] + index_finger_tip[1] + middle_finger_tip[1] +
                                         ring_finger_tip[1] + pinky_tip[1]) / 5

                        if center_hand_y < frente_threshold:
                            cv2.putText(image, 'ADIOS', (center_x - 50, 250), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 
                                        1.5, (255, 255, 0), 2)

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

if __name__ == '__main__':
    app.run(debug=True)
