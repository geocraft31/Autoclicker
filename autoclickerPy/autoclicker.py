from threading import Thread, Event
import time
from pynput.mouse import Button, Controller


class Autoclicker:
    """
    Autoclicker object.

    ### Arguments

    delay: float
        Delay between each click
    
    mouseButton: pynupt.mouse.Button
        The mouse button that the autoclicker targets

    Attributes
    ----
    active: bool
        The current state of the autoclicker

    Methods
    ----
    start()
        Starts the autoclicker
    
    stop()
        Stops the autoclicker

    run( time: float )
        Runs the autoclicker for `time` seconds

    """
    def __init__(self, delay: float) -> None:

        self.delay = delay
        self._mouse = Controller()
        self._clickingThread = Thread(target=self._clicker, name="Clicker")
        self._stopEvent = Event()
        self.active = False

        
    def start(self, button: Button = Button.left):
        """Start the autoclicker

        Args:
            button (Button, optional): The mouse button to click. Defaults to Button.left.
        """
        self.mouseButton = button
        self._stopEvent.clear()
        self.active = True
        if not self._clickingThread.is_alive():
            self._clickingThread = Thread(target=self._clicker, name="Clicker")
            self._clickingThread.start()
    
    def stop(self):
        """Stops the autoclicker object
        """
        if self._stopEvent.is_set():
            return
        self.active = False
        self._stopEvent.set()
        if self._clickingThread.is_alive():
            self._clickingThread.join()


    def run(self, timeSec: float, button: Button = Button.left):
        """Starts the autoclicker for `timeSec` seconds

        Args:
            timeSec (float): The time the autoclicker is running
            button (Button, optional): The mouse button to click. Defaults to Button.left.
            
        Raises:
            ValueError: if `timeSec` <= 0
        """
        if timeSec <= 0:
            raise ValueError("Variable `timeSec` can't be 0 or below")
        self.mouseButton = button
        self.start()
        now = time.time()
        while time.time() - now < timeSec:
            if not self.active:
                return
            time.sleep(0.01)
        self.stop()

    def _clicker(self):
        # private! Not for public use
        
        while not self._stopEvent.is_set():
            self._mouse.click(self.mouseButton)
            time.sleep(self.delay)
