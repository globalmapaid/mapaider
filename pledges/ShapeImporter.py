import os
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.contrib.gis.gdal import DataSource, GDALException
from .models import Pledge, PledgeType


class ShapeImporter:
    @classmethod
    def _convert_date(cls, date_string):
        try:
            if date_string.endswith('UTC'):
                dt =   datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S UTC')
            elif date_string.endswith('.000'):
                dt =   datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.000')
            elif str(date_string).count('-') == 2:
                dt =   datetime.strptime(date_string, '%Y-%m-%d')
            elif str(date_string).count('/') == 2:
                try:
                    dt =   datetime.strptime(date_string, '%d/%m/%Y')
                except ValueError:
                    dt =   datetime.strptime(date_string, '%d/%m/%y')
            elif date_string is None:
                dt =   datetime.now().replace(microsecond=0)
            else:
                dt =   datetime.now().replace(microsecond=0)
        except AttributeError:
            dt =  datetime.now().replace(microsecond=0)
        finally:
            uk = timezone('Europe/London')
            return uk.localize(dt)            

    @classmethod
    def import_farm_pledges(cls):
        filename = 'Farm_Pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='farm-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = feat.get('acres') if feat.get('acres') is not None else 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='acres',
                first_name=feat.get('Name'),
                street=feat.get('Your stree'),
                city=feat.get('Area'),
                postcode=str(feat.get('Postcode')).upper(),
                notes=feat.get('Notes'),
                submitted_at=cls._convert_date(feat.get('Submission')),
                visibility=4
            )

            new_pledge.save()

    @classmethod
    def import_garden_pledges(cls):
        filename = 'Garden_Pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='garden-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = feat.get('Acres') if feat.get('Acres') is not None else 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='acres',
                first_name=feat.get('Firstname'),
                last_name=feat.get('Surname'),
                email=feat.get('Email'),
                phone=feat.get('Phone'),
                street=feat.get('Address'),
                city=feat.get('Area'),
                postcode=str(feat.get('Postcode')).upper(),
                notes=feat.get('Notes'),
                submitted_at=cls._convert_date(feat.get('date')),
                visibility=4
            )

            new_pledge.save()


    @classmethod
    def import_church_pledges(cls):
        filename = 'Church_Pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='church-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='acres',
                first_name=feat.get('name'),
                notes=feat.get('Notes'),
                submitted_at=datetime.now(tz=timezone('UTC')),
                visibility=4
            )

            new_pledge.save()


    @classmethod
    def import_school_pledges(cls):
        filename = 'School_Pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='school-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='acres',
                first_name=feat.get('name'),
                notes=feat.get('Notes'),
                submitted_at=datetime.now(tz=timezone('UTC')),
                visibility=4
            )

            new_pledge.save()

    @classmethod
    def import_government_pledges(cls):
        filename = 'Government_Pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='government-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = feat.get('Hectares') if feat.get('Hectares') is not None else 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='ha',
                first_name=feat.get('Council'),
                street=feat.get('Location'),
                notes=feat.get('Descriptio'),
                reason=feat.get('ReasonForP'),
                submitted_at=datetime.now(tz=timezone('UTC')),
                visibility=4
            )

            new_pledge.save()

    @classmethod
    def import_railway_stations_pledges(cls):
        filename = 'Railway_stations_pledges.shp'
        file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'shape', filename))

        pledge_type = PledgeType.objects.get(slug='railway-stations-pledges')

        ds = DataSource(file_path)
        layer = ds[0]

        for i, feat in enumerate(layer):
            try:
                geom = feat.geom.wkt
                geom_type = feat.geom.geom_type
            except GDALException:
                geom = None
                geom_type = None

            area = 0

            new_pledge = Pledge(
                type=pledge_type,
                area=area,
                geom=geom,
                geom_type=geom_type,
                measurement_unit='acres',
                first_name=feat.get('Station ad'),
                postcode=feat.get('Postcode'),
                city=feat.get('Region'),
                submitted_at=datetime.now(tz=timezone('UTC')),
                visibility=4
            )

            new_pledge.save()
