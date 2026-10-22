# LED Sequencer System (SBC1 ↔ SBC2)
This project implements a simple two-board LED sequencing system using GPIO communication between SBC1 and SBC2. The boards coordinate through digital signals to trigger and acknowledge LED animations.

## Project Overview
**SBC1: Acts as the controller/initiator.**
- Sends a trigger signal to SBC2.
- Waits for a response after initiating a cycle.
**SBC2: Executes the LED sequence.**
- Receives trigger from SBC1.
- Runs a sequential LED animation across multiple pins.
- Sends acknowledgment back to SBC1 after completion.

## Communication Flow
1. SBC1 sends a HIGH pulse → SBC2 input pin.
2. SBC2 detects signal → starts LED sequence.
3. SBC2 flashes LEDs in order (4 → 9).
4. SBC2 sends a short HIGH pulse back to SBC1.
5. SBC1 detects response → resets state and repeats cycle.

## SBC1 Behavior
### Key Pins
- SBC2_PIN_OUT = 1 → sends trigger to SBC2
- SBC2_PIN_IN = 2 → receives response from SBC2
### States
- "Notifying" → sends trigger pulse
- "Listening for response" → waits for SBC2 acknowledgment

### Core Logic
- Sends a 500ms HIGH pulse to SBC2
- Waits 1 second
- Listens for response signal
- Resets cycle once response is received

### Event Handler
`remote_sbc_event()` detects incoming signal from SBC2 and resets state


## SBC2 Behavior
### Key Pins
- `SBC2_PIN_IN` = 1 → receives trigger from SBC1
- `SBC2_PIN_OUT` = 2 → sends response back to SBC1

### LED Pins
Sequential LED output pins:
- `LED_4_PIN` → LED_9_PIN

### State
`active_sbc_state` (Boolean)
- True → LED sequence active
- False → idle

## LED Sequencing
**When triggered:**
1. SBC2 iterates through LED list:
- LED 4 → ON → delay → OFF
- LED 5 → ON → delay → OFF
- ...
- LED 9 → ON → delay → OFF

2. Each LED stays on for:
- `LED_SEQUENCER_DELAY` = 100ms

3. After full sequence:
- SBC2 notifies SBC1 via pulse
- Resets or toggles state depending on SBC1 response


### SBC2 Event Handling
- `remote_sbc_event()` toggles LED sequence state when input signal is HIGH.
- This allows SBC1 to start/stop the LED sequence cycle.

## Timing Summary
| Operation           | Delay   |
| ------------------- | ------- |
| SBC1 trigger pulse  | 500 ms  |
| SBC1 wait cycle     | 1000 ms |
| SBC2 LED step       | 100 ms  |
| SBC2 response pulse | 50 ms   |

---

## Python Script of SBC1

```python
from gpio import *
from time import *


BUTTON_PIN = 0
SBC1_PIN_OUT = 1
SBC1_PIN_IN = 2

alt_button_func = False
start_led_flash = False
resume_led_flash = False


LED_1_PIN = 4
LED_2_PIN = 5
LED_3_PIN = 6
LED_PIN_LIST1 = [LED_1_PIN, LED_2_PIN, LED_3_PIN]

LED_10_PIN = 7
LED_11_PIN = 8
LED_12_PIN = 9
LED_PIN_LIST2 = [LED_10_PIN, LED_11_PIN, LED_12_PIN]

LED_SEQUENCER_DELAY = 1000

def button_event():
	""" Alters button functionality, calls led squencer starter/stopper accordingly"""
	global active_sbc_state,alt_button_func 
	if digitalRead(BUTTON_PIN) == HIGH:
		# Next button press will turn off the sequence
		alt_button_func = not alt_button_func
		start_stop_led_sequence()

	
def remote_sbc_event():
	""" Set the stage to resume led flashing (lower led group) """
	global resume_led_flash
	if digitalRead(SBC1_PIN_IN)== HIGH:
		resume_led_flash = True

		
def start_stop_led_sequence():
	""" Starts/Stops led sequence by changing SBC state to active. """
	global resume_led_flash,start_led_flash
	
	if alt_button_func:
		# Start flashing the upper led group
		start_led_flash = True

	else:
		# Stop the entire sequence
		resume_led_flash = False
		start_led_flash = False


def main():
	""" Mechanism to trigger flash led and sbc2 alert functions. """
	global start_led_flash, resume_led_flash
	while True:
		if start_led_flash == True and resume_led_flash == False:
			resume_led_flash = False
			flash_led(1)
			start_led_flash = notify_remote_sbc()
			
		if alt_button_func == True and resume_led_flash == True:
			print("SBC2 indicates it has finished flashing the leds")
			flash_led(2)
			flash_led(1)
			
			# Stop flash looping (until an SBC2 event is detected)
			start_led_flash = notify_remote_sbc()
		delay(500)

def notify_remote_sbc():
	""" Sends signal to SBC2 """
	print("Telling SBC2 to start flashing the leds")
	digitalWrite(SBC1_PIN_OUT, HIGH)
	delay(50)
	digitalWrite(SBC1_PIN_OUT, LOW)

	return False
	
def flash_led(group):
	""" Flashes the leds according to the group specified by the parameter"""
	if group == 1: 
		# Upper led group
		for aLedPin in LED_PIN_LIST1:
			digitalWrite(aLedPin,HIGH)
			delay(LED_SEQUENCER_DELAY)
			digitalWrite(aLedPin,LOW)
	if group == 2:
		# Lower led group
		for aLedPin in LED_PIN_LIST2:
			digitalWrite(aLedPin,HIGH)
			delay(LED_SEQUENCER_DELAY)
			digitalWrite(aLedPin,LOW)
			
			
			
if __name__ == "__main__":
	add_event_detect(BUTTON_PIN, button_event)
	add_event_detect(SBC1_PIN_IN, remote_sbc_event)
	main()

```

## Python Script of SBC2

```python
from gpio import *
from time import *


SBC2_PIN_IN = 1
SBC2_PIN_OUT = 2

LED_4_PIN = 4
LED_5_PIN = 5
LED_6_PIN = 6
LED_7_PIN = 7
LED_8_PIN = 8
LED_9_PIN = 9

LED_PIN_LIST = [LED_4_PIN, LED_5_PIN, LED_6_PIN, LED_7_PIN, LED_8_PIN,LED_9_PIN]

LED_SEQUENCER_DELAY = 100

active_sbc_state = False

def notify_remote_sbc():
	""" Sends signal to SBC1 """
	digitalWrite(SBC2_PIN_OUT, HIGH)
	delay(50)
	digitalWrite(SBC2_PIN_OUT, LOW)
	return False


def remote_sbc_event():
	""" Set the stage to start led flashing """
	global active_sbc_state
	if digitalRead(SBC2_PIN_IN)== HIGH:
		# Alter current state. Marks the flashing stage commence or stop sequence
		active_sbc_state = not active_sbc_state
	

def flash_led():
	""" Flashes the leds"""
	if active_sbc_state == True:
		for aLedPin in LED_PIN_LIST:
			digitalWrite(aLedPin,HIGH)
			delay(LED_SEQUENCER_DELAY)
			digitalWrite(aLedPin,LOW)
			
		print("Finished flashing leds, notifying SBC1")


def main():
	""" Mechanism to trigger flash led and sbc1 response functions. """
	global active_sbc_state
	while True:
		if active_sbc_state == True:
			print("I've been told to start flashing the leds from SBC1 ")
			flash_led()
			
			# Inform the remote SBC1 to resume flashing
			active_sbc_state = notify_remote_sbc()
			
		delay(1000)

if __name__ == "__main__":
	add_event_detect(SBC2_PIN_IN, remote_sbc_event)
	main()
	
```

## Packet Tracer Workspace Snapshot
Below is the topology workspace used in Packet Tracer.

> **All Iterations**
![Packet Tracer Workspace: : All Iterations](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-workspace-topology-iterations.png)


> **Iteration 5 (Final Iteration)**
![Packet Tracer Workspace: Iteration 5 (Final Iteration)](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-workspace-topology-iteration-5.png)


> **Previous Iterations**
![Packet Tracer Workspace: Iteration 1](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-workspace-topology-iteration-1.png)
![Packet Tracer Workspace: Iteration 2](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-workspace-topology-iteration-2.png)
![Packet Tracer Workspace: Iteration 3](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-workspace-topology-iteration-3.png)

## Demo of the Final Iteration
Below is the project demo of the temperature sensor and heating system using push button.
<video src="https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-5.1.1-iteration-5-demo.mp4" controls></video>


## Future Improvements
- Extend LED patterns (wave, random, binary counter)
- Add safety timeout to prevent stuck states
- Add debounce handling for GPIO inputs
- Replace fixed delays with non-blocking timers
- Add bidirectional state confirmation (ACK/NACK)