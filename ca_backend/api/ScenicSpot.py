from ..models.model import ScenicSpotInfo
from ..models.database import Database
from flask_restful import Resource, reqparse
import requests
import json
import re

class ScenicSpot(Resource):


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, default=None)
        parser.add_argument('Keyword', type=str, default=None)
        parser.add_argument('Ticketinfo', type=str, default=None)
        parser.add_argument('Travellinginfo', type=str, default=None)
        parser.add_argument('Add', type=str, default=None)
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=float, default=None, help='plz type the number')
        args = parser.parse_args()
        result = {'data': ScenicSpotInfo.get(args)}
        return result

    def post(self):
        # pylint: disable=no-member
        """
        Input list in json body.
        {
            "IdList":["C1_382000000A_402683", "C1_376430000A_000136"]
        }
        """
        RETURN_FIELD = "Location"
        parser = reqparse.RequestParser()
        parser.add_argument('IdList', type=str, default=None, action='append')
        args = parser.parse_args()
        result_dict = json.loads(ScenicSpotInfo.objects(Id__in=args['IdList']).only(RETURN_FIELD).to_json())
        result = {'data': result_dict}
        return result

    def put(self):
        return ScenicSpotInfo.insert_all()

    def delete(self):
        result = ScenicSpotInfo.delete()
        return {'collection': result, 'status': "successed"}
