from django.db import models

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
