# from IoTDevice import IoTDevice
# from SmartLight import SmartLight
# from Thermostat import Thermostat
# from SecurityCamera import SecurityCamera
# from Status import Status
# import random
# from datetime import date
# from datetime import datetime
# from os import strerror

# class AutomationSystem:
#     def __init__(self):
#         self.__devices = []
#         self.__sensor_data = []
    
#     def get_devices(self):
#         return self.__devices

#     def add_devices(self):
#         sl = SmartLight(0, 0)
#         th = Thermostat(1, 0, 0, 30)
#         sc = SecurityCamera(2, "secure")

#         self.__devices.append(sl)
#         self.__devices.append(th)
#         self.__devices.append(sc)

#     def exec_automation_tasks(self):
#         if self.__devices[2].get_motion():
#             self.__devices[0].set_status(Status.On)
#             if self.__devices[0].get_brightness() == 0:
#                 self.__devices[0].set_brightness(1)

#     def randomize(self):        
#         self.__devices[0].set_brightness(random.randint(0,100))

#         min_t = random.randint(0,30)
#         self.__devices[1].set_min_temp(min_t)
#         self.__devices[1].set_max_temp(random.randint(min_t,30))

#         self.__devices[1].set_temperature(random.randint(
#                 self.__devices[1].get_min_temp(), self.__devices[1].get_max_temp()))

#         self.__devices[2].detect_motion(True if random.randint(0,1) else False)

#     def randomize_detect_motion(self):  
#         self.__devices[2].detect_motion(True if random.randint(0,1) else False)

#     def get_sensor_data(self):
#         return self.__sensor_data

#     def gather_sensor_data(self):
#         current_time = datetime.now().strftime("%H:%M:%S")
#         self.__sensor_data.append("[" + str(date.today()) + " " + current_time + "] " + "Living room Light brightness: " + str(self.__devices[0].get_brightness()) + "%" + "\n")
#         self.__sensor_data.append("[" + str(date.today())  + " " + current_time + "] " + "Living room Thermostat temperature: " + str(self.__devices[1].get_temperature()) + "C" + "\n")
#         self.__sensor_data.append("[" + str(date.today())  + " " + current_time + "] " + "Front door camera motion: " + str(self.__devices[2].get_motion()) + "\n\n")
    
#     def store_sensor_data(self):
#         try:
#             fo = open('out.txt', "wt")
#             for line in self.__sensor_data:
#                 fo.write(line)
#             fo.close()
#         except IOError as e:
#             print("Error: ", strerror(e.errno))

from IoTDevice import IoTDevice
from AmbientLightSensor import AmbientLightSensor
from AirQualityPredictionSensor import AirQualityPredictionSensor
from OccupancyActivitySensor import OccupancyActivitySensor
from Status import Status
import random
from datetime import date
from datetime import datetime
from os import strerror

class AutomationSystem:
    def __init__(self):
        self.__devices = []
        self.__sensor_data = []
        
    def get_devices(self):
        return self.__devices
    
    def add_devices(self):
        # Create instances of our novel sensors
        light_sensor = AmbientLightSensor(0, 0, 0, 10000)  # ID, current level, min, max
        air_quality = AirQualityPredictionSensor(1, 50)    # ID, initial AQI
        occupancy = OccupancyActivitySensor(2, 0)          # ID, initial occupancy
        
        self.__devices.append(light_sensor)
        self.__devices.append(air_quality)
        self.__devices.append(occupancy)
    
    def exec_automation_tasks(self):
        # Rule 1: Adjust ambient light based on occupancy
        occupancy = self.__devices[2]
        light_sensor = self.__devices[0]
        
        if occupancy.get_status() == Status.On and occupancy.get_occupancy_count() > 0:
            # If people are present, ensure light sensor is on
            light_sensor.set_status(Status.On)
            
            # Adjust light level based on activity (more light for active tasks)
            activity = occupancy.get_activity_type()
            if activity in ["Walking", "Running", "Meeting"]:
                # Brighter lighting for active scenarios
                if light_sensor.get_light_level() < 800:
                    light_sensor.set_light_level(max(800, light_sensor.get_light_level()))
            elif activity in ["Working", "Eating"]:
                # Medium lighting for focused activities
                if light_sensor.get_light_level() < 500 or light_sensor.get_light_level() > 1000:
                    light_sensor.set_light_level(750)
            elif activity in ["Sitting", "Idle"]:
                # Lower lighting for passive activities
                if light_sensor.get_light_level() > 500:
                    light_sensor.set_light_level(min(500, light_sensor.get_light_level()))
        
        # Rule 2: Predict air quality based on occupancy density
        air_quality = self.__devices[1]
        if occupancy.get_status() == Status.On and air_quality.get_status() == Status.On:
            # Occupancy above 50% may affect air quality prediction
            density = occupancy.get_occupancy_density()
            if density > 50:
                # Higher occupancy tends to worsen air quality over time
                air_quality.simulate_trend(5, 0.1, 1, min(10, density/5))  # Gradual increase
    
    def randomize(self):
        # Randomize Ambient Light settings
        light_sensor = self.__devices[0]
        light_sensor.set_light_level(random.randint(0, 10000))
        
        # Randomize Air Quality settings
        air_quality = self.__devices[1]
        air_quality.set_aqi_level(random.randint(0, 300))
        
        # Randomize Occupancy settings
        occupancy = self.__devices[2]
        occupancy.set_occupancy_count(random.randint(0, occupancy.get_room_capacity()))
        occupancy.detect_activity()  # This will randomly select an appropriate activity
    
    def randomize_detect_motion(self):
        # For legacy compatibility - now randomizes occupancy and activity
        occupancy = self.__devices[2]
        
        # 50% chance of changing occupancy
        if random.choice([True, False]):
            current = occupancy.get_occupancy_count()
            # Either increase or decrease by 1-3 people, within limits
            change = random.randint(1, 3) * random.choice([-1, 1])
            new_count = max(0, min(occupancy.get_room_capacity(), current + change))
            occupancy.set_occupancy_count(new_count)
        
        # Detect new activity based on current occupancy
        occupancy.detect_activity()
    
    def get_sensor_data(self):
        return self.__sensor_data
    
    def gather_sensor_data(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Ambient Light Sensor data
        self.__sensor_data.append(f"[{date.today()} {current_time}] Ambient Light Sensor: {self.__devices[0].get_light_level()} lux\n")
        
        # Air Quality Sensor data
        aqi = self.__devices[1].get_aqi_level()
        aqi_category = "Good"
        if aqi > 300:
            aqi_category = "Hazardous"
        elif aqi > 200:
            aqi_category = "Very Unhealthy"
        elif aqi > 150:
            aqi_category = "Unhealthy"
        elif aqi > 100:
            aqi_category = "Unhealthy for Sensitive Groups"
        elif aqi > 50:
            aqi_category = "Moderate"
        
        self.__sensor_data.append(f"[{date.today()} {current_time}] Air Quality Index: {aqi} ({aqi_category})\n")
        
        # Occupancy Sensor data
        occupancy = self.__devices[2]
        count = occupancy.get_occupancy_count()
        activity = occupancy.get_activity_type()
        confidence = occupancy.get_confidence_level()
        
        self.__sensor_data.append(f"[{date.today()} {current_time}] Occupancy: {count} people, Activity: {activity} (Confidence: {confidence}%)\n\n")
        
    def store_sensor_data(self):
        try:
            fo = open('sensor_data_log.txt', "wt")
            for line in self.__sensor_data:
                fo.write(line)
            fo.close()
        except IOError as e:
            print("Error: ", strerror(e.errno))