# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import CharField, BooleanField, DateField
from django.db.models.fields.files import ImageField
from datetime import datetime

# Create your models here.

class Invite(models.Model):
    SENT = 'SE'
    SEEN = 'SN'
    ACCEPTED = 'AC'
    DECLINED = 'DC'
    STATE_CHOICES = (
        (SENT, u'Poslaná'),
        (SEEN, u'Prečítaná'),
        (ACCEPTED, u'Akceptovaná'),
        (DECLINED, u'Odmietnutá'),
    )
    user = ForeignKey(User)
    decision = ForeignKey('Decision')
    state = CharField(max_length=2, choices=STATE_CHOICES, default="SE")
    
class Decision(models.Model):
    NEW = 'NE'
    STAGE_ONE = 'SO'
    STAGE_TWO = 'ST'
    FINISHED = 'FI'
    STATE_CHOICES = (
        (NEW, u'Nové'),
        (STAGE_ONE, u'Prvá fáza'),
        (STAGE_TWO, u'Druhá fáza'),
        (FINISHED, u'Dokončené'),
    )
    name = CharField(max_length=200)
    description = CharField( max_length=200, blank=True)
    image = ImageField(null=True, blank=True)
    state = CharField(max_length=2, choices=STATE_CHOICES, default="NE")
    published = DateField(default=datetime.now())
    stage_one_date = DateField(null=True, blank=True)
    stage_two_date = DateField(null=True, blank=True)
    def __unicode__(self):
        return self.get_state_value() + "_" + self.name
    
class Criteria_Variant(models.Model):
    decision = ForeignKey(Decision)
    name = CharField(max_length=200)
    description = CharField(max_length=200, blank=True)
    image = ImageField(null=True, blank=True)
    crit_var = BooleanField(default=None)
    def __unicode__(self):
        return self.decision.__unicode__()+"_"+("Variant_" if self.crit_var else "Criteria_") +self.name
    
class Vote(models.Model):
    NOT_AT_ALL = 'NA'
    MORE_NOT = 'MN'
    UNDECIDED = 'UN'
    MORE_YES = 'MY'
    DEFINETLY_YES = 'DY'
    VOTE_CHOICES = (
        (NOT_AT_ALL, u'Vôbec nie'),
        (MORE_NOT, u'Skôr nie'),
        (UNDECIDED, u'Nezáleží'),
        (MORE_YES, u'Skôr áno'),
        (DEFINETLY_YES, u'Určite áno'),
    )
    user = ForeignKey(User)
    crit_var = ForeignKey(Criteria_Variant)
    value = CharField(max_length=2, choices=VOTE_CHOICES)
    def __unicode__(self):
        return self.crit_var.__unicode__() + "_" + self.user.__unicode__() + "_" +self.get_value_display()
    