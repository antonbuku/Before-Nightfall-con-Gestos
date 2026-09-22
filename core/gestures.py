# Equipo 7
# Antón Bukuyemskyy Bukuyemska
# Nicolás Leal Carrillo
# Hugo Alberola López

import cv2
import mediapipe as mp
import numpy as np
import threading
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands  # type: ignore[attr-defined]
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils  # type: ignore[attr-defined]

def calcular_angulo_mano(lm0, lm9):
    """
    Calcula el ángulo en grados respecto a la vertical.
    0° = Mano apuntando hacia arriba
    Valores positivos = Inclinación hacia la derecha
    Valores negativos = Inclinación hacia la izquierda
    """
    dx = lm9.x - lm0.x
    dy = lm9.y - lm0.y  # Y crece hacia abajo en la imagen

    # -dy invierte el eje Y para considerar "arriba" como el sentido positivo
    angulo_rad = np.arctan2(dx, -dy)
    angulo_deg = np.degrees(angulo_rad)
    return angulo_deg

camera = None
latest_gesture = [
    {"left": False, "right": False, "jump": False, "down": False},
    {"left": False, "right": False, "jump": False, "down": False}
]
cam_running = False
show_debug = False

def get_frame():
    """Este bucle se ejecutará en paralelo sin frenar el juego."""
    global camera, latest_gesture, cam_running

    cv2.namedWindow("Cámara Gestos", cv2.WINDOW_NORMAL)

    while cam_running:
        if camera is not None:
            success, frame = camera.read()
            if not success:
                continue
    
            gestures = [
                {"left": False, "right": False, "jump": False, "down": False},
                {"left": False, "right": False, "jump": False, "down": False}
            ]

            angulos_debug = [0.0, 0.0]

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
                # Ordenar las manos de izquierda a derecha en la pantalla
                hands_list = sorted(result.multi_hand_landmarks, key=lambda hand: hand.landmark[0].x)
                for i, hand_landmark in enumerate(hands_list):
                    mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
                    lm = hand_landmark.landmark

                    # Valores customizables
                    angulo_mov = 15
                    distancia_umbral = 0.07

                    # --- Cálculo del Ángulo ---
                    lm0 = lm[0]  # WRIST
                    lm9 = lm[9]  # MIDDLE_FINGER_MCP

                    angulo = calcular_angulo_mano(lm0, lm9)
                    angulos_debug[i] = angulo

                    # --- Lógica de Dirección ---
                    if angulo > angulo_mov:
                        #direccion = "Izquierda"
                        gestures[i]["left"] = True
                    elif angulo < -angulo_mov:
                        #direccion = "Derecha"
                        gestures[i]["right"] = True

                    # --- Lógica de Salto ---
                    lm4 = lm[4]  # THUMB_TIP
                    lm17 = lm[17]  # PINKY_MCP

                    # Calcular la distancia entre el pulgar y el meñique sea menor a una distancia umbral
                    distancia = math.sqrt(
                        (lm4.x - lm17.x) ** 2 + (lm4.y - lm17.y) ** 2 + (lm4.z - lm17.z) ** 2
                    )
                    if distancia < distancia_umbral:
                        gestures[i]["jump"] = True

                    # --- Lógica de Agacharse ---

                    # Calcular que TIP de los dedos está más bajo que el MCP correspondiente
                    # para determinar si la mano está cerrada (agacharse)

                    dedos_cerrados = 0
                    pares_dedos = [(8, 5), (12, 9), (16, 13), (20, 17)]

                    for punta, base in pares_dedos:
                        # Si la coordenada Y de la punta es mayor que la de la base, el dedo está doblado hacia la palma
                        if lm[punta].y > lm[base].y:
                            dedos_cerrados += 1

                    if dedos_cerrados >= 4:
                        gestures[i]["down"] = True

            latest_gesture = gestures

            frame = cv2.flip(frame, 1)

            if show_debug:
                cv2.rectangle(frame, (10, 10), (550, 140), (0, 0, 0), -1)
                cv2.putText(frame, "--- DEBUG MODE ---", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                for i in range(2):
                    # Generar lista de acciones activas de forma dinámica
                    acciones = [k for k, v in gestures[i].items() if v]
                    str_acciones = ", ".join(acciones).title() if acciones else "Repose"
                    
                    texto = f"J{i+1} [Angle: {int(angulos_debug[i]):>3}*] -> {str_acciones}"
                    color = (255, 150, 50) if i == 0 else (100, 255, 100)
                    cv2.putText(frame, texto, (20, 80 + (i * 40)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                   
            cv2.imshow("Cámara Gestos", frame)
            tecla = cv2.waitKey(1)
            if tecla == 9:  # 9 es el código ASCII del Tabulador
                toggle_debug()

def toggle_debug():
    global show_debug
    show_debug = not show_debug

def init_camera():
    """Abre la cámara solo si no estaba ya abierta."""
    global camera, cam_running
    if camera is None:
        camera = cv2.VideoCapture(0)
        cam_running = True

        # Arrancar el hilo que captura frames en segundo plano
        thread = threading.Thread(target=get_frame, daemon=True)
        thread.start()

def release_camera():
    """Libera la cámara si estaba abierta."""
    global camera, cam_running
    cam_running = False
    if camera is not None:
        camera.release()
        camera = None
        cv2.destroyAllWindows()

def get_current_gesture():
    global latest_gesture
    return latest_gesture.copy()
