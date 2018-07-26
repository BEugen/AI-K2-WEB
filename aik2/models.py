from django.db import models
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import math
import json
import calendar
import numpy as np

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


class conv2seconds(models.Model):
    id = models.UUIDField(primary_key=True)
    nclass = models.IntegerField()
    ndate = models.DateTimeField()
    seconds = models.FloatField()


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
    def get_json_stat(self):
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
                    result[str(x)][str(y)] = sql_val.seconds / 60 if sql_val else None
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
                duration=dtc - F('start')).all()[:1].values()
            if len(last_stat) > 0:
                last_stat = last_stat[0]
            else:
                last_stat = None
            dtc = datetime(dtc.year, dtc.month, dtc.day, 0, 0, 0, tzinfo=pytz.UTC)
            dte = datetime(dtc.year, dtc.month, dtc.day, 23, 59, 59, tzinfo=pytz.UTC)
            allt = 0
            for y in range(-1, 5):
                sql_val = convstat.objects.filter(
                    start__gte=dtc, end__lte=dte, nclass__exact=y, end__isnull=False).annotate(
                    duration=F('end') - F('start')).aggregate(
                    total=Sum('duration')
                )['total']
                add_seconds = 0
                if last_stat and y == last_stat['nclass']:
                    add_seconds = last_stat['duration'].seconds
                allt += (sql_val.seconds + add_seconds) if sql_val else add_seconds
                result.append([[t_class[str(y)],
                                (sql_val.seconds + add_seconds) if sql_val else add_seconds
                                if add_seconds != 0 else None]])
            for x in result:
                if x[0][1] is not None:
                    x[0][1] = x[0][1] * 100.0 / allt if allt > 0 else 0
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
                duration=dtc - F('start')).all()[:1].values()
            if len(last_stat) > 0:
                last_stat = last_stat[0]
            else:
                last_stat = None
            hour = int(dtc.hour / 8) * 8
            dtc = datetime(dtc.year, dtc.month, dtc.day, hour, 0, 0, tzinfo=pytz.UTC)
            dtc = dtc - timedelta(hours=number * 8)
            dte = dtc + timedelta(hours=8)
            allt = 0
            for y in range(-1, 5):
                sql_val = convstat.objects.filter(
                    start__gte=dtc, end__lt=dte, nclass__exact=y, end__isnull=False).annotate(
                    duration=F('end') - F('start')).aggregate(
                    total=Sum('duration')
                )['total']
                add_seconds = 0
                if last_stat and y == last_stat['nclass'] and number == 0:
                    add_seconds = last_stat['duration'].seconds
                allt += (sql_val.seconds + add_seconds) if sql_val else add_seconds
                result.append([[t_class[str(y)],
                                (sql_val.seconds + add_seconds) if sql_val else add_seconds
                                if add_seconds != 0 else None]])

            ses = ''
            if dtc.hour == 0:
                ses = '№1'
            if dtc.hour == 8:
                ses = '№2'
            if dtc.hour == 16:
                ses = '№3'
            for x in result:
                if x[0][1] is not None:
                    x[0][1] = x[0][1] * 100.0 / allt if allt > 0 else 0
            return result, dtc.strftime("%d.%m.%y") + ' ' + ses
        except Exception as e:
            print(e)
            return []

    def get_json_fullstat(self, st, en):
        try:
            result = {0: {}, 1: {}, 2: {}, 3: {}}
            time_all = []
            chart_result = []
            dts = datetime.strptime(st, "%d.%m.%Y")
            dte = datetime.strptime(en, "%d.%m.%Y")
            dts = datetime(dts.year, dts.month, dts.day, 0, 0, 0, tzinfo=pytz.UTC)
            dte = datetime(dte.year, dte.month, dte.day, 23, 59, 59, tzinfo=pytz.UTC)
            dlt_time = (dte - dts).total_seconds() / 3
            sesion = 0
            max_all = 1.0
            max_ses = 1.0
            while dts < dte:
                all = 0
                for y in range(-1, 5):
                    sql_val = convstat.objects.filter(
                        start__gte=dts, end__lt=(dts + timedelta(hours=8)),
                        nclass__exact=y, end__isnull=False).annotate(
                        duration=F('end') - F('start')).aggregate(
                        total=Sum('duration')
                    )['total']
                    k = str(y)
                    val = sql_val.seconds if sql_val else 0
                    all += val
                    if sesion not in result or k not in result[sesion]:
                        result[sesion][k] = val
                        max_ses = max_ses if max_ses > val else val
                    else:
                        result[sesion][k] += val
                        max_ses = max_ses if max_ses > (result[sesion][k] + val) else (result[sesion][k] + val)
                    if 3 not in result or k not in result[3]:
                        result[3][k] = val
                        max_all = max_all if max_all > val else val
                    else:
                        result[3][k] += val
                        max_all = max_all if max_all > (result[3][k] + val) else (result[3][k] + val)
                sesion += 1
                time_all.append(all)
                dts = dts + timedelta(hours=8)
                if sesion > 2:
                    sesion = 0
            for i in range(0, 4):
                t = []
                for k in range(-1, 5):
                    if i < 3:
                        result[i][str(k)] = result[i][str(k)] * 100 / time_all[i] if time_all[i] != 0.0 else 0.0
                    else:
                        result[i][str(k)] = result[i][str(k)] * 100 / np.sum(time_all) \
                            if np.sum(time_all) != 0.0 else 0.0
                    t.append([[t_class[str(k)], result[i][str(k)]]])
                chart_result.append(t)
            max_ses = math.floor(max_ses * 0.10 + max_ses)
            max_all = math.floor(max_all * 0.10 + max_all)
            chart_result.append([[max_ses, max_all]])
            return chart_result
        except Exception as e:
            print(e)
            return []

    def get_json_protocol(self, direct, dtime):
        try:
            if dtime:
                dt = datetime.strptime(dtime, '%d.%m.%Y %H:%M:%S')
                dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=pytz.UTC)
                if direct and direct == '1':
                    sql_val = conveyer2status.objects.filter(tstamp__gt=dt).order_by('-tstamp')[:20].all().values()
                else:
                    sql_val = conveyer2status.objects.filter(tstamp__lt=dt).order_by('-tstamp')[:20].all().values()
            else:
                sql_val = conveyer2status.objects. \
                              order_by('-tstamp')[:20].all().values()
            for row in sql_val:
                row['id'] = str(row['id'])
                row['tstamp'] = json.dumps(row['tstamp'].strftime('%d.%m.%Y %H:%M:%S')).replace('"', '')
                row['tfile'] = json.dumps(row['tfile'].strftime('%d.%m.%Y %H:%M:%S')).replace('"', '')
            return [dict(sql) for sql in sql_val]
        except Exception as e:
            print(e)
            return []

    def get_json_thrend(self, id):
        try:
            result = []
            dtc = datetime.now()
            dte = datetime(dtc.year, dtc.month, dtc.day, dtc.hour, dtc.minute, dtc.second, tzinfo=pytz.UTC)
            dte = dte - timedelta(days=1)
            if id == '1':
                dtc = datetime(dtc.year, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
            else:
                dtc = datetime(dtc.year, dtc.month, 1, 0, 0, 0, tzinfo=pytz.UTC)
            while dtc < dte:
                for y in range(0, 6):
                    sql_val = conv2seconds.objects.filter(
                        ndate__gte=dtc, ndate__lt=(dtc + timedelta(days=1)), nclass__exact=(y - 1)).all().values()
                    allt = conv2seconds.objects.filter(
                        ndate__gte=dtc, ndate__lt=(dtc + timedelta(days=1))).aggregate(total=Sum('seconds'))['total']
                    if sql_val and len(sql_val) > 0:
                        sql_val = sql_val[0]['seconds']
                    else:
                        sql_val = None
                    if allt is None:
                        allt = 86400
                    if len(result) > y:
                        result[y]['data'].append([self.__convert_time_to_jscript(dtc), sql_val * 100.0 / allt
                                                if sql_val else 0])
                    else:
                        result.append({'label': t_class[str(y - 1)], 'data':
                            [[self.__convert_time_to_jscript(dtc), sql_val * 100.0 / allt
                            if sql_val else 0]]})
                dtc = dtc + timedelta(days=1)
            return result
        except Exception as e:
            print(e)
            return []

    def __convert_time_to_jscript(self, dt):
        return calendar.timegm(dt.timetuple()) * 1000
