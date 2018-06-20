from django.db import models
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
# Create your models here.

t_class = {'-1': 'Простой', '0': 'Без мат.', '2': 'Пыль', '1': 'Не расп.', '3': 'Брик., мелочь', '4': 'Брик.'}
class conveyer2firstr(models.Model):
    id = models.UUIDField(primary_key=True)
    stamp = models.DateTimeField()
    predstop = models.FloatField()
    predempty = models.FloatField()
    predfull = models.FloatField()
    img = models.TextField()
    idnext = models.UUIDField(null=True)


class conveyer2next(models.Model):
    id = models.UUIDField(primary_key=True)
    nclass = models.IntegerField()
    predict0 = models.FloatField()
    predict1 = models.FloatField()
    predict2 = models.FloatField()
    predict3 = models.FloatField()
    predict4 = models.FloatField()


class conveyer2status(models.Model):
    id = models.UUIDField(primary_key=True)
    tstamp = models.DateTimeField()
    stop = models.FloatField()
    empty = models.FloatField()
    imerror = models.FloatField()
    full = models.FloatField()
    snn1 = models.TextField()
    snn2 = models.TextField()
    snn3 = models.TextField()
    snnclass = models.FloatField()
    img = models.TextField()
    tfile = models.DateTimeField()

class conveyer2imgcrop(models.Model):
    tstamp = models.DateTimeField()
    x1 = models.FloatField()
    x2 = models.FloatField()
    y1 = models.FloatField()
    y2 = models.FloatField()


class convstat(models.Model):
    id = models.UUIDField(primary_key=True)
    nclass = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()


class Getdata(object):
    def get_json_data(self):
        try:
            sql_val = conveyer2firstr.objects. \
                          order_by('-stamp')[:1].all().values()
            jsd = dict(sql_val[0])
            jsd['id'] = str(jsd['id'])
            jsd['stamp'] = jsd['stamp'].strftime("%d.%m.%Y %H:%M:%S")
            if jsd['idnext'] is not None:
                sql_val_n = conveyer2next.objects.filter(id__exact=str(jsd['idnext'])).values()
                jsdn = dict(sql_val_n[0])
                jsdn['id'] = str(jsdn['id'])
                jsd['idnext'] = jsdn
            return jsd
        except Exception as e:
            print(e)
            return []

class GetDataRecognize(object):
    def get_json_data(self):
        try:
            sql_val = conveyer2status.objects. \
                          order_by('-tstamp')[:1].all().values()
            jsd = dict(sql_val[0])
            jsd['id'] = str(jsd['id'])
            jsd['tstamp'] = jsd['tstamp'].strftime("%d.%m.%Y %H:%M:%S")
            jsd['tfile'] = jsd['tfile'].strftime("%d.%m.%Y %H:%M:%S")
            return jsd
        except Exception as e:
            print(e)
            return []

class Getstat(object):
    def get_json_stat(self, sdt):
        try:
            result = {'0': {}, '1': {}, '2': {}}
            dtc = datetime.now()
            dtc = datetime(dtc.year, dtc.month, dtc.day, 0, 0, 0, tzinfo=pytz.UTC)
            for x in range(0, 3):
                dte = dtc + timedelta(hours=8)
                for y in range(-1, 5):
                    sql_val = convstat.objects.filter(
                        start__gte=dtc, end__lt=dte, nclass__exact=y, end__isnull=False).annotate(
                        duration=F('end') - F('start')).aggregate(
                        total=Sum('duration')
                    )['total']
                    result[str(x)][str(y)] = sql_val.seconds/60 if sql_val else None
                dtc = dtc + timedelta(hours=8)
            return result
        except Exception as e:
            print(e)
            return []


class GetStatForChart(object):
    def get_json_stat_day(self):
        try:
            result = []
            dtc = datetime.now()
            dtc = datetime(dtc.year, dtc.month, dtc.day,
                           dtc.hour, dtc.minute, dtc.second, tzinfo=pytz.UTC)
            last_stat = convstat.objects.filter(
                start__lte=dtc, end__isnull=True).order_by('-start').annotate(
                duration=dtc - F('start')).all()[:1].values()[0]
            dtc = datetime(dtc.year, dtc.month, dtc.day, 0, 0, 0, tzinfo=pytz.UTC)
            dte = datetime(dtc.year, dtc.month, dtc.day, 23, 59, 59, tzinfo=pytz.UTC)
            for y in range(-1, 5):
                sql_val = convstat.objects.filter(
                    start__gte=dtc, end__lte=dte, nclass__exact=y, end__isnull=False).annotate(
                    duration=F('end') - F('start')).aggregate(
                    total=Sum('duration')
                )['total']
                add_seconds = 0
                if last_stat and y == last_stat['nclass']:
                    add_seconds = last_stat['duration'].seconds
                result.append([[t_class[str(y)],
                                (sql_val.seconds + add_seconds)/3600 if sql_val else add_seconds/3600
                                if add_seconds != 0 else None]])
            return result
        except Exception as e:
            print(e)
            return []

    def get_json_stat_ses(self, number):
        try:
            result = []
            dtc = datetime.now()
            dtc = datetime(dtc.year, dtc.month, dtc.day,
                           dtc.hour, dtc.minute, dtc.second, tzinfo=pytz.UTC)
            last_stat = convstat.objects.filter(
                start__lte=dtc, end__isnull=True).order_by('-start').annotate(
                    duration=dtc - F('start')).all()[:1].values()[0]
            hour = int(dtc.hour/8)*8
            dtc = datetime(dtc.year, dtc.month, dtc.day, hour, 0, 0, tzinfo=pytz.UTC)
            dtc = dtc - timedelta(hours=number*8)
            dte = dtc + timedelta(hours=8)
            for y in range(-1, 5):
                sql_val = convstat.objects.filter(
                    start__gte=dtc, end__lt=dte, nclass__exact=y, end__isnull=False).annotate(
                    duration=F('end') - F('start')).aggregate(
                    total=Sum('duration')
                )['total']
                add_seconds = 0
                if last_stat and y == last_stat['nclass'] and number == 0:
                    add_seconds = last_stat['duration'].seconds
                result.append([[t_class[str(y)],
                                (sql_val.seconds + add_seconds)/3600 if sql_val else add_seconds/3600
                                if add_seconds != 0 else None]])

            ses = ''
            if dtc.hour == 0:
                ses = '№1'
            if dtc.hour == 8:
                ses = '№2'
            if dtc.hour == 16:
                ses = '№3'
            return result, dtc.strftime("%d.%m.%y") + ' ' + ses
        except Exception as e:
            print(e)
            return []

