from gpio import *
from time import *

LED_PORT = 0
LCD_PORT = 1
BUTTON_PORT = 2

LCD_TEXT = "Blinking"

def main():
	""" Displays a text and switches the LED on intermittently after the Toggle push button is switched ON. """
	
	while True:
		if digitalRead(BUTTON_PORT) == HIGH:
			#button_state = 'ON'
			customWrite(LCD_PORT, LCD_TEXT)  
			digitalWrite(LED_PORT, HIGH)
			sleep(1)
			
			# Blinking effect, temporary no display and no light
			customWrite(LCD_PORT, '')
			digitalWrite(LED_PORT, LOW)
			sleep(0.5)
			
		else:
			sleep
			
			
if __name__ == "__main__":
	main()
