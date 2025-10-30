import queue
import customtkinter as ctk
from tkinter import scrolledtext
import threading
from queue import Queue
from main import run_weather_pipeline
from logger import log

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")

def on_generate_click():
    log("Function on_generate_click started", "INFO")

    btn_generate.configure(state="disabled")

    txt_display.configure(state=ctk.NORMAL)
    txt_display.delete("1.0", "end")
    txt_display.insert("end", "Generating weather report, it may take a while...")
    txt_display.configure(state="disabled")

    result_queue = Queue()

    thread = threading.Thread(
        target=run_ai_in_background,
        args=(result_queue,)
    )
    thread.start()
    log("Thread started", "INFO")
    root.after(100, check_for_result, result_queue)

def run_ai_in_background(result_queue):
    log("Function run_ai_in_background started", "INFO")
    try:
        report_text = run_weather_pipeline()
        result_queue.put(report_text)
    except Exception as e:
        log("Function run_ai_in_background failed", "ERROR")
        result_queue.put(e)
    log("Function run_ai_in_background finished", "INFO")

def check_for_result(result_queue):
    log("Function check_for_result started", "INFO")
    try:
        result = result_queue.get_nowait()
        log("Got result from main thread", "INFO")
        txt_display.configure(state="normal")
        txt_display.delete("1.0", "end")
        txt_display.insert("end", result)
        txt_display.configure(state="disabled")
        btn_generate.configure(state="normal")
    except queue.Empty:
        root.after(100, check_for_result, result_queue)

# --- Configuration ---
root = ctk.CTk()
root.title("Weather AI")
root.geometry("500x300")

frame_top = ctk.CTkFrame(root, fg_color="transparent", bg_color="transparent")
frame_top.pack(pady=10)

btn_generate = ctk.CTkButton(
    frame_top,
    text="Generate weather description",
    font=("Helvetica", 12),
    command=on_generate_click
)
btn_generate.pack()

frame_bottom = ctk.CTkFrame(root)
frame_bottom.pack(pady=10, padx=10, fill="both", expand=True)

txt_display = ctk.CTkTextbox(
    frame_bottom,
    wrap="word",
    font=("Arial", 16),
    state="disabled",
)
txt_display.pack(fill="both", expand=True)

log("Starting main loop", "INFO")
root.mainloop()
log("Ending main loop", "INFO")