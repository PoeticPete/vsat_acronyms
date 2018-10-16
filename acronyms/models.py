from django.db import models
from django.contrib.auth.models import User
# from Profiles.models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from acronyms.search_indexes import AcronymIndex
import uuid


# Create your models here.
class Acronym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    acronym = models.TextField(null=False, blank=False, db_index=True)
    definition = models.TextField(null=False, blank=False)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def indexing(self):
        """
        Saves the acronym to elasticsearch index
        :return: indexed object as dictionary
        """
        obj = AcronymIndex(
            meta={'id': self.id},
            acronym=self.acronym,
            definition=self.definition,
            description=self.description,
            created=self.created,
            id=self.id
        )
        obj.save()
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=Acronym)
def index_acronym(sender, instance, **kwargs):
    """
    Saves the new userprofile to the elasticsearch index
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.indexing()


@receiver(post_delete, sender=Acronym)
def delete_acronym_from_index(sender, instance, **kwargs):
    """
    Automatically delete userprofile from the elasticsearch index when it is deleted from the master database
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.delete_from_index()
