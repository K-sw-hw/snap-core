#Importa librerie


import cv2
import mediapipe as mp
import math
import data
import serial

import tkinter as tk
from tkinter import ttk, messagebox

from pyedo import edo

myedo = edo('192.168.12.1')
myedo.stepByStepOff()
myedo.moveGripper(0)

from PIL import Image, ImageTk  # Correct import for Image and ImageTk

from intro import show_intro
show_intro()

#crea Tkinter root
root = tk.Tk()
root.title("Riconoscimento gestuale")


#Inizializza modulo di riconoscimento della mano
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

#Inizializza output
mp_drawing = mp.solutions.drawing_utils

#Apri telecamera (0 = telecamera di default)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Errore nell'apertura della webcam")
except Exception as e:
    messagebox.showerror(f"Errore nell'apertura del flusso video: {e}")
    root.destroy()  # Close the Tkinter window if the camera can't be opened

_, frame = cap.read()
frame_height, frame_width, _ = frame.shape
root.geometry(f"{frame_width}x{frame_height}")

canvas = tk.Canvas(root, width=frame_width, height=frame_height)
canvas.pack(side=tk.BOTTOM)


"""
Crea slicer per cambiare valore threshold
"""
threshold_value = tk.DoubleVar(value=0.2)

threshold_slider = tk.Scale(
    root,
    from_=0.1, to=0.5,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    label="Threshold",
    variable=threshold_value
)
threshold_slider.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10) #Posizione slicer

def mapHand(mp_hands, hand_landmarks):
    try:
        #thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
        #thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP] 
        #thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] 

        #index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
        #index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
        #index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
        #middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        #middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP] 
        #middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] 

        #ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
        #ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
        #ring_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
        ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

        #pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
        #pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
        #pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    except Exception as e:
        messagebox.showerror(f"Errore nella mappatura della mano: {e}")
    return thumb_tip,index_finger_tip,middle_finger_tip,ring_finger_tip,pinky_tip

def GestureRecognizer(thumb_tip, index_finger_tip, ring_finger_tip):
    """
    Riconoscimento mano aperta/chiusa
    """

    distance_thumb_index = math.sqrt((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) #Formula distanza euclidea

    distance_thumb_ring = math.sqrt((thumb_tip.x - ring_finger_tip.x) ** 2 +  (thumb_tip.y - ring_finger_tip.y) ** 2)

    threshold = threshold_value.get()

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
    cv2.putText(frame, distance_text, (10, 60), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

def CalculateCenter(mp_hands, mp_drawing, frame, hand_landmarks, wrist, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
    """
    Calcolo punto centrale della mano
    """

    palm_center_x = int((wrist.x) * frame.shape[1])
    palm_center_y = int((wrist.y) * frame.shape[0])

    palm_center_x = int((wrist.x + index_finger_tip.x + middle_finger_tip.x + ring_finger_tip.x + pinky_tip.x) / 5 * frame.shape[1])
    palm_center_y = int((wrist.y + index_finger_tip.y + middle_finger_tip.y + ring_finger_tip.y + pinky_tip.y) / 5 * frame.shape[0])

    palm_center_text = f"X: {int(palm_center_x)} Y: {int(palm_center_y)}"

    robotX = palm_center_x

    #Aggiorna dato
    data.palm_center = (palm_center_x, palm_center_y)

            #Disegna pallina
    cv2.circle(frame, (palm_center_x, palm_center_y), 10, (0, 0, 255), -1)

            #Mostra scritta
    cv2.putText(frame, palm_center_text, (10, 90), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

            #Mostra output
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


"""
Loop principale
"""
def update_video_stream():
    ret, frame = cap.read()

    if not ret:
        return

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

    #Mostra output
            if gesture == "Mano aperta":
    	        myedo.moveGripper(80)
            else:
                myedo.moveGripper(0)

    #Converti i frame in modo che possano essere usati da Tkinter
    img = Image.fromarray(frame)  # Converti frame ad immagine
    imgtk = ImageTk.PhotoImage(image=img)  # Converti immagine a formato supportato (ImageTk)
    
    #Aggiorna lo schermo
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
    canvas.imgtk = imgtk  #Evita di accumulare frame
    
    #Aggiorna il flusso ogni 10 millisecondi
    root.after(10, update_video_stream)       


"""
Avvia subroutine principali
"""
#Inizia flusso
update_video_stream()

#Apri Finestra
root.mainloop()

#Richiama funzione e finestra di dialogo
cap.release()
cv2.destroyAllWindows()
