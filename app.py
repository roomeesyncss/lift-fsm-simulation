import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk

IDLE = 0
MOVING_UP = 1
MOVING_DOWN = 2
DOOR_OPEN = 3

state = IDLE
current_floor = 0
target_floor = -1

def enter_floor(floor_button_pressed):
    global state, current_floor, target_floor
    if state == IDLE:
        if floor_button_pressed > current_floor:
            target_floor = floor_button_pressed
            state = MOVING_UP
            return "move_up"
        elif floor_button_pressed < current_floor:
            target_floor = floor_button_pressed
            state = MOVING_DOWN
            return "move_down"
    elif state == MOVING_UP:
        if current_floor == target_floor:
            state = DOOR_OPEN
            return "stop, open_door"
        else:
            current_floor += 1
            return "move_up"
    elif state == MOVING_DOWN:
        if current_floor == target_floor:
            state = DOOR_OPEN
            return "stop, open_door"
        else:
            current_floor -= 1
            return "move_down"
    elif state == DOOR_OPEN:
        state = IDLE
        return "close_door"
    return ""

def update_display(output):
    global current_floor, state
    status_label.config(text=f"Output: {output}, Current Floor: {current_floor}, State: {state}")
    if state == IDLE:
        st_text.set("idle")
    elif state == MOVING_UP:
        st_text.set("moving_up")
    elif state == MOVING_DOWN:
        st_text.set("moving_down")
    elif state == DOOR_OPEN:
        st_text.set("door_open")
    floor_var.set(current_floor)

def handle_button_press(floor):
    output = enter_floor(floor)
    update_display(output)
    root.update()
    root.after(1000, lambda: None)

root = ttk.Window(themename="journal")
root.title("Lift FSM Simulation")

st_text = tk.StringVar()
st_text.set("idle")
state_label = ttk.Label(root, text="Current State:", font=("Helvetica", 12))
state_label.grid(row=0, column=0, padx=10, pady=10)
state_display = ttk.Label(root, textvariable=st_text, font=("Helvetica", 12, "bold"))
state_display.grid(row=0, column=1, padx=10, pady=10)

floor_var = tk.IntVar()
floor_var.set(current_floor)
floor_label = ttk.Label(root, text="Current Floor:", font=("Helvetica", 12))
floor_label.grid(row=1, column=0, padx=10, pady=10)
floor_display = ttk.Label(root, textvariable=floor_var, font=("Helvetica", 12, "bold"))
floor_display.grid(row=1, column=1, padx=10, pady=10)

status_label = ttk.Label(root, text="Status: ", font=("Helvetica", 12))
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

button_ctr = ttk.Frame(root)
button_ctr.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
for i in range(7):
    btn = ttk.Button(button_ctr, text=f"Floor {i}", bootstyle=PRIMARY, command=lambda i=i: handle_button_press(i))
    btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)

root.mainloop()
