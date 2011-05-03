from django.db import models


class Happy(models.Model):
    happy = models.BooleanField()
    day = models.DateTimeField(auto_now=True)
    reason = models.TextField(blank=True)
    done = models.BooleanField()

    def __unicode__(self):
        return '%s - %s' % (self.happy, self.reason)

    class Meta:
        ordering = ['-day']


class Advise(models.Model):
    happy = models.ForeignKey(Happy)
    ad = models.TextField()
    votes = models.IntegerField()

    def __unicode__(self):
        return '%s - %s - %s' % (self.happy, self.ad, self.votes)

    class Meta:
        ordering = ['-votes']


class Voter(models.Model):
    ad = models.ForeignKey(Advise)
    sid = models.CharField(max_length=255)
