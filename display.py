# ============================================================================
# display.py - LCD Display Interface
# Handles text display on 7-inch touch LCD via HDMI
# Uses console/terminal output to LCD framebuffer
# ============================================================================

import os
import time
import subprocess
from config import INTRUSION_MESSAGE, SAFE_MESSAGE, SYSTEM_STARTUP, SYSTEM_SHUTDOWN

# ============================================================================
# LCD DISPLAY CLASS
# ============================================================================

class LCDDisplay:
    """
    7-inch Touch LCD Display Interface
    Displays system status and alerts
    
    Notes:
    - LCD connected via HDMI to Raspberry Pi 4
    - Output can be configured to direct /dev/tty or framebuffer
    - Default: Uses print statements that output to HDMI display
    - For direct framebuffer control, modify device path in config
    """
    
    def __init__(self, enable_framebuffer=False):
        """
        Initialize LCD display
        
        Args:
            enable_framebuffer (bool): Use direct framebuffer control if True
        """
        self.enable_framebuffer = enable_framebuffer
        self.current_message = ""
        self.last_update_time = 0
        self.display_update_interval = 1.0  # Seconds between display updates
        
        print("[DISPLAY] LCD display module initialized")
    
    def clear_screen(self):
        """
        Clear LCD display
        Uses OS-specific clear command
        """
        try:
            # For Linux/Raspberry Pi OS
            os.system('clear')
            print("[DISPLAY] Screen cleared")
        except Exception as e:
            print(f"[ERROR] Failed to clear screen: {e}")
    
    def display_message(self, message, data=None):
        """
        Display message on LCD with optional data
        
        Args:
            message (str): Main message to display
            data (dict): Optional additional data to display
                - distance: Distance reading in cm
                - motion: Motion detection status
                - timestamp: Current timestamp
        """
        try:
            current_time = time.time()
            
            # Only update display at specified interval to avoid flicker
            if (current_time - self.last_update_time) >= self.display_update_interval:
                self.clear_screen()
                
                # Display header
                print("=" * 50)
                print("  INTRUSION DETECTION SYSTEM - RASPBERRY PI 4")
                print("=" * 50)
                print()
                
                # Display main message
                print(f"STATUS: {message}")
                print()
                
                # Display sensor data if provided
                if data:
                    if 'motion' in data:
                        motion_status = "DETECTED" if data['motion'] else "CLEAR"
                        print(f"Motion Detection: {motion_status}")
                    
                    if 'distance' in data:
                        distance = data['distance']
                        if distance > 0:
                            print(f"Distance: {distance:.2f} cm")
                        else:
                            print("Distance: No valid reading")
                    
                    if 'timestamp' in data:
                        print(f"Time: {data['timestamp']}")
                
                print()
                print("=" * 50)
                
                self.current_message = message
                self.last_update_time = current_time
        
        except Exception as e:
            print(f"[ERROR] Failed to display message: {e}")
    
    def show_intrusion_alert(self, distance, timestamp):
        """
        Display intrusion alert on LCD
        
        Args:
            distance (float): Distance to detected object (cm)
            timestamp (str): Time of intrusion detection
        """
        data = {
            'motion': True,
            'distance': distance,
            'timestamp': timestamp
        }
        self.display_message(INTRUSION_MESSAGE, data)
    
    def show_area_safe(self, distance, timestamp):
        """
        Display "area safe" status on LCD
        
        Args:
            distance (float): Distance reading (cm)
            timestamp (str): Current timestamp
        """
        data = {
            'motion': False,
            'distance': distance,
            'timestamp': timestamp
        }
        self.display_message(SAFE_MESSAGE, data)
    
    def show_startup_message(self):
        """Display system startup message"""
        self.clear_screen()
        print("=" * 50)
        print("  INTRUSION DETECTION SYSTEM - RASPBERRY PI 4")
        print("=" * 50)
        print()
        print(f"STATUS: {SYSTEM_STARTUP}")
        print()
        print("Initializing sensors and alert system...")
        print("Please wait...")
        print()
        print("=" * 50)
        time.sleep(2)
    
    def show_shutdown_message(self):
        """Display system shutdown message"""
        self.clear_screen()
        print("=" * 50)
        print("  INTRUSION DETECTION SYSTEM - RASPBERRY PI 4")
        print("=" * 50)
        print()
        print(f"STATUS: {SYSTEM_SHUTDOWN}")
        print()
        print("Cleaning up resources and exiting...")
        print("Thank you for using this system")
        print()
        print("=" * 50)
    
    def show_error_message(self, error_code, error_description):
        """
        Display error message on LCD
        
        Args:
            error_code (str): Error code/identifier
            error_description (str): Description of error
        """
        self.clear_screen()
        print("=" * 50)
        print("  INTRUSION DETECTION SYSTEM - ERROR")
        print("=" * 50)
        print()
        print(f"ERROR CODE: {error_code}")
        print(f"DESCRIPTION: {error_description}")
        print()
        print("System will shutdown. Please check connections.")
        print()
        print("=" * 50)
    
    def cleanup(self):
        """Clean up display resources"""
        print("[DISPLAY] LCD display cleaned up")

# ============================================================================
# DISPLAY MANAGER CLASS
# ============================================================================

class DisplayManager:
    """
    Manages LCD display and status updates
    Provides unified interface for all display operations
    """
    
    def __init__(self, enable_framebuffer=False):
        """
        Initialize display manager
        
        Args:
            enable_framebuffer (bool): Use framebuffer mode if True
        """
        self.lcd = LCDDisplay(enable_framebuffer)
        self.display_count = 0
        print("[DISPLAY] Display manager initialized")
    
    def update_display(self, intrusion_detected, motion, distance):
        """
        Update display based on current system status
        
        Args:
            intrusion_detected (bool): Whether intrusion is detected
            motion (bool): PIR motion sensor status
            distance (float): Ultrasonic distance reading (cm)
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if intrusion_detected:
            self.lcd.show_intrusion_alert(distance, timestamp)
        else:
            self.lcd.show_area_safe(distance, timestamp)
        
        self.display_count += 1
    
    def show_startup(self):
        """Show startup message"""
        self.lcd.show_startup_message()
    
    def show_shutdown(self):
        """Show shutdown message"""
        self.lcd.show_shutdown_message()
    
    def show_error(self, error_code, error_description):
        """
        Show error message
        
        Args:
            error_code (str): Error code
            error_description (str): Error description
        """
        self.lcd.show_error_message(error_code, error_description)
    
    def cleanup(self):
        """Clean up display resources"""
        self.lcd.cleanup()
        print("[DISPLAY] Display manager cleaned up")

# ============================================================================
# END OF DISPLAY MODULE
# ============================================================================
