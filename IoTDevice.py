from Status import Status

# class IoTDevice:
#     def __init__(self, id):
#         self._id = id
#         self._status = Status.Off
    
#     def get_status(self):
#         return self._status
    
#     def set_status(self, status):
#         self._status = status

#     def get_id(self):
#         return self._id

class IoTDevice:
    def __init__(self, id, device_type="Generic"):
        self._id = id
        self._status = Status.Off
        self._device_type = device_type
        self._last_updated = None
        self._data_history = []
        self._max_history_length = 100
        
    def get_status(self):
        return self._status
        
    def set_status(self, status):
        self._status = status
        self._update_timestamp()
    
    def get_id(self):
        return self._id
    
    def get_device_type(self):
        return self._device_type
    
    def _update_timestamp(self):
        """Update the last modified timestamp"""
        import datetime
        self._last_updated = datetime.datetime.now()
        
    def get_last_updated(self):
        """Get the last time this device was updated"""
        return self._last_updated
    
    def add_to_history(self, data_point):
        """Add a data point to device history"""
        if len(self._data_history) >= self._max_history_length:
            self._data_history.pop(0)
        self._data_history.append(data_point)
        
    def get_history(self):
        """Get device data history"""
        return self._data_history
    
    def clear_history(self):
        """Clear the device history"""
        self._data_history = []
    
    def set_max_history(self, length):
        """Set maximum history length"""
        if length > 0:
            self._max_history_length = length