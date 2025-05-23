# from IoTDevice import IoTDevice
# from Status import Status
# import time

# class SmartLight(IoTDevice):
#     def __init__(self, id, brightness):
#         super().__init__(id)
#         self.__brightness = brightness
    
#     def set_status(self, status):
#         if status == Status.On and self.__brightness == 0:
#             self.__brightness = 1
#         elif status == Status.Off and self.__brightness > 0:
#             self.__brightness = 0
        
#         self._status = status

#     def get_brightness(self):
#         return self.__brightness 

#     def set_brightness(self, brightness):
#         if self._status == Status.Off and brightness > 0:
#             self._status = Status.On
#         elif self._status == Status.On and brightness == 0:
#             self._status = Status.Off

#         self.__brightness = brightness

#     def gradual_dimming(self, steps, duration, delay, step_size):
#         for _ in range(steps):
#             new_brightness = self.__brightness - step_size
#             if(new_brightness >= 0):
#                 self.__brightness = new_brightness
#             time.sleep(delay)

#         self.__brightness = 0
#         self._status = Status.Off

from IoTDevice import IoTDevice
from Status import Status
import time
import random

class AirQualityPredictionSensor(IoTDevice):
    def __init__(self, id, aqi_level):
        super().__init__(id)
        self.__aqi_level = aqi_level  # Air Quality Index level
        self.__pollutants = {
            "PM2.5": 0,
            "PM10": 0,
            "CO2": 400,
            "VOC": 0,
            "NO2": 0,
            "O3": 0
        }
        self.__prediction_horizon = 6  # Default prediction horizon in hours
        
    def set_status(self, status):
        self._status = status
        
    def get_aqi_level(self):
        return self.__aqi_level
        
    def set_aqi_level(self, aqi_level):
        if aqi_level >= 0 and aqi_level <= 500:  # AQI ranges from 0-500
            self.__aqi_level = aqi_level
        else:
            print("Error: AQI level must be between 0 and 500")
    
    def get_pollutant_level(self, pollutant):
        if pollutant in self.__pollutants:
            return self.__pollutants[pollutant]
        else:
            print(f"Error: {pollutant} is not a tracked pollutant")
            return None
    
    def set_pollutant_level(self, pollutant, level):
        if pollutant in self.__pollutants:
            self.__pollutants[pollutant] = level
            self.__recalculate_aqi()
        else:
            print(f"Error: {pollutant} is not a tracked pollutant")
    
    def __recalculate_aqi(self):
        # Simplified AQI calculation based on pollutant levels
        # In a real implementation, this would use proper EPA formulas
        pm25_weight = 0.35
        pm10_weight = 0.15
        co2_weight = 0.2
        voc_weight = 0.1
        no2_weight = 0.1
        o3_weight = 0.1
        
        # Normalize each pollutant to a 0-500 scale
        pm25_normalized = min(self.__pollutants["PM2.5"] * 10, 500)
        pm10_normalized = min(self.__pollutants["PM10"] * 5, 500)
        co2_normalized = min((self.__pollutants["CO2"] - 400) / 2, 500)
        voc_normalized = min(self.__pollutants["VOC"] * 50, 500)
        no2_normalized = min(self.__pollutants["NO2"] * 25, 500)
        o3_normalized = min(self.__pollutants["O3"] * 40, 500)
        
        # Calculate weighted average
        self.__aqi_level = (pm25_weight * pm25_normalized +
                          pm10_weight * pm10_normalized +
                          co2_weight * co2_normalized +
                          voc_weight * voc_normalized +
                          no2_weight * no2_normalized +
                          o3_weight * o3_normalized)
        
        # Round to nearest integer
        self.__aqi_level = round(self.__aqi_level)
    
    def set_prediction_horizon(self, hours):
        if hours > 0:
            self.__prediction_horizon = hours
        else:
            print("Error: Prediction horizon must be positive")
    
    def get_prediction_horizon(self):
        return self.__prediction_horizon
    
    def predict_future_aqi(self):
        """Generate air quality predictions for the set prediction horizon"""
        if self._status == Status.Off:
            print("Error: Sensor is off. Cannot generate predictions.")
            return None
            
        predictions = []
        current_aqi = self.__aqi_level
        
        for hour in range(1, self.__prediction_horizon + 1):
            # Simple prediction model with some randomness
            # In a real implementation, this would use historical data patterns
            # and environmental factors like weather forecasts
            
            # Add some variance with time trend
            variance = random.uniform(-20, 20)
            time_trend = (hour / self.__prediction_horizon) * random.uniform(-15, 15)
            
            predicted_aqi = max(0, min(500, current_aqi + variance + time_trend))
            predictions.append(round(predicted_aqi))
        
        return predictions
    
    def simulate_trend(self, steps, duration, trend_direction, magnitude):
        """Simulate a gradual trend in air quality over time"""
        if self._status == Status.Off:
            self._status = Status.On
            
        delay = duration / steps
        step_change = magnitude / steps * trend_direction
        
        for _ in range(steps):
            new_aqi = self.__aqi_level + step_change
            if 0 <= new_aqi <= 500:
                self.__aqi_level = new_aqi
            time.sleep(delay)
            
        print(f"Air quality trend simulation complete. Current AQI: {self.__aqi_level}")