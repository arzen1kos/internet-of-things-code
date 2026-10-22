# LED Blinking System with LCD Display (Python)

This project is a simple Python GPIO control script that simulates an embedded system behaviour using an LED, LCD display, and toggle button.

When the button is switched ON:
- The LCD displays the text `"Blinking"`
- The LED blinks continuously

---

# Technologies Used

- Python
- GPIO Library

---

# Components and Port Assignment

| Component | GPIO Port |
|-----------|------------|
| LED | `0` |
| LCD Display | `1` |
| Toggle Button | `2` |

---

# Script Behaviour

## Button ON
When the toggle button is ON:
1. LCD displays: `Blinking`
2. LED turns ON for 1 second
3. LCD clears temporarily
4. LED turns OFF for 0.5 seconds
5. Process repeats continuously

## Button OFF
When the toggle button is OFF:
- LED remains OFF
- LCD remains blank
- System waits for input

---

# Packet Tracer Workspace Snapshot

Below is the topology workspace used in Packet Tracer.

![Packet Tracer Workspace](https://github.com/arzen1kos/internet-of-things-code/tree/docs/media/lab-1.2.1-workspace-topology-1.png)

---

## Notes
The script runs continuously using a while True loop.
Timing is controlled using Python's sleep() function.
The gpio library handles hardware input and output operations.