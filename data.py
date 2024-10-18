import serial, time

#Qui vengono memorizzate le variabili globali

#Variabili globali
gesture = ""
distance = 0
palm_center = (0, 0)

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Porta seriale non disponibile: {e}")
    arduino = None

def send_data():
    if arduino is not None:
        data_string = f"{gesture}.{distance}.{palm_center[0]}.{palm_center[1]}"
        
        try:
            arduino.write(data_string.encode())
        except Exception as e:
            print(f"Errore nella trasmissione dati: {e}")

