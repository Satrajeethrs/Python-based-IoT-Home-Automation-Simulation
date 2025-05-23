# from IoTDevice import IoTDevice
# from Status import Status

# class Thermostat(IoTDevice):
#     def __init__(self, id, temperature, min_temp, max_temp):
#         super().__init__(id)
#         self.__temperature = temperature
#         self.__min_temp = min_temp
#         self.__max_temp = max_temp

#     def get_temperature(self):
#         return self.__temperature

#     def get_min_temp(self):
#         return self.__min_temp

#     def get_max_temp(self):
#         return self.__max_temp

#     def set_temperature(self, temperature):
#         if self._status == Status.Off:
#             self._status = Status.On
        
#         if(self.__min_temp <= temperature and self.__max_temp >= temperature):
#             self.__temperature = temperature
#         else:
#             print(f"Error. Temperature must be between {__min_temp} and {__max_temp}")

#     def set_min_temp(self, min_temp):
#         self.__min_temp = min_temp

#     def set_max_temp(self, max_temp):
#         self.__max_temp = max_temp
        
#     def adjust_temperature(self, temperature):
#         if self._status == Status.Off:
#             self._status == Status.On
        
#         new_temp = temperature + self.__temperature
        
#         if(self.__min_temp <= new_temp and self.__max_temp >= new_temp):
#             self.__temperature = new_temp
#         else:
#             print(f"Error. Temperature must be between {__min_temp} and {__max_temp}")

from IoTDevice import IoTDevice
from Status import Status

class AmbientLightSensor(IoTDevice):
    def __init__(self, id, light_level, min_level, max_level):
        super().__init__(id)
        self.__light_level = light_level  # Current light level in lux
        self.__min_level = min_level      # Minimum detectable light level
        self.__max_level = max_level      # Maximum detectable light level
    
    def get_light_level(self):
        return self.__light_level
    
    def get_min_level(self):
        return self.__min_level
    
    def get_max_level(self):
        return self.__max_level
    
    def set_light_level(self, light_level):
        if self._status == Status.Off:
            self._status = Status.On
            
        if(self.__min_level <= light_level and self.__max_level >= light_level):
            self.__light_level = light_level
        else:
            print(f"Error. Light level must be between {self.__min_level} and {self.__max_level}")
    
    def set_min_level(self, min_level):
        self.__min_level = min_level
    
    def set_max_level(self, max_level):
        self.__max_level = max_level
        
    def adjust_light_level(self, adjustment):
        if self._status == Status.Off:
            self._status = Status.On
            
        new_level = adjustment + self.__light_level
            
        if(self.__min_level <= new_level and self.__max_level >= new_level):
            self.__light_level = new_level
        else:
            print(f"Error. Light level must be between {self.__min_level} and {self.__max_level}")