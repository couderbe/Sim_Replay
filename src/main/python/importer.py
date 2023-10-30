from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

import gpxpy
import gpxpy.gpx
import math

from gpxpy.gpx import GPXTrackPoint
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.flight_model.flight_model import Attitude, compute_attitude_from_gpx
from src.main.python.tools.gpx_interpolate import GPXData, gpx_interpolate, gpx_read
from src.main.python.tools.geometry import DEG_2_RAD

M_TO_FT = 1/0.3048


def import_gpx_file(tableModel: QStandardItemModel, fileName, limit=math.inf):
    """Updates the table with the trajectory found in a given .gpx file

    Args:
        tableModel (QStandardItemModel): the table that displays the trajectory 
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
        previous_attitude = Attitude(0, 0, 0)
        for track in reader_gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    if i > 0:
                        attitude = Attitude(0, 0, 0)
                        row = [
                            QStandardItem(
                                str(previous_point.time_difference(first_point))),
                            QStandardItem(str(previous_point.longitude)),
                            QStandardItem(str(previous_point.latitude)),
                            QStandardItem(str(previous_point.elevation)),
                            QStandardItem(str(attitude.phi)),
                            QStandardItem(str(attitude.theta)),
                            QStandardItem(str(attitude.psi))
                        ]
                        tableModel.appendRow(row)
                        previous_attitude = attitude
                    previous_point = point
                    if i >= limit:
                        break
                else:
                    continue
                break
            else:
                continue
            break

        for i, header in enumerate(headers):
            tableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
        # Set time label initial value


def import_gpx_file_interp(tableModel: QStandardItemModel, fileName):
    """Updates the table with the trajectory found in a given .gpx file with interpolation
    computed individually between points

    Args:
        tableModel (QStandardItemModel): the table that displays the trajectory 
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
                for i, point in enumerate(segment.points):
                    if i > 0:
                        gpx_data = {'lat': [previous_point.latitude, point.latitude],
                                    'lon': [previous_point.longitude, point.longitude],
                                    'ele': [previous_point.elevation, point.elevation],
                                    'tstamp': [previous_point.time_difference(first_point), point.time_difference(first_point)],
                                    'tzinfo': []
                                    }
                        interp_data = gpx_interpolate(gpx_data, 1, 10)
                        previous_interp_point = GPXTrackPoint(
                            interp_data['lat'][0], interp_data['lon'][0], interp_data['ele'][0], interp_data['tstamp'][0])
                        previous_attitude = Attitude(0, 0, 0)
                        for j in range(1, len(interp_data['lat'])):

                            interp_point = GPXTrackPoint(
                                interp_data['lat'][j], interp_data['lon'][j], interp_data['ele'][j], interp_data['tstamp'][j])
                            attitude = compute_attitude_from_gpx(
                                previous_attitude, previous_interp_point, interp_point)
                            row = [
                                QStandardItem(str(previous_interp_point.time)),
                                QStandardItem(
                                    str(previous_interp_point.longitude)),
                                QStandardItem(
                                    str(previous_interp_point.latitude)),
                                QStandardItem(
                                    str(previous_interp_point.elevation)),
                                QStandardItem(str(attitude.phi)),
                                QStandardItem(str(attitude.theta)),
                                QStandardItem(str(attitude.psi))
                            ]
                            tableModel.appendRow(row)
                            previous_interp_point = interp_point
                            previous_attitude = attitude
                    previous_point = point

        for i, header in enumerate(headers):
            tableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
        # Set time label initial value


def import_gpx_file_module(tableModel: QStandardItemModel, fileName):
    """Updates the table with the trajectory found in a given .gpx file with interpolation
    computed globally by module

    Args:
        tableModel (QStandardItemModel): the table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file

    Returns:
        Any: null
    """
    gpx_datas = gpx_interpolate(
        gpx_read(fileName), 5)  #TODO resolution to be defined
    first_interp_point_time = GPXTrackPoint(
        gpx_datas['lat'][0], gpx_datas['lon'][0], gpx_datas['ele'][0], gpx_datas['tstamp'][0])
    previous_interp_point = first_interp_point_time
    previous_attitude = Attitude(0, 0, 0)
    for j in range(1, len(gpx_datas['lat'])):
        interp_point = GPXTrackPoint(
            gpx_datas['lat'][j], gpx_datas['lon'][j], gpx_datas['ele'][j], gpx_datas['tstamp'][j])
        attitude = compute_attitude_from_gpx(
            previous_attitude, previous_interp_point, interp_point)
        row = [
            QStandardItem(str(previous_interp_point.time)),
            QStandardItem(str(previous_interp_point.longitude)),
            QStandardItem(str(previous_interp_point.latitude)),
            QStandardItem(str(previous_interp_point.elevation*M_TO_FT)),
            QStandardItem(str(attitude.phi if (j > 1) else 0)),
            QStandardItem(str(attitude.theta)),
            QStandardItem(str(attitude.psi))
        ]
        tableModel.appendRow(row)
        previous_interp_point = interp_point
        previous_attitude = attitude
    for i, header in enumerate(FlightDatasManager.get_current_keys()):
            tableModel.setHeaderData(
                i, Qt.Orientation.Horizontal, header)
