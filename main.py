import launchpad_py as launchpad
import random
import threading
import time

class LaunchpadListener:
    def __init__(self):
        self.lp = launchpad.Launchpad()
        self.running = False

    def connect(self):
        if self.lp.Open(0, "Launchpad S"):
            print("Launchpad S connected")
            self.lp.Reset()  # Clear the launchpad
            self.running = True
        else:
            print("No Launchpad found, please connect your Launchpad.")

    def disconnect(self):
        if self.running:
            self.lp.Reset()
            self.lp.Close()
            self.running = False
            print("Launchpad disconnected")

    def run_listener(self):
        while self.running:
            events = self.lp.ButtonStateXY()
            if events:
                x, y, pressed = events
                if pressed:
                    red = random.randint(0, 127)
                    green = random.randint(0, 127)
                    self.lp.LedCtrlXY(x, y, red, green)
                    print(f"Button ({x},{y}) pressed, lit up with color red:{red}, green:{green}")
            time.sleep(0.1)

    def start(self):
        if not self.running:
            print("No Launchpad connected.")
            return
        # Start the listener in a new thread
        threading.Thread(target=self.run_listener, daemon=True).start()
        print("Event listener started.")

def main():
    launchpad_listener = LaunchpadListener()
    launchpad_listener.connect()
    launchpad_listener.start()

    try:
        # The main program continues to run
        while True:
            print("Main program running...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
        launchpad_listener.disconnect()

if __name__ == "__main__":
    main()
