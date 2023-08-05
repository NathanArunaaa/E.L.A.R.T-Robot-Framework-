#E.L.A.R.T Robot Controller Interface By: Nathan Aruna

import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from io import BytesIO
import struct
import pickle

# Function to update the camera feed
def update_camera_feed():
    try:
        while True:
            # Request camera frame from the server
            client_socket.sendall("camera_frame".encode())
            frame_size_data = client_socket.recv(4)
            if not frame_size_data:
                break
            frame_size = struct.unpack('!L', frame_size_data)[0]
            frame_data = b''
            while len(frame_data) < frame_size:
                data = client_socket.recv(frame_size - len(frame_data))
                if not data:
                    break
                frame_data += data

            if len(frame_data) == frame_size:
                # Convert the received bytes to a NumPy array
                frame = pickle.loads(frame_data)

                # Convert the NumPy array to an ImageTk object
                image = Image.fromarray(frame)

                # Resize the image to fit the label
                label_width, label_height = camera_label.winfo_width(), camera_label.winfo_height()
                image = image.resize((1180, 790), Image.ANTIALIAS)

                # Convert the resized image to an ImageTk object
                image = ImageTk.PhotoImage(image)
                
                # Update the label with the new image
                camera_label.config(image=image)
                camera_label.image = image
    except Exception as e:
        print("Error updating camera feed:", e)



# ----------Function to start the camera feed thread----------
def start_camera_thread():
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.daemon = True
    camera_thread.start()
#---------------------------------------------------------------



# -----------Function to send commands to the server-----------
def on_button_click(command):
    print(f"Sending command: {command}")
    client_socket.sendall(command.encode())
#---------------------------------------------------------------



# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's access point
server_address = ('192.168.4.1', 87)  
client_socket.connect(server_address)




# ---------Function to update the temp sensor data----------------
def update_Temp1_data():
    # Replace this with actual sensor data retrieval logic
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp1_data)  # Update the data every 1000ms (1 second)

def update_Temp2_data():
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp2_data)  
    
def update_Temp3_data():
    sensor_reading = "Sensor Data: 123.45"
    Temp1_label.config(text=sensor_reading)
    root.after(1000, update_Temp3_data)  

#---------------------------------------------------------------   



# --------------Function to update the progress bar-------------
def update_progress_etlu():
    value = progress_var_etlu.get() + 10
    if value > 100:
        value = 0
    progress_var_etlu.set(value)
    root.after(1000, update_progress_etlu)
    
def update_progress_battery():
    value = progress_var_battery.get() + 10
    if value > 100:
        value = 0
    progress_var_battery.set(value)
    root.after(1000, update_progress_battery)
#---------------------------------------------------------------  
    
    
root = tk.Tk()
root.title("E.L.A.R.T - Controller")

sensor_frame = tk.Frame(root)
sensor_frame.pack(side=tk.TOP, pady=10)
   
# ---------------------Temperature Lables------------------------
Temp1_label = tk.Label(sensor_frame, fg='white', text="[Temp1: N/A]")
Temp1_label.pack(side=tk.LEFT)

Temp2_label = tk.Label(sensor_frame, fg='white', text="[Temp2: N/A]")
Temp2_label.pack(side=tk.LEFT)

Temp3_label = tk.Label(sensor_frame, fg='white', text="[Temp3: N/A]")
Temp3_label.pack(side=tk.LEFT)
#---------------------------------------------------------------



left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)


#----------------------Left Row Buttons-------------------------
Text1_label = tk.Label(left_frame, fg='white', text="E.L.A.R.T")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)

button_forward = tk.Button(left_frame, fg='red', text="SHUTDOWN", activebackground='tomato', command=lambda: on_button_click("shutdown"))
button_forward.pack(side=tk.TOP, padx=5, pady=5)

button_backward = tk.Button(left_frame, fg='red', text="  REBOOT  ", command=lambda: on_button_click("reboot"))
button_backward.pack(side=tk.TOP, padx=5, pady=5)

button_left = tk.Button(left_frame,  fg='blue', text="   NAV-1   ", command=lambda: on_button_click("nav1"))
button_left.pack(side=tk.TOP, padx=5, pady=5)

button_right = tk.Button(left_frame, fg='blue', text="HEADLIGHT1", command=lambda: on_button_click("headlight1"))
button_right.pack(side=tk.TOP, padx=5, pady=5)

progress_var_etlu = tk.DoubleVar(left_frame)
vertical_progress = ttk.Progressbar(left_frame, orient='vertical', variable=progress_var_etlu, length=200, mode='determinate')
vertical_progress.pack(pady=10)

Text1_label = tk.Label(left_frame, fg='white', text="ETLU")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)
#----------------------------------------------------------------



#----------------------------Camera------------------------------
camera_label = tk.Label(root, text="Camera View")
camera_label.pack(side=tk.LEFT, padx=5, pady=5)
#---------------------------------------------------------------



#----------------------Right Row Buttons-------------------------
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT)

Text1_label = tk.Label(right_frame, fg='white', text="Version 1")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)

button_forward = tk.Button(right_frame, fg='red',text="OVERIDE", command=lambda: on_button_click("overide"))
button_forward.pack(side=tk.TOP, padx=5, pady=5)

button_backward = tk.Button(right_frame, fg='green', text="AUTO", command=lambda: on_button_click("auto"))
button_backward.pack(side=tk.TOP, padx=5, pady=5)

button_left = tk.Button(right_frame, fg='blue', text="  NAV-2  ", command=lambda: on_button_click("nav2"))
button_left.pack(side=tk.TOP, padx=5, pady=5)

button_right = tk.Button(right_frame, fg='blue', text="HEADLIGHT2", command=lambda: on_button_click("headlight2"))
button_right.pack(side=tk.TOP, padx=5, pady=5)

progress_var_battery = tk.DoubleVar(right_frame)
vertical_progress = ttk.Progressbar(right_frame, orient='vertical', variable=progress_var_battery, length=200, mode='determinate')
vertical_progress.pack(pady=10)

Text1_label = tk.Label(right_frame, fg='white', text="Battery Level")
Text1_label.pack(side=tk.TOP, padx=5, pady=5)
#----------------------------------------------------------------





update_progress_etlu() 
update_progress_battery()
start_camera_thread()

# Run the Tkinter event loop
root.mainloop()
