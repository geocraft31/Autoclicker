from threading import Thread, Event
import time
from pynput.mouse import Button, Controller


class Autoclicker:
    def __init__(self, delay: float, mouseButton: Button) -> None:
        self.delay = delay
        self.mouse = Controller()
        self.mouseButton = mouseButton
        self.clickingThread = Thread(target=self._clicker, name="Clicker")
        self.stopEvent = Event()
        self.active = False

        
    def start(self):
        self.stopEvent.clear()
        self.active = True
        if not self.clickingThread.is_alive():
            self.clickingThread = Thread(target=self._clicker, name="Clicker")
            self.clickingThread.start()
    
    def stop(self):
        if self.stopEvent.is_set():
            return
        self.active = False
        self.stopEvent.set()
        if self.clickingThread.is_alive():
            self.clickingThread.join()


    def run(self, timeSec: float):
        self.start()
        time.sleep(timeSec)
        self.stop()

    def _clicker(self):
        while not self.stopEvent.is_set():
            self.mouse.click(self.mouseButton)
            time.sleep(self.delay)
