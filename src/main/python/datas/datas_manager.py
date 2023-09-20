from ctypes import c_double


class FlightDataset:
    def __init__(self, _set, _timestamp:str):
        self.set:dict = _set
        self.timestamp = _timestamp

    def merge(self,_set:dict):
        self.set = self.set | _set
    
    def get_keys(self):
        return self.set.keys()
    


class FlightDatasManager:
    STATE_FLIGHT_DATASET = FlightDataset(
        {
            "ZULU TIME": {"unit": "s", "type": c_double},
            "Plane Latitude": {"unit": "°", "type": c_double},
            "Plane Longitude": {"unit": "°", "type": c_double},
            "Plane Altitude": {"unit": "ft", "type": c_double},
            "Plane Bank Degrees": {"unit": "°", "type": c_double},
            "Plane Pitch Degrees": {"unit": "°", "type": c_double},
            "Plane Heading Degrees True": {"unit": "°", "type": c_double},
        },
        "ZULU TIME",
    )

    INPUT_FLIGHT_DATASET = FlightDataset(
        {
            "ZULU TIME": {"unit": "s", "type": c_double},
            "Aileron Position": {"unit": "Position", "type": c_double},
            "Elevator Position": {"unit": "Position", "type": c_double},
            "Rudder Position": {"unit": "Position", "type": c_double},
            "General Eng Throttle Lever Position:1": {
                "unit": "Percent",
                "type": c_double,
            },
        },
        "ZULU TIME",
    )

    current_dataset:FlightDataset = FlightDataset(STATE_FLIGHT_DATASET.set, STATE_FLIGHT_DATASET.timestamp)

    has_positioning = True

    timestamp = STATE_FLIGHT_DATASET.timestamp

    @classmethod
    def add_data(cls,name:str, unit:str|None, type=c_double):
        res = {}
        res[name]= {'unit':unit,'type':type}
        if(unit!=None or (name not in cls.current_dataset.set.keys()) ):
            cls.current_dataset.merge(res)

    @classmethod
    def clean_dataset(cls):
        cls.current_dataset = FlightDataset({},None)
        cls.has_positioning = False
        cls.timestamp = None

    @classmethod
    def get_current_keys(cls):
        return cls.current_dataset.get_keys()

    @classmethod
    def set_dataset_as_state(cls):
        cls.current_dataset = FlightDataset(cls.STATE_FLIGHT_DATASET.set, cls.STATE_FLIGHT_DATASET.timestamp)
        cls.has_positioning = True
        cls.timestamp = cls.STATE_FLIGHT_DATASET.timestamp





