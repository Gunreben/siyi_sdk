# GimbalCoreController.py

import sys
import os
from time import sleep

# Adjust the import path if necessary
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from siyi_sdk import SIYISDK

class GimbalController:
    def __init__(self, server_ip="192.168.144.25", port=37260):
        """
        Initializes the GimbalController with the specified server IP and port.

        Args:
            server_ip (str): The IP address of the gimbal server.
            port (int): The port number for the connection.
        """
        self.server_ip = server_ip
        self.port = port
        self.cam = SIYISDK(server_ip=self.server_ip, port=self.port)
        self.connected = False

    def connect(self):
        """
        Establishes a connection to the gimbal.

        Returns:
            bool: True if connection was successful, False otherwise.
        """
        print("Attempting to connect to the gimbal...")
        if not self.cam.connect():
            print("Failed to connect to the gimbal.")
            return False
        self.cam.requestHardwareID()  # Important to get the angles limits defined in cameras.py
        sleep(1)
        self.connected = True
        print("Connected to the gimbal successfully.")
        return True

    def disconnect(self):
        """
        Closes the connection to the gimbal.
        """
        if self.connected:
            self.cam.disconnect()
            self.connected = False
            print("Disconnected from the gimbal.")

    def set_angles(self, yaw_deg, pitch_deg):
        """
        Sets the gimbal's yaw and pitch angles.

        Args:
            yaw_deg (float): The target yaw angle in degrees.
            pitch_deg (float): The target pitch angle in degrees.

        Returns:
            bool: True if the angles were set successfully, False otherwise.
        """
        if not self.connected:
            print("Error: Not connected to the gimbal.")
            return False

        # Validate angles based on the gimbal's specifications
        if not self._validate_angles(yaw_deg, pitch_deg):
            return False

        self.cam.requestSetAngles(yaw_deg, pitch_deg)
        print(f"Gimbal angles set to yaw: {yaw_deg}°, pitch: {pitch_deg}°")
        return True

    def get_attitude(self):
        """
        Retrieves the current attitude (yaw, pitch, roll) of the gimbal.

        Returns:
            tuple: A tuple containing the yaw, pitch, and roll angles.
        """
        if not self.connected:
            print("Error: Not connected to the gimbal.")
            return None
        if self.cam.getAttitude()[1] <= 0:
            attitude = (self.cam.getAttitude()[0], 180.0 - self.cam.getAttitude()[1], self.cam.getAttitude()[2])
        else:
            attitude = (self.cam.getAttitude()[0], -180.0 - self.cam.getAttitude()[1], self.cam.getAttitude()[2])
        	
        print(f"Current gimbal attitude: yaw={attitude[0]}°, pitch={attitude[1]}°, roll={attitude[2]}°")
        return attitude

    def _validate_angles(self, yaw_deg, pitch_deg):
        """
        Validates the yaw and pitch angles.

        Args:
            yaw_deg (float): The target yaw angle in degrees.
            pitch_deg (float): The target pitch angle in degrees.

        Returns:
            bool: True if angles are within valid range, False otherwise.
        """

        YAW_MIN, YAW_MAX = -135.0, 135.0
        PITCH_MIN, PITCH_MAX = -90.0, 25.0

        if not (YAW_MIN <= yaw_deg <= YAW_MAX):
            print(f"Error: Yaw angle {yaw_deg}° is out of range ({YAW_MIN}° to {YAW_MAX}°).")
            return False

        if not (PITCH_MIN <= pitch_deg <= PITCH_MAX):
            print(f"Error: Pitch angle {pitch_deg}° is out of range ({PITCH_MIN}° to {PITCH_MAX}°).")
            return False

        return True

def main():
    controller = GimbalController()
    if controller.connect():
        # Example usage; you can modify these angles as needed
        target_yaw_deg = 0.5
        target_pitch_deg = -10.0

        if controller.set_angles(target_yaw_deg, target_pitch_deg):
            controller.get_attitude()

        controller.disconnect()

if __name__ == "__main__":
    main()

