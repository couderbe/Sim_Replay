from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

import gpxpy
import math

from gpxpy.gpx import GPXTrackPoint
from src.main.python.importer.specific_parsers import SpecificParser
from src.main.python.datas.datas_manager import FlightDatasManager
from src.main.python.flight_model.flight_model import Attitude, compute_attitude_from_gpx
from src.main.python.tools.gpx_interpolate import GPXData, gpx_interpolate, gpx_read

M_TO_FT = 1/0.3048


def import_gpx_file(tableModel: QStandardItemModel, fileName, limit=math.inf, ref_time_used=False, with_supp_data=False):
    """Updates the table with the trajectory found in a given .gpx file

    Args:
        tableModel (QStandardItemModel): the table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file
        limit (int): an optional limit of imported rows
        ref_time_used (Boolean): whether the first time point is used as reference
        with_supp_data (bool): if supplementary data are retrieved from description tag

    Returns:
        Any: null
    """
    with open(fileName, 'r') as gpxfile:
        reader_gpx = gpxpy.parse(gpxfile)
        headers = FlightDatasManager.get_current_keys()
        first_point = reader_gpx.tracks[0].segments[0].points[0]
        
        previous_point = first_point        
        
        if with_supp_data:
            spec_parser = SpecificParser(first_point.description)
            previous_specific = spec_parser.parse_data(first_point.description)

        for track in reader_gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    if i > 0:
                        attitude = Attitude(0, 0, 0)
                        row = [
                            QStandardItem(
                                str(previous_point.time_difference(first_point) if ref_time_used else previous_point.time.timestamp())),
                            QStandardItem(str(previous_point.latitude)),
                            QStandardItem(str(previous_point.longitude)),
                            QStandardItem(str(previous_point.elevation)),
                            QStandardItem(str(attitude.phi)),
                            QStandardItem(str(attitude.theta)),
                            QStandardItem(str(attitude.psi))
                        ]
                        
                        if with_supp_data:
                            # Add and update specific values
                            for v in previous_specific.values():
                                row.append(QStandardItem(str(v)))
                            previous_specific = spec_parser.parse_data(point.description)

                        tableModel.appendRow(row)
                        
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
            
        if with_supp_data:
            for i, header in enumerate(spec_parser.headers.keys()):
                tableModel.setHeaderData(
                    len(headers) + i, Qt.Orientation.Horizontal, header)
        # Set time label initial value

def import_gpx_file_module(tableModel: QStandardItemModel, fileName, ref_time_used=False):
    """Updates the table with the trajectory found in a given .gpx file with interpolation
    computed globally by module

    Args:
        tableModel (QStandardItemModel): the table that displays the trajectory 
        fileName (String): the file name of the imported .gpx file
        ref_time_used (Boolean): whether the first time point is used as reference

    Returns:
        Any: null
    """
    gpx_datas = gpx_interpolate(
        gpx_read(fileName), 2)  #TODO resolution to be defined
    first_interp_point_time = GPXTrackPoint(
        gpx_datas['lat'][0], gpx_datas['lon'][0], gpx_datas['ele'][0], gpx_datas['tstamp'][0])
    ref_tstamp = first_interp_point_time.time if ref_time_used else 0.0
    previous_interp_point = first_interp_point_time
    previous_attitude = Attitude(0, 0, 0)
    for j in range(1, len(gpx_datas['lat'])):
        interp_point = GPXTrackPoint(
            gpx_datas['lat'][j], gpx_datas['lon'][j], gpx_datas['ele'][j], gpx_datas['tstamp'][j])
        attitude = compute_attitude_from_gpx(
            previous_attitude, previous_interp_point, interp_point)
        row = [
            QStandardItem(str(previous_interp_point.time-ref_tstamp)),
            QStandardItem(str(previous_interp_point.latitude)),
            QStandardItem(str(previous_interp_point.longitude)),
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