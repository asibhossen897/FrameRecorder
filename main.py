import datetime
import webbrowser
import interface
import mss
import numpy as np
import cv2 as cv
import tkinter

status = ""
selected_monitor = None


def find_time():
    """
    Returns a string representing the current date and time in the format
    DD-MM-YYYY-HH-MM-SS.
    """
    x = datetime.datetime.now()
    return x.strftime("%d-%m-%Y-%H-%M-%S")


def edit_checks(clicked):
    """
    Set the state of the other radio button to the opposite of the clicked
    radio button. This is used to ensure that only one of the two radio
    buttons is checked at a time.

    Parameters
    ----------
    clicked : str
        The value of the radio button that was clicked. This is either
        "mp4" or "avi".
    """
    if clicked == "mp4":
        if not interface.mp4_format.get():
            interface.avi_format.set(True)
        else:
            interface.avi_format.set(False)
    elif clicked == "avi":
        if not interface.avi_format.get():
            interface.mp4_format.set(True)
        else:
            interface.avi_format.set(False)


def result_format():
    """
    Returns the file extension for the recorded video based on the selected
    radio button in the GUI.

    Returns
    -------
    str
        The file extension for the recorded video. This is either ".mp4" or
        ".avi".
    """
    if interface.mp4_format.get():
        return ".mp4"
    else:
        return ".avi"


def result_format2():
    """
    Returns the four-character code for the recorded video based on the selected
    radio button in the GUI.

    Returns
    -------
    str
        The four-character code for the recorded video. This is either
        "MP4V" or "XVID".
    """
    if result_format() == ".mp4":
        return "MP4V"
    else:
        return "XVID"


def populate_monitor_menu():
    with mss.mss() as sct:
        monitors = sct.monitors
        for i, monitor in enumerate(monitors):
            # Skip the first monitor entry which might be the virtual screen
            if i == 0:
                continue
            monitor_name = f"Monitor {i} ({monitor['width']}x{monitor['height']})"
            interface.monitor_menu.add_command(
                label=monitor_name, command=lambda m=monitor: set_selected_monitor(m)
            )


def set_selected_monitor(monitor):
    """
    Sets the selected monitor for recording.

    Parameters
    ----------
    monitor : dict
        The monitor to select for recording. This is a dictionary with the
        keys "top", "left", "width", and "height".

    """
    global selected_monitor
    selected_monitor = monitor
    print(
        f"Selected Monitor: {selected_monitor} -> {selected_monitor['width']}x{selected_monitor['height']}"
    )


interface.video_format_menu.add_checkbutton(
    label=".mp4",
    onvalue=1,
    offvalue=0,
    variable=interface.mp4_format,
    command=lambda: edit_checks("mp4"),
)
interface.video_format_menu.add_checkbutton(
    label=".avi",
    onvalue=1,
    offvalue=0,
    variable=interface.avi_format,
    command=lambda: edit_checks("avi"),
)

interface.about_menu.add_command(
    label="Mehmet Mert Altuntas",
    command=lambda: webbrowser.open("https://github.com/mehmet-mert"),
)

populate_monitor_menu()


def create_vid():
    """
    Initializes the VideoWriter object for recording the screen.

    If a monitor is selected, records that monitor. Otherwise, records the
    primary monitor.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    This function is called by the "Play" button in the GUI.

    """
    global out
    if selected_monitor:
        monitor_pos = (selected_monitor["left"], selected_monitor["top"])
        monitor_size = (selected_monitor["width"], selected_monitor["height"])
    else:
        # Fallback to the primary monitor if none selected
        monitor_pos = (0, 0)
        monitor_size = mss.mss().monitors[1]["width"], mss.mss().monitors[1]["height"]

    fourcc = cv.VideoWriter_fourcc(*result_format2())
    out = cv.VideoWriter(
        "Outputs/FrameRecorder " + find_time() + result_format(),
        fourcc,
        interface.switch.get(),
        monitor_size,
    )
    print(f"VideoWriter initialized with size: {monitor_size}")


def record():
    """
    Records a single frame from the selected monitor and writes it to the
    VideoWriter object initialized by `create_vid`.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    This function is called by the `start_record` function.

    """
    with mss.mss() as sct:
        if selected_monitor:
            monitor = selected_monitor
        else:
            monitor = sct.monitors[1]  # Default to the primary monitor

        img = sct.grab(monitor)
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)  # Convert RGBA to RGB

        # Save a screenshot for debugging
        # cv.imwrite("test_screenshot.png", frame)

        out.write(frame)


def start_record():
    """
    Starts recording the screen.

    If the previous recording has just ended (`status` is `"end"`), this
    function will call `create_vid` to initialize the VideoWriter object.
    Then, it will change `status` to `"playing"` and enable the "Pause" and
    "Stop" buttons.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if status in ("end"):
        create_vid()
    status_playing("playing")


def status_playing(yeter):
    """
    Updates the state of the GUI based on the `status` variable.

    Parameters
    ----------
    yeter : str
        The new value of the `status` variable. This should be one of
        "stopped", "playing", or "end".

    Returns
    -------
    None

    Notes
    -----
    This function is used to update the state of the GUI based on the
    recording status. It will change the state of the buttons and the text
    on the canvas based on the `status` variable.

    """
    global status
    status = yeter
    if status == "stopped":
        interface.pause["state"] = "disabled"
        interface.start["state"] = "normal"
        interface.canvas.itemconfig(
            interface.info, text="Paused. Continue Recording with Play"
        )
    elif status == "playing":
        interface.pause["state"] = "normal"
        interface.end["state"] = "normal"
        interface.start["state"] = "disabled"
        interface.canvas.itemconfig(interface.info, text="Recording...")
    elif status == "end":
        interface.canvas.itemconfig(
            interface.info,
            text="Video Saved At Outputs Folder. Let's Create Another One!",
        )
        interface.pause["state"] = "disabled"
        interface.end["state"] = "disabled"
        interface.start["state"] = "normal"


interface.start.config(command=lambda: start_record())
interface.end.config(command=lambda: status_playing("end"))
interface.pause.config(command=lambda: status_playing("stopped"))

interface.running = True
while interface.running:
    interface.root.update()
    interface.switch.place(x=400, y=176, anchor=tkinter.CENTER)
    interface.start.place(x=318, y=230, width=172, height=58)
    interface.pause.place(x=118, y=230, width=172, height=58)
    interface.end.place(x=518, y=230, width=172, height=58)
    interface.root.config(menu=interface.menubar)
    if status == "playing":
        record()
    elif status == "stopped":
        pass
    elif status == "end":
        out.release()
