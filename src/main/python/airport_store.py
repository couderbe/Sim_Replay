from src.main.python.tools.geometry import Point3D

# Lasbordes
AIRPORT_SETTINGS = {
    "point0": Point3D(1.5013254024875005, 43.583443220201715, 460),
    "point1": Point3D(1.4971921614488435, 43.58999951743251, 460),
}
AIRPORT_SETTINGS2 = {
    "point0": Point3D(2.0064941910496525, 43.768835706514764, 575),
    "point1": Point3D(2.014150946651791, 43.768252580658775, 580),
}


class AirportStore:

    airports = {
        "LFCL": {
            "point0": Point3D(1.5013254024875005, 43.583443220201715, 460),
            "point1": Point3D(1.4971921614488435, 43.58999951743251, 460),
        },
        "LFCQ": {
            "point0": Point3D(2.0064941910496525, 43.768835706514764, 575),
            "point1": Point3D(2.014150946651791, 43.768252580658775, 580),
        },
    }

    @classmethod
    def get_airports(cls):
        return cls.airports