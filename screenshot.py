import ctypes
import tkinter as tk
import mss
import mss.tools

ctypes.windll.user32.SetProcessDPIAware()


def capture_screen():

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.configure(background="black")

    canvas = tk.Canvas(root, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    rect = None
    start_x = start_y = 0
    end_x = end_y = 0

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect

        start_x = root.winfo_pointerx()
        start_y = root.winfo_pointery()

        rect = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

    def on_mouse_move(event):
        canvas.coords(rect, canvas.coords(rect)[0], canvas.coords(rect)[1], event.x, event.y)

    def on_mouse_up(event):
        nonlocal end_x, end_y

        end_x = root.winfo_pointerx()
        end_y = root.winfo_pointery()

        root.quit()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()

    x1 = min(start_x, end_x)
    y1 = min(start_y, end_y)
    x2 = max(start_x, end_x)
    y2 = max(start_y, end_y)

    width = x2 - x1
    height = y2 - y1

    with mss.mss() as sct:

        monitor = {
            "top": y1,
            "left": x1,
            "width": width,
            "height": height
        }

        screenshot = sct.grab(monitor)

        output = "screen.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output)

    return output