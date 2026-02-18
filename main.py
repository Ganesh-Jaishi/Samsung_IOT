# ============================================================================
# main.py - Main Execution File
# Real-Time Intrusion Detection System with Cloud Integration & Web Dashboard
# ============================================================================

import RPi.GPIO as GPIO
import time
import sys
from threading import Thread

# Set GPIO mode immediately after import to avoid conflicts
GPIO.setmode(GPIO.BCM)
print("[SYSTEM] GPIO mode set to BCM numbering")

from config import (
    DISTANCE_THRESHOLD, MAIN_LOOP_DELAY, SYSTEM_STARTUP, SYSTEM_SHUTDOWN
)
from sensors import SensorManager
from alerts import AlertManager
from display import DisplayManager
from flask_app import initialize_flask_app, start_flask_server

# ============================================================================
# INTRUSION DETECTION SYSTEM CLASS
# ============================================================================

class IntrusionDetectionSystem:
    """
    Main Intrusion Detection System Controller
    
    Coordinates all system components:
    - Sensor monitoring (PIR motion, ultrasonic distance)
    - Alert triggers (LED activation)
    - Display updates (LCD status)
    - Real-time intrusion detection
    """
    
    def __init__(self):
        """Initialize the intrusion detection system"""
        print("\n" + "=" * 70)
        print("  REAL-TIME INTRUSION DETECTION SYSTEM FOR RASPBERRY PI 4")
        print("  WITH CLOUD INTEGRATION & WEB DASHBOARD")
        print("=" * 70 + "\n")
        
        try:
            # GPIO mode already set at module level
            print("[SYSTEM] GPIO mode already configured\n")
            
            # Initialize all system components
            print("[SYSTEM] Initializing components...")
            self.sensor_manager = SensorManager()
            self.alert_manager = AlertManager()
            self.display_manager = DisplayManager()

            # Initialize Flask app with system components (no ThingSpeak)
            initialize_flask_app(
                self.sensor_manager,
                self.alert_manager,
                self.display_manager
            )
            
            # Start Flask server in background thread
            from flask_app import start_flask_server
            from threading import Thread
            flask_thread = Thread(target=start_flask_server, daemon=True)
            flask_thread.start()
            print("[SYSTEM] Flask web server started in background")
            print("[SYSTEM] Access dashboard at: http://localhost:5000")
            
            self.running = True
            self.cycle_count = 0
            
            print("\n[SYSTEM] All components initialized successfully!")
            print("[SYSTEM] Starting monitoring immediately...\n")
            
        except Exception as e:
            print(f"\n[ERROR] System initialization failed: {e}")
            self.display_manager.show_error("INIT_ERROR", str(e))
            self.cleanup()
            sys.exit(1)
    
    def monitor_restricted_area(self):
        """
        Main monitoring loop - Continuous real-time intrusion detection
        
        Workflow:
        1. Read sensors (PIR motion, ultrasonic distance)
        2. Check for intrusion condition (motion AND distance < threshold)
        3. Trigger alerts if intrusion detected
        4. Update display with current status
        5. Repeat indefinitely
        """
        print("\n[SYSTEM] Starting restricted area monitoring...")
        print("[SYSTEM] Press Ctrl+C to stop the system\n")
        
        # Show startup message on display
        self.display_manager.show_startup()
        
        try:
            # Main monitoring loop - runs indefinitely
            while self.running:
                try:
                    # Step 1: Read sensor data (PIR, Ultrasonic, DHT only)
                    motion_detected, distance, temperature, humidity = self.sensor_manager.read_sensors()

                    # Handle None values from DHT sensor (can fail occasionally)
                    if temperature is None:
                        temperature = 0.0
                    if humidity is None:
                        humidity = 0.0

                    # Step 2: Check intrusion condition
                    # Intrusion = PIR motion detected AND distance below threshold
                    intrusion = self.alert_manager.check_intrusion(
                        motion_detected, distance, DISTANCE_THRESHOLD
                    )

                    # Step 3: Update alert system based on intrusion status
                    self.alert_manager.update_status(intrusion)

                    # Step 4: Update LCD display
                    self.display_manager.update_display(
                        intrusion, motion_detected, distance
                    )

                    # Log cycle information (for debugging)
                    if self.cycle_count % 10 == 0:  # Log every 10 cycles
                        temp_str = f"{temperature:.1f}" if temperature is not None else "N/A"
                        hum_str = f"{humidity:.1f}" if humidity is not None else "N/A"
                        dist_str = f"{distance:.2f}" if distance >= 0 else "Invalid"

                        log_message = (
                            f"[CYCLE {self.cycle_count}] "
                            f"Motion={motion_detected} | "
                            f"Distance={dist_str}cm | "
                            f"Temp={temp_str}°C | "
                            f"Humidity={hum_str}% | "
                            f"Intrusion={intrusion}"
                        )
                        print(log_message)
                    
                    self.cycle_count += 1
                    
                    # Step 5: Delay before next monitoring cycle
                    time.sleep(MAIN_LOOP_DELAY)
                
                except KeyboardInterrupt:
                    # User pressed Ctrl+C
                    print("\n\n[SYSTEM] Keyboard interrupt received!")
                    self.running = False
                    break
                
                except Exception as e:
                    # Handle any runtime errors
                    print(f"[ERROR] Error during monitoring cycle: {e}")
                    time.sleep(1)  # Brief pause before retrying
        
        except Exception as e:
            print(f"[ERROR] Fatal error in monitoring loop: {e}")
            self.display_manager.show_error("RUNTIME_ERROR", str(e))
    
    def cleanup(self):
        """
        System cleanup and shutdown
        Safely releases all GPIO resources and components
        """
        print("\n[SYSTEM] Initiating system shutdown...")
        print("[SYSTEM] Cleaning up resources...\n")
        
        try:
            # Stop cloud upload thread
            if hasattr(self, 'cloud_thread') and self.cloud_thread:
                self.cloud_thread.stop()
            
            # Show shutdown message on display
            self.display_manager.show_shutdown()
            
            # Clean up all components in reverse order
            self.alert_manager.cleanup()
            self.sensor_manager.cleanup()
            # self.thingspeak_logger.cleanup()  # Removed - no ThingSpeak
            self.display_manager.cleanup()
            
            # Clean up GPIO
            GPIO.cleanup()
            print("[GPIO] GPIO cleaned up successfully")
            
            print("\n[SYSTEM] System shutdown complete")
            print("=" * 70 + "\n")
        
        except Exception as e:
            print(f"[ERROR] Error during cleanup: {e}")
        
        finally:
            # Ensure program exits
            sys.exit(0)
    
    def run(self):
        """
        Start the intrusion detection system
        Main entry point for system execution
        """
        try:
            self.monitor_restricted_area()
        
        except KeyboardInterrupt:
            print("\n[SYSTEM] System interrupted by user")
        
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
        
        finally:
            self.cleanup()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point of the program
    Creates and runs the intrusion detection system
    """
    system = IntrusionDetectionSystem()
    system.run()


# ============================================================================
# PROGRAM EXECUTION
# ============================================================================

if __name__ == "__main__":
    main()

# ============================================================================
# END OF MAIN MODULE
# ============================================================================
