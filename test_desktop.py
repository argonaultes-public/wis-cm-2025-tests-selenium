import pyautogui
from test_2 import show_inventory_interface
import tkinter as tk
from threading import Thread
import time

class TestDesktop:

    def setup_method(self):
        self.root = tk.Tk()
        self.root.title("Interface de reconnaissance faciale")
        self.root.geometry("1000x600")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def test_grant_access(self):
        screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
        btn_location = pyautogui.locateCenterOnScreen('./assets/btn-compare.png')
        if btn_location:
            print(f'#####{btn_location}')
            pyautogui.click(x=btn_location[0],y=btn_location[1], clicks=2, interval=1, button='left')

    def test_show_inventory(self):
        show_inventory_interface(self.main_frame, 'bob', self.root)
        t1 = Thread(target=self.root.mainloop, daemon=True)
        t1.start()
        screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
        pyautogui.alert(f'{screenWidth}, {screenHeight}')
        time.sleep(3)

