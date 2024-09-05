import tkinter
from tkinter import *


def on_closing():
    """
    Stops the main loop of the GUI when the window is closed.

    This function is used as a callback for the WM_DELETE_WINDOW protocol.
    It sets the global variable `running` to False, which stops the main
    loop of the GUI.
    """
    global running
    running = False


# GUI
root = tkinter.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)
root.title("Frame Recorder")
root.geometry("800x400+500+100")
canvas = Canvas(
    root,
    bg="#4392F1",
    height=400,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)
background_img = PhotoImage(file=f"assets/background.png")
background = canvas.create_image(400.0, 200.0, image=background_img)
header = canvas.create_text(
    400.0, 91.0, text="Frame Recorder", fill="#ECE8EF", font=("Roboto-Bold", int(30.0))
)
create_label = canvas.create_text(
    203.5, 174.5, text="create an", fill="#ECE8EF", font=("Roboto-Bold", int(16.0))
)
video_label = canvas.create_text(
    590.5, 174.5, text="fps video", fill="#ECE8EF", font=("Roboto-Medium", int(16.0))
)
switch = tkinter.Scale(
    from_=100,
    to=200,
    orient=tkinter.HORIZONTAL,
    length=200,
    activebackground="#C25993",
    bg="#C25993",
    highlightcolor="#C25993",
    highlightbackground="#C25993",
    fg="white",
    troughcolor="white",
)

menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
about_menu = Menu(menubar, tearoff=0)
video_format_menu = Menu(file_menu, tearoff=0)
monitor_menu = Menu(file_menu, tearoff=0)

mp4_format = tkinter.BooleanVar()
mp4_format.set(True)
avi_format = tkinter.BooleanVar()

file_menu.add_cascade(label="Video Format", menu=video_format_menu)
file_menu.add_cascade(label="Monitor Selection", menu=monitor_menu)
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="About", menu=about_menu)

start_img = PhotoImage(file=f"assets/start.png")
start = Button(image=start_img, borderwidth=0, highlightthickness=0, relief="flat")
pause_img = PhotoImage(file=f"assets/pause.png")
pause = Button(image=pause_img, borderwidth=0, highlightthickness=0, relief="flat")
end_img = PhotoImage(file=f"assets/end.png")
end = Button(image=end_img, borderwidth=0, highlightthickness=0, relief="flat")
info = canvas.create_text(
    400.0,
    342.5,
    text="Start Recording",
    fill="#ECE8EF",
    font=("Roboto-Medium", int(16.0)),
)

# When started
end["state"] = "disabled"
pause["state"] = "disabled"
