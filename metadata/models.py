from ast import literal_eval

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class MetaDataManager(models.Manager):
    '''This manager allow to with MetaData.objects as a Dict (useful for
    templates).'''
    def __getitem__(self, key):
        '''Return the value of metadata or None if not found'''
        try:
            return self.get_query_set().get(name=key).value
        except MetaData.DoesNotExist:
            return None

    def __setitem__(self, key, value):
        try:
            metadata = self.instance.metadata.get(name=key)
            metadata.value = value
            metadata.save()
        except MetaData.DoesNotExist:
            metadata = self.instance.metadata.create(name=key, value=value)

    def __contains__(self, key):
        try:
            if not self[key] is None:
                return True
            else:
                return False
        except IndexError:
            return False

    def __iter__(self):
        return self.iteritems()

    def iterkeys(self):
        for metadata in self.get_query_set().order_by('name'):
            yield metadata.name

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        # This way we can zip iterkeys and itervalues and retrieve the correct
        # information
        for metadata in self.get_query_set().order_by('name'):
            yield metadata.value

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        for metadata in self.get_query_set().order_by('name'):
            yield metadata.name, metadata.value

    def items(self):
        return list(self.iteritems())


class MetaData(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    _value = models.CharField(max_length=256, db_index=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = MetaDataManager()

    @property
    def value(self):
        '''Return the value as a Python literal if possible.'''
        try:
            return literal_eval(self._value)
        except ValueError:
            return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def as_tuple(self):
        '''Return a tuple in the format (name, value)'''
        return (self.name, self.value)

    def __repr__(self):
        return "".join(
            'MetaData(',
            'name=%s, ' % self.name,
            'value=%s, ' % self.value,
            'content_type=%s, ' % self.content_type.name,
            'object_id=%s)' % self.object_id
        )
