import datetime
from haystack import indexes
from models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    # location
    # tags
    # times

    def get_model(self):
        return Event

    # def index_queryset(self, using=None):
    #     # Only indexes events that are more current than now
    #     # TODO: do we still want to index old events?
    #     return self.get_model().objects.filter(pub_date__gte=datetime.datetime.now())
