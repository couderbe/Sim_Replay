from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

import gpxpy
import gpxpy.gpx

from gpxpy.gpx import GPXTrackPoint

def import_gpx_file(_mainTableModel:QStandardItemModel, fileName):
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

def compute_attitude(previous_point:GPXTrackPoint,point:GPXTrackPoint):
    heading = point.course_between(previous_point)
    return {"bank":0.0,"pitch":0.0,"heading":heading }