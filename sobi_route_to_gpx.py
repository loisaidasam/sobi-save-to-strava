#!/usr/bin/env python

import argparse
import datetime
import json

import gpxpy.gpx
import pytz


TIMEZONE_DEFAULT = 'America/New_York'

# This is the `gpxpy`'s default `creator` value:
# CREATOR_DEFAULT = 'gpx.py -- https://github.com/tkrajina/gpxpy'
# TODO: Come up with our own, something like this:
# CREATOR_DEFAULT = 'sobi-route-to-gpx.py -- https://github.com/loisaidasam/sobi-route-to-gpx'
CREATOR_DEFAULT = None


def main():
    args = parse_args()
    with open(args.route_filename, 'r') as fp:
        route = json.load(fp)
    timezone = args.timezone and pytz.timezone(args.timezone) or None
    gpx = convert(route, timezone)
    if args.creator:
        gpx.creator = args.creator
    print gpx.to_xml()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('route_filename',
                        help="The filename of a JSON file representing a SoBi route")
    # TODO: Use `route`'s `start_time` / `finish_time` for auto-detecting timezone
    parser.add_argument('--timezone',
                        default=TIMEZONE_DEFAULT,
                        help="The timezone the coordinates came from. Default: '%s'" % TIMEZONE_DEFAULT)
    parser.add_argument('--creator',
                        default=CREATOR_DEFAULT,
                        help="A custom value for the base gpx element's 'creator' attribute")
    return parser.parse_args()


def convert(route, timezone):
    """Convert a JSON representation of a SoBi route into a gpxpy.gpx.GPX object

    """
    # TODO: Determine good values for `name`/`description`
    name = "SoBi route #%s" % route['id']
    description = None
    # The GPX object
    gpx = gpxpy.gpx.GPX()
    # The GPXTrack
    gpx_track = gpxpy.gpx.GPXTrack(name=name, description=description)
    gpx.tracks.append(gpx_track)
    # The GPXTrackSegment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    # Now add all of the coordinate data
    coordinates = route_coordinates_generator(route, timezone)
    for coordinate in coordinates:
        trackpoint = gpxpy.gpx.GPXTrackPoint(**coordinate)
        gpx_segment.points.append(trackpoint)
    return gpx


def route_coordinates_generator(route, timezone):
    """
    {
      "path": {
        "type": "LineString",
        "coordinates": [
          [
            -84.36963166666666,
            33.746605,
            1549299522
          ],
          ...
    }
    """
    # Make sure the route looks like we think it should
    path = route['path']
    # Not sure what other types can be here:
    assert path['type'] == "LineString"
    for coordinate in path['coordinates']:
        yield format_route_path_coordinate(coordinate, timezone)


def format_route_path_coordinate(coordinate, timezone):
    """
    Params:
        coordinate::tuple(
            longitude::float
            latitude::float
            timestamp::int
                A timezone-naive local timestamp
        )
        timezone::datetime.tzinfo
    Returns:
        ::dict{
            latitude::float
            longitude::float
            time::datetime.datetime
        }
    """
    longitude, latitude, timestamp = coordinate
    time = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
    time_utc = time.astimezone(pytz.utc)
    return {
        'latitude': latitude,
        'longitude': longitude,
        'time': time_utc,
    }


if __name__ == '__main__':
    main()
