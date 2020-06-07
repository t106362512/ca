from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, post_load, INCLUDE, RAISE, EXCLUDE
from json import JSONEncoder
import marshmallow_mongoengine as ma
import mongoengine as me
# from . import db as me
# from ca_backend import db


class Base(Schema):

    Locations_iot_navigationLink = fields.URL()
    HistoricalLocations_iot_navigationLink = fields.URL()
    Datastreams_iot_navigationLink = fields.URL()
    MultiDatastreams_iot_navigationLink = fields.URL()
    _iot_id = fields.Int()
    _iot_selfLink = fields.URL()
    _iot_nextLink = fields.URL()
    _iot_count = fields.Int()

    @pre_load
    def change_key_name(self, data, **kwargs):
        if isinstance(data, dict):
            return {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}


class LocationM(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    encodingType = fields.Str(required=True)
    location = fields.Raw(required=True)


class Observation(Base):
    class Meta:
        unknown = True
    phenomenonTime = fields.DateTime()
    resultTime = fields.Str(allow_none=True)
    result = fields.Raw()
    properties = fields.Raw()


class Thing(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    properties = fields.Raw()


class Datastream(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    observationType = fields.URL()
    unitOfMeasurement = fields.Raw()
    phenomenonTime = fields.Str()
    phenomenon_time_start = fields.DateTime()
    phenomenon_time_end = fields.DateTime()

    @pre_load
    def spilt_phenomenonTime(self, data, **kwargs):
        if 'phenomenonTime' in data:
            (data['phenomenon_time_start'], data['phenomenon_time_end']) = str(
                data['phenomenonTime']).split('/')
            return data


class Datastreams(Base):
    class Meta:
        model = Datastream
    value = fields.List(fields.Nested(Datastream))


class LocationsInThing(Thing):
    Locations = fields.List(fields.Nested(LocationM))


class ThingAndLocationInDatastream(Datastream):
    Observations = fields.List(fields.Nested(
        Observation), data_key='Observations')
    Thing = fields.Nested(LocationsInThing, data_key='Thing')


class FullDatastream(Schema):
    # class Meta:
    #     fields = ('value')
    _iot_count = fields.Int(data_key='@iot.count')
    _iot_nextLink = fields.URL(data_key='@iot.nextLink')
    value = fields.List(fields.Nested(ThingAndLocationInDatastream))


class ScenicSpotInfo(me.Document):
    Id = me.StringField()
    Name = me.StringField()
    Zone = me.StringField()
    Toldescribe = me.StringField()
    Description = me.StringField()
    Tel = me.StringField()
    Add = me.StringField()
    Zipcode = me.StringField()
    Region = me.StringField()
    Town = me.StringField()
    Travellinginfo = me.StringField()
    Opentime = me.StringField()
    Picture1 = me.StringField()
    Picdescribe1 = me.StringField()
    Picture2 = me.StringField()
    Picdescribe2 = me.StringField()
    Picture3 = me.StringField()
    Picdescribe3 = me.StringField()
    Map = me.StringField()
    Gov = me.StringField()
    Px = me.FloatField()
    Py = me.FloatField()
    Orgclass = me.StringField()
    Class1 = me.StringField()
    Class2 = me.StringField()
    Class3 = me.StringField()
    Level = me.StringField()
    Website = me.StringField()
    Parkinginfo = me.StringField()
    Parkinginfo_Px = me.FloatField()
    Parkinginfo_Py = me.FloatField()
    Ticketinfo = me.StringField()
    Remarks = me.StringField()
    Keyword = me.StringField()
    Changetime = me.DateTimeField()
    Location = me.GeoPointField()
    Keywords = me.ListField()

    meta = {
        # 'indexes': [
        # {
        #     'fields': ['$Name', "$Toldescribe"],
        #     'default_language': 'english',
        #     'weights': {'Name': 5, 'Toldescribe': 10}
        #  }
        # ],
        'auto_create_index': True
    }

    def __repr__(self):
        return '<ScenicSpotInfo(name={self.name!r})>'.format(self=self)

    def to_dict(self):
        return self.__dict__
