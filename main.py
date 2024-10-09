#Importa librerie

import cv2
import mediapipe as mp
import math
import data

#Inizializza modulo di riconoscimento della mano
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

#Inizializza output
mp_drawing = mp.solutions.drawing_utils

#Apri telecamera (0 = telecamera di default)
cap = cv2.VideoCapture(0)

def mapHand(mp_hands, hand_landmarks):
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP] 
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] 

    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
    middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP] 
    middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] 

    ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    return thumb_tip,index_finger_tip,middle_finger_tip,ring_finger_tip,pinky_tip

def GestureRecognizer(thumb_tip, index_finger_tip, ring_finger_tip):
    """
    Riconoscimento mano aperta/chiusa
    """

    distance_thumb_index = math.sqrt((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) #Formula distanza euclidea

    distance_thumb_ring = math.sqrt((thumb_tip.x - ring_finger_tip.x) ** 2 +  (thumb_tip.y - ring_finger_tip.y) ** 2)

    threshold = 0.2 #Soglia di riferimento

    if distance_thumb_index < threshold and distance_thumb_ring < threshold:
        gesture = "Mano chiusa"
    else:
        gesture = "Mano aperta"
    return gesture

def CalculateDistance(frame, wrist):
    """
    Calcolo distanza
    """

            #Misura di riferimento: altezza del polso rispetto all'inquadratura
    frame_height, frame_width, _ = frame.shape
    distance_from_camera = (1 - wrist.y) * frame_height #Calcola la distanza in pixel
    distance_text = f"Distanza: {int(distance_from_camera)} px"

    #Aggiorna dato
    data.distance = int(distance_from_camera)

    #Mostra scritta
    cv2.putText(frame, distance_text, (10, 60), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def CalculateCenter(mp_hands, mp_drawing, frame, hand_landmarks, wrist, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
    """
    Calcolo punto centrale della mano
    """

    palm_center_x = int((wrist.x) * frame.shape[1])
    palm_center_y = int((wrist.y) * frame.shape[0])

    palm_center_x = int((wrist.x + index_finger_tip.x + middle_finger_tip.x + ring_finger_tip.x + pinky_tip.x) / 5 * frame.shape[1])
    palm_center_y = int((wrist.y + index_finger_tip.y + middle_finger_tip.y + ring_finger_tip.y + pinky_tip.y) / 5 * frame.shape[0])

    #Aggiorna dato
    data.palm_center = (palm_center_x, palm_center_y)

            #Disegna pallina
    cv2.circle(frame, (palm_center_x, palm_center_y), 10, (0, 0, 255), -1)

            #Mostra output
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


"""
Loop principale
"""
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    #Converti frame in formato RGB
    frame_rbg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Processa frame per riconoscere mani
    results = hands.process(frame_rbg)

    #Controlla se mani sono riconosciute
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            #Estrai coordinate dei punti di riferimento
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST] 

            thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip = mapHand(mp_hands, hand_landmarks) 


            """Richiama subroutine"""

            gesture = GestureRecognizer(thumb_tip, index_finger_tip, ring_finger_tip)

            CalculateDistance(frame, wrist)

            CalculateCenter(mp_hands, mp_drawing, frame, hand_landmarks, wrist, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip)

            #Aggiorna dato
            data.gesture = gesture


            #Mostra scritta
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 3)



    cv2.imshow('Riconsocimento gestuale', frame)

    #Esci se hai premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Richiama funzione e finestra di dialogo
cap.release()
cv2.destroyAllWindows()