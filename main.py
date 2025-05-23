import tkinter as tk
from tkinter import *
from AutomationSystem import AutomationSystem
import threading
import time
from Status import Status

class App():
    def __init__(self):
        # AutomationSystem
        self.asys = AutomationSystem()
        self.asys.add_devices()
        self.devices = self.asys.get_devices()

        # root and frame
        self.root = tk.Tk()
        self.root.geometry('1000x750')
        self.root.title('Smart Environment Simulator')
        # --- Redesign V2: Primary Dark Background ---
        self.root.configure(background='#2c2f33')
        self.mainframe = tk.Frame(self.root, background='#2c2f33')
        self.mainframe.pack(fill='both', expand=True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Title
        # --- Redesign V2: Accent color for main title ---
        self.title_label = Label(self.mainframe, text="VIRTUAL SMART LAB ENVIRONMENT",
                              font=("Helvetica", 16, "bold"), fg="#7289da", bg="#2c2f33")
        self.title_label.pack(pady=10)

        # automation
        self.automation_running = False
        self.update_gui()

        # --- Redesign V2: Consistent frame background ---
        frame_top = Frame(self.mainframe, bg="#2c2f33")
        frame_top.pack(fill='x', padx=20, pady=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.automation_button = Button(frame_top, text="Automation ON/OFF",
                                     command=self.on_off_automation,
                                     bg="#23272a", fg="#7289da", padx=10, pady=5,
                                     font=("Helvetica", 10), relief=RIDGE)
        self.automation_button.pack(side=LEFT, padx=10)

        # --- Redesign V2: General text color ---
        self.text_block = Label(frame_top, text="Automation Status: OFF",
                             bg='#2c2f33', fg='#ffffff', font=("Helvetica", 10))
        self.text_block.pack(side=LEFT, padx=10)

        self.loop_thread = None

        # randomize button
        # --- Redesign V2: Buttons with accent color text ---
        self.randomize_button = Button(frame_top, text="Randomize Sensors",
                                    command=self.randomize, bg="#23272a", fg="#7289da",
                                    padx=10, pady=5, font=("Helvetica", 10), relief=RIDGE)
        self.randomize_button.pack(side=RIGHT, padx=10)

        # status box
        # --- Redesign V2: Consistent frame background and border ---
        frame_status = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        frame_status.pack(fill='x', padx=20, pady=5)

        # --- Redesign V2: General label text color ---
        Label(frame_status, text="DEVICE STATUS", font=("Helvetica", 10, "bold"),
             fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: Text box background, text color, and insert color ---
        self.status_box = Text(frame_status, height=3, width=50,
                            bg="#2c2f33", fg="#ffffff", insertbackground="#f04747",
                            font=("Courier", 10), bd=0, highlightthickness=0) # Removed default border
        self.status_text = ("Ambient Light Sensor status: OFF\n" +
                        "Air Quality Prediction Sensor status: OFF\n" +
                        "Occupancy Activity Sensor status: OFF")
        self.status_box.insert("1.0", self.status_text)
        self.status_box.config(state=DISABLED)
        self.status_box.pack(padx=10, pady=5)

        # Create frames for each sensor
        self.create_light_sensor_frame()
        self.create_air_quality_frame()
        self.create_occupancy_frame()

        # Sensor data display
        self.create_sensor_data_frame()

        # automation rule
        # --- Redesign V2: Consistent frame background and border ---
        rule_frame = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        rule_frame.pack(fill='x', padx=20, pady=10)

        # --- Redesign V2: General label text color ---
        Label(rule_frame, text="AUTOMATION RULES", font=("Helvetica", 10, "bold"),
             fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: General text color ---
        self.text_block8 = Label(rule_frame, text="Rule 1: Adjust ambient light when occupancy changes\n" +
                              "Rule 2: Predict air quality based on occupancy density\n" +
                              "Rule 3: Alert when air quality falls below threshold",
                              justify=LEFT, bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.text_block8.pack(anchor='w', padx=10, pady=5)

        self.root.mainloop()

    def create_light_sensor_frame(self):
        # Ambient Light Sensor
        # --- Redesign V2: Consistent frame background and border ---
        light_frame = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        light_frame.pack(fill='x', padx=20, pady=5)

        # --- Redesign V2: General label text color ---
        Label(light_frame, text="AMBIENT LIGHT SENSOR", font=("Helvetica", 10, "bold"),
             fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: Consistent frame background ---
        light_control_frame = Frame(light_frame, bg="#23272a")
        light_control_frame.pack(fill='x', padx=10)

        # --- Redesign V2: General text color ---
        Label(light_control_frame, text="Light Level (lux):",
             bg='#23272a', fg='#ffffff', font=("Helvetica", 9)).pack(side=LEFT, padx=5)

        # --- Redesign V2: Slider colors ---
        self.slider1 = Scale(light_control_frame, from_=0, to=10000, orient=HORIZONTAL,
                         bg='#23272a', fg='#ffffff', troughcolor='#99aab5', highlightthickness=0,
                         length=300, command=self.change_light_level, activebackground="#7289da") # Accent blue-purple on hover/active
        self.slider1.pack(side=LEFT, padx=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.light_button = Button(light_control_frame, text="Toggle ON/OFF",
                                command=self.on_off_light, bg="#23272a", fg="#7289da",
                                padx=5, pady=2, font=("Helvetica", 9), relief=RIDGE)
        self.light_button.pack(side=RIGHT, padx=10)

        # --- Redesign V2: General text color ---
        self.light_level_label = Label(light_frame, text="Current Light Level: 0 lux",
                                    bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.light_level_label.pack(anchor='w', padx=10, pady=5)

    def create_air_quality_frame(self):
        # Air Quality Prediction Sensor
        # --- Redesign V2: Consistent frame background and border ---
        aqi_frame = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        aqi_frame.pack(fill='x', padx=20, pady=5)

        # --- Redesign V2: General label text color ---
        Label(aqi_frame, text="AIR QUALITY PREDICTION SENSOR", font=("Helvetica", 10, "bold"),
             fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: Consistent frame background ---
        aqi_control_frame = Frame(aqi_frame, bg="#23272a")
        aqi_control_frame.pack(fill='x', padx=10)

        # --- Redesign V2: General text color ---
        Label(aqi_control_frame, text="AQI Level:",
             bg='#23272a', fg='#ffffff', font=("Helvetica", 9)).pack(side=LEFT, padx=5)

        # --- Redesign V2: Slider colors ---
        self.slider2 = Scale(aqi_control_frame, from_=0, to=500, orient=HORIZONTAL,
                         bg='#23272a', fg='#ffffff', troughcolor='#99aab5', highlightthickness=0,
                         length=300, command=self.change_aqi_level, activebackground="#7289da") # Accent blue-purple on hover/active
        self.slider2.pack(side=LEFT, padx=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.aqi_button = Button(aqi_control_frame, text="Toggle ON/OFF",
                              command=self.on_off_aqi, bg="#23272a", fg="#7289da",
                              padx=5, pady=2, font=("Helvetica", 9), relief=RIDGE)
        self.aqi_button.pack(side=RIGHT, padx=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.predict_button = Button(aqi_control_frame, text="Predict Future AQI",
                                  command=self.predict_aqi, bg="#23272a", fg="#7289da",
                                  padx=5, pady=2, font=("Helvetica", 9), relief=RIDGE)
        self.predict_button.pack(side=RIGHT, padx=10)

        # --- Redesign V2: General text color ---
        self.aqi_level_label = Label(aqi_frame, text="Current AQI: 0 (Good)",
                                  bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.aqi_level_label.pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: General text color ---
        self.aqi_prediction_label = Label(aqi_frame, text="No predictions available",
                                       bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.aqi_prediction_label.pack(anchor='w', padx=10, pady=5)

    def create_occupancy_frame(self):
        # Occupancy Activity Sensor
        # --- Redesign V2: Consistent frame background and border ---
        occupancy_frame = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        occupancy_frame.pack(fill='x', padx=20, pady=5)

        # --- Redesign V2: General label text color ---
        Label(occupancy_frame, text="OCCUPANCY & ACTIVITY RECOGNITION SENSOR",
             font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: Consistent frame background ---
        occupancy_control_frame = Frame(occupancy_frame, bg="#23272a")
        occupancy_control_frame.pack(fill='x', padx=10)

        # --- Redesign V2: General text color ---
        Label(occupancy_control_frame, text="Occupancy Count:",
             bg='#23272a', fg='#ffffff', font=("Helvetica", 9)).pack(side=LEFT, padx=5)

        # --- Redesign V2: Slider colors ---
        self.slider3 = Scale(occupancy_control_frame, from_=0, to=20, orient=HORIZONTAL,
                         bg='#23272a', fg='#ffffff', troughcolor='#99aab5', highlightthickness=0,
                         length=300, command=self.change_occupancy_count, activebackground="#7289da") # Accent blue-purple on hover/active
        self.slider3.pack(side=LEFT, padx=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.occupancy_button = Button(occupancy_control_frame, text="Toggle ON/OFF",
                                    command=self.on_off_occupancy, bg="#23272a", fg="#7289da",
                                    padx=5, pady=2, font=("Helvetica", 9), relief=RIDGE)
        self.occupancy_button.pack(side=RIGHT, padx=10)

        # --- Redesign V2: Buttons with accent color text ---
        self.detect_button = Button(occupancy_control_frame, text="Detect Activity",
                                 command=self.detect_activity, bg="#23272a", fg="#7289da",
                                 padx=5, pady=2, font=("Helvetica", 9), relief=RIDGE)
        self.detect_button.pack(side=RIGHT, padx=10)

        # --- Redesign V2: General text color ---
        self.occupancy_label = Label(occupancy_frame, text="Current Occupancy: 0/20 (0%)",
                                  bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.occupancy_label.pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: General text color ---
        self.activity_label = Label(occupancy_frame, text="Current Activity: None",
                                 bg='#23272a', fg='#ffffff', font=("Helvetica", 9))
        self.activity_label.pack(anchor='w', padx=10, pady=5)

    def create_sensor_data_frame(self):
        # Sensor data display
        # --- Redesign V2: Consistent frame background and border ---
        sensor_data_frame = Frame(self.mainframe, bg="#23272a", bd=2, relief=GROOVE, highlightbackground="#99aab5", highlightthickness=1)
        sensor_data_frame.pack(fill='x', padx=20, pady=5)

        # --- Redesign V2: General label text color ---
        Label(sensor_data_frame, text="SENSOR DATA STREAM (5 sec update)",
             font=("Helvetica", 10, "bold"), fg="#ffffff", bg="#23272a").pack(anchor='w', padx=10, pady=5)

        # --- Redesign V2: Data stream specific colors ---
        self.sensor_data_box = Text(sensor_data_frame, height=5, width=70,
                                 bg="#2c2f33", fg="#43b581", insertbackground="#f04747",
                                 font=("Courier", 9), bd=0, highlightthickness=0) # Removed default border
        self.iter = -3
        self.loop_thread2 = threading.Thread(target=self.call_gather_sensor_data, daemon=True)
        self.loop_thread2.start()
        self.sensor_data_box.pack(padx=10, pady=5, fill='x')

    # automation
    def on_off_automation(self):
        if not self.automation_running:
            self.automation_running = True
            self.text_block.config(text="Automation Status: ON")
            self.automation_button.config(relief=SUNKEN)
            self.loop_thread = threading.Thread(target=self.call_exec_automation_tasks)
            self.loop_thread.start()
        else:
            self.automation_running = False
            self.text_block.config(text="Automation Status: OFF")
            self.automation_button.config(relief=RIDGE)

    def call_exec_automation_tasks(self):
        while self.automation_running:
            self.asys.exec_automation_tasks()
            # Update GUI elements for each sensor
            self.slider1.set(self.devices[0].get_light_level())
            self.light_level_label.config(text=f"Current Light Level: {self.devices[0].get_light_level()} lux")

            self.slider2.set(self.devices[1].get_aqi_level())
            self.update_aqi_display()

            self.slider3.set(self.devices[2].get_occupancy_count())
            self.update_occupancy_display()

            self.update_status_box()
            time.sleep(1)

    def on_closing(self):
        if self.loop_thread and self.loop_thread.is_alive():
            self.automation_running = False
            self.loop_thread.join(timeout=2)

        self.asys.store_sensor_data()
        self.root.destroy()

    def update_gui(self):
        self.root.after(1000, self.update_gui)


    # randomize
    def randomize(self):
        self.asys.randomize()
        self.update_status_box()

        # Update light sensor display
        self.slider1.set(self.devices[0].get_light_level())
        self.light_level_label.config(text=f"Current Light Level: {self.devices[0].get_light_level()} lux")

        # Update AQI display
        self.slider2.set(self.devices[1].get_aqi_level())
        self.update_aqi_display()

        # Update occupancy display
        self.slider3.set(self.devices[2].get_occupancy_count())
        self.update_occupancy_display()

    # status box
    def update_status_box(self):
        self.status_text = (f"Ambient Light Sensor status: {'ON' if self.devices[0].get_status() == Status.On else 'OFF'}\n" +
                        f"Air Quality Prediction Sensor status: {'ON' if self.devices[1].get_status() == Status.On else 'OFF'}\n" +
                        f"Occupancy Activity Sensor status: {'ON' if self.devices[2].get_status() == Status.On else 'OFF'}")
        self.status_box.config(state=NORMAL)
        self.status_box.delete("1.0", "end")
        self.status_box.insert("1.0", self.status_text)
        self.status_box.config(state=DISABLED)

    # Ambient Light Sensor Controls
    def change_light_level(self, num):
        if self.devices[0].get_status() == Status.On:
            self.devices[0].set_light_level(int(float(num)))
        self.light_level_label.config(text=f"Current Light Level: {self.devices[0].get_light_level()} lux")
        self.update_status_box()

    def on_off_light(self):
        if self.devices[0].get_status() == Status.Off:
            self.devices[0].set_status(Status.On)
            self.light_button.config(relief=SUNKEN)
            if self.devices[0].get_light_level() == 0:
                self.devices[0].set_light_level(1)
                self.slider1.set(1)
        else:
            self.devices[0].set_status(Status.Off)
            self.light_button.config(relief=RIDGE)
            self.devices[0].set_light_level(0)
            self.slider1.set(0)

        self.light_level_label.config(text=f"Current Light Level: {self.devices[0].get_light_level()} lux")
        self.update_status_box()

    # Air Quality Sensor Controls
    def change_aqi_level(self, num):
        if self.devices[1].get_status() == Status.On:
            self.devices[1].set_aqi_level(int(float(num)))
        self.update_aqi_display()
        self.update_status_box()

    def update_aqi_display(self):
        aqi = self.devices[1].get_aqi_level()
        category = "Good"
        if aqi > 300:
            category = "Hazardous"
        elif aqi > 200:
            category = "Very Unhealthy"
        elif aqi > 150:
            category = "Unhealthy"
        elif aqi > 100:
            category = "Unhealthy for Sensitive Groups"
        elif aqi > 50:
            category = "Moderate"

        self.aqi_level_label.config(text=f"Current AQI: {aqi} ({category})")

    def on_off_aqi(self):
        if self.devices[1].get_status() == Status.Off:
            self.devices[1].set_status(Status.On)
            self.aqi_button.config(relief=SUNKEN)
        else:
            self.devices[1].set_status(Status.Off)
            self.aqi_button.config(relief=RIDGE)
        self.update_status_box()

    def predict_aqi(self):
        if self.devices[1].get_status() == Status.Off:
            self.devices[1].set_status(Status.On)
            self.aqi_button.config(relief=SUNKEN)
            self.update_status_box()

        predictions = self.devices[1].predict_future_aqi()
        if predictions:
            pred_text = "AQI Prediction (next 6 hours): " + " → ".join([str(p) for p in predictions])
            self.aqi_prediction_label.config(text=pred_text)
        else:
            self.aqi_prediction_label.config(text="Prediction failed: Sensor is off or no predictions generated.")


    # Occupancy Sensor Controls
    def change_occupancy_count(self, num):
        if self.devices[2].get_status() == Status.On:
            self.devices[2].set_occupancy_count(int(float(num)))
        self.update_occupancy_display()
        self.update_status_box()

    def update_occupancy_display(self):
        count = self.devices[2].get_occupancy_count()
        capacity = self.devices[2].get_room_capacity()
        density = self.devices[2].get_occupancy_density()
        self.occupancy_label.config(text=f"Current Occupancy: {count}/{capacity} ({density:.1f}%)")

        activity = self.devices[2].get_activity_type()
        confidence = self.devices[2].get_confidence_level()
        self.activity_label.config(text=f"Current Activity: {activity} (Confidence: {confidence}%)")

    def on_off_occupancy(self):
        if self.devices[2].get_status() == Status.Off:
            self.devices[2].set_status(Status.On)
            self.occupancy_button.config(relief=SUNKEN)
        else:
            self.devices[2].set_status(Status.Off)
            self.occupancy_button.config(relief=RIDGE)
        self.update_status_box()

    def detect_activity(self):
        if self.devices[2].get_status() == Status.Off:
            self.devices[2].set_status(Status.On)
            self.occupancy_button.config(relief=SUNKEN)
            self.update_status_box()

        self.devices[2].detect_activity()
        self.update_occupancy_display()

    # sensor data
    def call_gather_sensor_data(self):
        while True:
            self.asys.gather_sensor_data()
            self.sensor_data_array = self.asys.get_sensor_data()
            self.sensor_data_lines = ""
            num_lines_to_show = 3
            start_index = max(0, len(self.sensor_data_array) - num_lines_to_show)
            for i in range(start_index, len(self.sensor_data_array)):
                 self.sensor_data_lines += self.sensor_data_array[i] + "\n"

            self.sensor_data_box.config(state=NORMAL)
            self.sensor_data_box.delete("1.0", "end")
            self.sensor_data_box.insert("1.0", self.sensor_data_lines)
            self.sensor_data_box.config(state=DISABLED)
            time.sleep(5)

if __name__ == '__main__':
    App()