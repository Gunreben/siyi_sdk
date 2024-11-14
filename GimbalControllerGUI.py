# GimbalControllerGUI.py

import tkinter as tk
from tkinter import messagebox
from GimbalCoreController import GimbalController

class GimbalControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gimbal Controller")
        self.controller = GimbalController()

        # Connection Frame
        self.connection_frame = tk.Frame(self.root, padx=10, pady=10)
        self.connection_frame.pack(fill=tk.X)
        
        self.connect_button = tk.Button(self.connection_frame, text="Connect", command=self.connect_to_gimbal)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_button = tk.Button(self.connection_frame, text="Disconnect", command=self.disconnect_from_gimbal, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)

        # Angle Setting Frame
        self.angle_frame = tk.Frame(self.root, padx=10, pady=10)
        self.angle_frame.pack(fill=tk.X)

        tk.Label(self.angle_frame, text="Yaw (degrees):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.yaw_slider = tk.Scale(self.angle_frame, from_=-135.0, to=135.0, orient=tk.HORIZONTAL, length=300, command=self.update_gimbal_angles)
        self.yaw_slider.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.angle_frame, text="Pitch (degrees):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.pitch_slider = tk.Scale(self.angle_frame, from_=-90.0, to=25.0, orient=tk.HORIZONTAL, length=300, command=self.update_gimbal_angles)
        self.pitch_slider.grid(row=1, column=1, padx=5, pady=5)

        # Attitude Frame
        self.attitude_frame = tk.Frame(self.root, padx=10, pady=10)
        self.attitude_frame.pack(fill=tk.X)

        self.get_attitude_button = tk.Button(self.attitude_frame, text="Get Attitude", command=self.get_gimbal_attitude, state=tk.DISABLED)
        self.get_attitude_button.pack(side=tk.LEFT, padx=5)

        self.attitude_label = tk.Label(self.attitude_frame, text="Attitude: yaw=0.0°, pitch=0.0°, roll=0.0°")
        self.attitude_label.pack(side=tk.LEFT, padx=5)

    def connect_to_gimbal(self):
        if self.controller.connect():
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.get_attitude_button.config(state=tk.NORMAL)
            messagebox.showinfo("Connection", "Successfully connected to the gimbal.")
        else:
            messagebox.showerror("Connection", "Failed to connect to the gimbal.")

    def disconnect_from_gimbal(self):
        self.controller.disconnect()
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.get_attitude_button.config(state=tk.DISABLED)
        messagebox.showinfo("Disconnection", "Disconnected from the gimbal.")

    def update_gimbal_angles(self, _=None):
        if self.controller.connected:
            yaw_deg = self.yaw_slider.get()
            pitch_deg = self.pitch_slider.get()
            self.controller.set_angles(yaw_deg, pitch_deg)

    def get_gimbal_attitude(self):
        attitude = self.controller.get_attitude()
        if attitude:
            self.attitude_label.config(text=f"Attitude: yaw={attitude[0]:.2f}°, pitch={attitude[1]:.2f}°, roll={attitude[2]:.2f}°")
        else:
            messagebox.showerror("Error", "Failed to retrieve gimbal attitude.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GimbalControllerGUI(root)
    root.mainloop()
