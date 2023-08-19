from enum import Enum


class SIMCONNECT_PERIOD(Enum):
    SIMCONNECT_PERIOD_NEVER = 0
    SIMCONNECT_PERIOD_ONCE = 1
    SIMCONNECT_PERIOD_VISUAL_FRAME = 2
    SIMCONNECT_PERIOD_SIM_FRAME = 3
    SIMCONNECT_PERIOD_SECOND = 4


class SIMCONNECT_RECV_ID(Enum):
    SIMCONNECT_RECV_ID_NULL = 0
    SIMCONNECT_RECV_ID_EXCEPTION = 1
    SIMCONNECT_RECV_ID_OPEN = 2
    SIMCONNECT_RECV_ID_QUIT = 3
    SIMCONNECT_RECV_ID_EVENT = 4
    SIMCONNECT_RECV_ID_EVENT_OBJECT_ADDREMOVE = 5
    SIMCONNECT_RECV_ID_EVENT_FILENAME = 6
    SIMCONNECT_RECV_ID_EVENT_FRAME = 7
    SIMCONNECT_RECV_ID_SIMOBJECT_DATA = 8
    SIMCONNECT_RECV_ID_SIMOBJECT_DATA_BYTYPE = 9
    SIMCONNECT_RECV_ID_WEATHER_OBSERVATION = 10
    SIMCONNECT_RECV_ID_CLOUD_STATE = 11
    SIMCONNECT_RECV_ID_ASSIGNED_OBJECT_ID = 12
    SIMCONNECT_RECV_ID_RESERVED_KEY = 13
    SIMCONNECT_RECV_ID_CUSTOM_ACTION = 14
    SIMCONNECT_RECV_ID_SYSTEM_STATE = 15
    SIMCONNECT_RECV_ID_CLIENT_DATA = 16
    SIMCONNECT_RECV_ID_EVENT_WEATHER_MODE = 17
    SIMCONNECT_RECV_ID_AIRPORT_LIST = 18
    SIMCONNECT_RECV_ID_VOR_LIST = 19
    SIMCONNECT_RECV_ID_NDB_LIST  = 20
    SIMCONNECT_RECV_ID_WAYPOINT_LIST = 21
    SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_SERVER_STARTED = 22
    SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_CLIENT_STARTED = 23
    SIMCONNECT_RECV_ID_EVENT_MULTIPLAYER_SESSION_ENDED = 24
    SIMCONNECT_RECV_ID_EVENT_RACE_END = 25
    SIMCONNECT_RECV_ID_EVENT_RACE_LAP = 26