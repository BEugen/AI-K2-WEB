from django.db import models
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
# Create your models here.


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
            jsd['stamp'] = jsd['stamp'].strftime("%d.%m.%Y %H:%M")
            if jsd['idnext'] is not None:
                sql_val_n = conveyer2next.objects.filter(id__exact=str(jsd['idnext'])).values()
                jsdn = dict(sql_val_n[0])
                jsdn['id'] = str(jsdn['id'])
                jsd['idnext'] = jsdn
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
