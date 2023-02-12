from ctypes import Structure
from ctypes.wintypes import DWORD


class SIMCONNECT_RECV(Structure):
    _fields_ = [("dwSize", DWORD), ("dwVersion", DWORD), ("dwID", DWORD)]


class SIMCONNECT_RECV_SIMOBJECT_DATA(SIMCONNECT_RECV):
    _fields_ = [("dwRequestID", DWORD), ("dwObjectID", DWORD), ("dwDefineID", DWORD),
                ("dwFlags", DWORD), ("dwentrynumber", DWORD), ("dwoutof", DWORD),
                ("dwDefineCount", DWORD), ("dwData", DWORD * 8192),]