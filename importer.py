import math
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

import gpxpy
import gpxpy.gpx

from gpxpy.gpx import GPXTrackPoint
from tools.gpx_interpolate import GPXData, gpx_interpolate, gpx_read
from tools.geometry import DEG_2_RAD

def import_gpx_file(_mainTableModel:QStandardItemModel, fileName):
    """Updates the main table with the trajectory found in a given .gpx file

    Args:
        _mainTableModel (QStandardItemModel): the main table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file

    Returns:
        Any: null
    """
    with open(fileName, 'r') as gpxfile:
        reader_gpx = gpxpy.parse(gpxfile)
        headers = [
                "ZULU TIME",
                "Plane Longitude",
                "Plane Latitude",
                "Plane Altitude",
                "Plane Bank Degrees",
                "Plane Pitch Degrees",
                "Plane Heading Degrees True"]
        first_point = reader_gpx.tracks[0].segments[0].points[0]
        previous_point = first_point
        for track in reader_gpx.tracks:
            for segment in track.segments:
                for i,point in enumerate(segment.points):
                    if i > 0:
                        attitude = compute_attitude(previous_point,point)
                        row = [
                            QStandardItem(str(previous_point.time_difference(first_point))),
                            QStandardItem(str(previous_point.longitude)),
                            QStandardItem(str(previous_point.latitude)),
                            QStandardItem(str(previous_point.elevation)),
                            QStandardItem(str(attitude["bank"])),
                            QStandardItem(str(attitude["pitch"])),
                            QStandardItem(str(attitude["heading"]))
                        ]
                        _mainTableModel.appendRow(row)
                    previous_point = point
                        
        for i, header in enumerate(headers):
            _mainTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
        # Set time label initial value

def import_gpx_file_interp(_mainTableModel:QStandardItemModel, fileName):
    """Updates the main table with the trajectory found in a given .gpx file with interpolation
    computed individually between points

    Args:
        _mainTableModel (QStandardItemModel): the main table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file

    Returns:
        Any: null
    """ 
    with open(fileName, 'r') as gpxfile:
        reader_gpx = gpxpy.parse(gpxfile)
        headers = [
                "ZULU TIME",
                "Plane Longitude",
                "Plane Latitude",
                "Plane Altitude",
                "Plane Bank Degrees",
                "Plane Pitch Degrees",
                "Plane Heading Degrees True"]
        first_point = reader_gpx.tracks[0].segments[0].points[0]
        previous_point = first_point
        for track in reader_gpx.tracks:
            for segment in track.segments:
                for i,point in enumerate(segment.points):
                    if i > 0:
                        gpx_data = {'lat':[previous_point.latitude,point.latitude],
                                    'lon':[previous_point.longitude,point.longitude],
                                    'ele':[previous_point.elevation,point.elevation],
                                    'tstamp':[previous_point.time_difference(first_point),point.time_difference(first_point)],
                                    'tzinfo':[]
                                    }
                        interp_data = gpx_interpolate(gpx_data,1,10)
                        previous_interp_point = GPXTrackPoint(interp_data['lat'][0],interp_data['lon'][0],interp_data['ele'][0],interp_data['tstamp'][0])
                        for j in range(1,len(interp_data['lat'])):
                            
                            interp_point = GPXTrackPoint(interp_data['lat'][j],interp_data['lon'][j],interp_data['ele'][j],interp_data['tstamp'][j])
                            attitude = compute_attitude(previous_interp_point,interp_point)
                            row = [
                                QStandardItem(str(previous_interp_point.time)),
                                QStandardItem(str(previous_interp_point.longitude)),
                                QStandardItem(str(previous_interp_point.latitude)),
                                QStandardItem(str(previous_interp_point.elevation)),
                                QStandardItem(str(attitude["bank"])),
                                QStandardItem(str(attitude["pitch"])),
                                QStandardItem(str(attitude["heading"]))
                            ]
                            _mainTableModel.appendRow(row)
                            previous_interp_point = interp_point
                               
                    previous_point = point
                        
        for i, header in enumerate(headers):
            _mainTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
        # Set time label initial value

def import_gpx_file_module(_mainTableModel:QStandardItemModel, fileName):
    """Updates the main table with the trajectory found in a given .gpx file with interpolation
    computed globally by module

    Args:
        _mainTableModel (QStandardItemModel): the main table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file

    Returns:
        Any: null
    """ 
    gpx_datas = gpx_interpolate(gpx_read(fileName),50,5000)
    first_interp_point_time =  GPXTrackPoint(gpx_datas['lat'][0],gpx_datas['lon'][0],gpx_datas['ele'][0],gpx_datas['tstamp'][0])
    previous_interp_point = first_interp_point_time
    for j in range(1,len(gpx_datas['lat'])):
        interp_point = GPXTrackPoint(gpx_datas['lat'][j],gpx_datas['lon'][j],gpx_datas['ele'][j],gpx_datas['tstamp'][j])
        attitude = compute_attitude(previous_interp_point,interp_point)
        row = [
            QStandardItem(str(previous_interp_point.time)),
            QStandardItem(str(previous_interp_point.longitude)),
            QStandardItem(str(previous_interp_point.latitude)),
            QStandardItem(str(previous_interp_point.elevation)),
            QStandardItem(str(attitude["bank"])),
            QStandardItem(str(attitude["pitch"])),
            QStandardItem(str(attitude["heading"]))
        ]
        _mainTableModel.appendRow(row)
        previous_interp_point = interp_point
    headers = [
                "ZULU TIME",
                "Plane Longitude",
                "Plane Latitude",
                "Plane Altitude",
                "Plane Bank Degrees",
                "Plane Pitch Degrees",
                "Plane Heading Degrees True"]
    for i, header in enumerate(headers):
            _mainTableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)


def compute_attitude(previous_point:GPXTrackPoint,point:GPXTrackPoint):
    heading = previous_point.course_between(point)
    heading = math.atan2((point.longitude-previous_point.longitude)*math.cos(DEG_2_RAD * point.latitude),point.latitude-previous_point.latitude)/DEG_2_RAD+180
    return {"bank":0.0,"pitch":0.0,"heading":heading }

def compute_interp_attitude(previous_point:GPXData,point:GPXData,):
    heading = point.course_between(previous_point)
    return {"bank":0.0,"pitch":0.0,"heading":heading }