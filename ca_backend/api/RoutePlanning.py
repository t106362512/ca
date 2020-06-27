# from ..models.RoutePlaningModel import RoutePlaning
from ..resource.RoutePlanning import RoutePlanning as RP
from ..models.model import CILocation, Datastream
from flask_restful import Resource, reqparse
import requests
import json
import re

class RoutePlanning(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('LocaltionList', type=list, default=None, help='plz type like the [121.297187,24.943325]')
        args = parser.parse_args()
        localtion_list = args['LocaltionList']
        min_path_length, min_path_list = RP().get_shortest(localtion_list)
        result = {'MinPathLen': min_path_length, 'MinPathList': min_path_length}
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Localtion', type=str, default=None, help='plz type like the [121.297187,24.943325]')
        args = parser.parse_args()
        for sta in ['STA_AirQuality_v2', 'STA_Rain']:
            loc_array = CILocation.get(args+{'Station': sta})[0]['location']['coordinates']
            si = Datastream.get_station_info(sta, loc_array)


    def put(self):
        pass

    def delete(self):
        pass
