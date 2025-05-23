# from IoTDevice import IoTDevice
# from Status import Status
# import random

# class SecurityCamera(IoTDevice):
#     def __init__(self, id, security_status):
#         super().__init__(id)
#         self.__security_status = security_status
#         self.__motion = False

#     def get_security_status(self):
#         return self.__security_status

#     def set_security_status(self, security_status):
#         self.__security_status = security_status

#     def get_motion(self):
#         if self._status == Status.Off:
#             return False

#         return self.__motion

#     def detect_motion(self, motion):
#         if self._status == Status.Off:
#             self._status = Status.On

#         self.__motion = motion

from IoTDevice import IoTDevice
from Status import Status
import random

class OccupancyActivitySensor(IoTDevice):
    def __init__(self, id, occupancy_count=0):
        super().__init__(id)
        self.__occupancy_count = occupancy_count
        self.__activity_type = "None"
        self.__confidence_level = 0
        self.__activity_history = []
        self.__room_capacity = 20  # Default maximum room capacity
        self.__activity_types = ["Sitting", "Standing", "Walking", "Running", 
                               "Meeting", "Eating", "Working", "Idle"]
    
    def get_occupancy_count(self):
        if self._status == Status.Off:
            return 0
        return self.__occupancy_count
    
    def set_occupancy_count(self, count):
        if self._status == Status.Off:
            self._status = Status.On
            
        if count >= 0 and count <= self.__room_capacity:
            self.__occupancy_count = count
        else:
            print(f"Error: Count must be between 0 and {self.__room_capacity}")
    
    def set_room_capacity(self, capacity):
        if capacity > 0:
            self.__room_capacity = capacity
        else:
            print("Error: Room capacity must be positive")
    
    def get_room_capacity(self):
        return self.__room_capacity
    
    def get_activity_type(self):
        if self._status == Status.Off or self.__occupancy_count == 0:
            return "None"
        return self.__activity_type
    
    def get_confidence_level(self):
        return self.__confidence_level
    
    def detect_activity(self, activity_type=None):
        if self._status == Status.Off:
            self._status = Status.On
            
        if self.__occupancy_count == 0:
            self.__activity_type = "None"
            self.__confidence_level = 100
            return
            
        # If activity is provided, use it; otherwise randomly select one based on occupancy
        if activity_type is not None and activity_type in self.__activity_types:
            self.__activity_type = activity_type
            self.__confidence_level = random.randint(85, 98)
        else:
            # Select activity based on occupancy patterns
            if self.__occupancy_count == 1:
                possible_activities = ["Sitting", "Standing", "Walking", "Working", "Idle"]
            elif 2 <= self.__occupancy_count <= 4:
                possible_activities = ["Meeting", "Sitting", "Standing", "Working"]
            else:  # 5 or more
                possible_activities = ["Meeting", "Standing", "Walking"]
                
            self.__activity_type = random.choice(possible_activities)
            self.__confidence_level = random.randint(75, 95)
            
        # Record in history
        self.__activity_history.append({
            "activity": self.__activity_type,
            "occupancy": self.__occupancy_count,
            "confidence": self.__confidence_level
        })
        
        # Keep history manageable
        if len(self.__activity_history) > 100:
            self.__activity_history.pop(0)
    
    def get_activity_history(self):
        return self.__activity_history
    
    def get_occupancy_density(self):
        """Calculate room density as percentage of capacity"""
        return (self.__occupancy_count / self.__room_capacity) * 100
    
    def predict_next_activity(self):
        """Simple prediction based on recent history"""
        if len(self.__activity_history) < 5 or self.__occupancy_count == 0:
            return "Insufficient data"
            
        # Get the most common recent activities
        recent_activities = [entry["activity"] for entry in self.__activity_history[-5:]]
        activity_count = {}
        for activity in recent_activities:
            if activity in activity_count:
                activity_count[activity] += 1
            else:
                activity_count[activity] = 1
                
        # Find most common activity
        most_common = max(activity_count, key=activity_count.get)
        
        return most_common