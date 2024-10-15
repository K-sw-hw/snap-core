from data import gesture, distance, palm_center
from pyedo import edo

import time
import math

myedo = edo('192.168.12.1') # Crea instanza oggetto eDO
init7Axes()

if (gesture = "Mano aperta"):
  moveGripper(70)
else if (gesture = "Mano chiusa"):
  moveGripper(10)
else:
  moveGripper(0)
