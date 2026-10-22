from gpio import *
from time import *

clicked_button = False
BUTTON_PORT = 0
LED1_PORT = 1
LED2_PORT = 2

def button_event():
	""" Alters button's function after a click is detected """
	print('Button event.')
	
	global clicked_button
	button_val = digitalRead(BUTTON_PORT)
	
	# Button event detected, switch button's function
	if button_val == HIGH:
		clicked_button = not clicked_button

 
def flash_led():
	""" Flashes the led """
	digitalWrite(LED1_PORT,HIGH)
	sleep(0.25)
	
	digitalWrite(LED2_PORT,HIGH)
	sleep(0.25)
	
	digitalWrite(LED1_PORT,LOW)
	sleep(0.2)
	digitalWrite(LED2_PORT,LOW)
	sleep(0.25)
 
def main():
	""" Triggers flash_led() function according to the current set of button's function """
	print('Starting ...') 
	while True:
		if clicked_button == True:
			flash_led()
		else:
			sleep(0.5)
			
if __name__ == "__main__":
    add_event_detect(BUTTON_PORT, button_event) 
    main()