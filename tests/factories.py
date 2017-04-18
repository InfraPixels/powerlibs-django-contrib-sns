from powerlibs.django.contrib.eventful.models import EventfulModelMixin
from powerlibs.django.contrib.sns.models import CRUDNotifierMixin, ChangeNotifierMixin


class Model:
    def __init__(self, **kwargs):
        self.id = None
        self.pk = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self, *args, **kwargs):
        self.id = self.pk = 1

    def delete(self, *args, **kwargs):
        pass


class EventfulModel(EventfulModelMixin, Model):
    def __init__(self, *args, **kwargs):
        self.debug_info = {
            'pre_creation_handler_called': 0,
            'post_creation_handler_called': 0,
            'pre_update_handler_called': 0,
            'post_update_handler_called': 0,
            'pre_delete_handler_called': 0,
            'post_delete_handler_called': 0,
        }
        super().__init__(*args, **kwargs)

    def pre_creation_test(self, **context):
        self.debug_info['pre_creation_handler_called'] += 1

    def post_creation_test(self, **context):
        self.debug_info['post_creation_handler_called'] += 1

    def pre_update_test(self, **context):
        self.debug_info['pre_update_handler_called'] += 1

    def post_update_test(self, **context):
        self.debug_info['post_update_handler_called'] += 1

    def pre_delete_test(self, **context):
        self.debug_info['pre_delete_handler_called'] += 1

    def post_delete_test(self, **context):
        self.debug_info['post_delete_handler_called'] += 1


class MockedSerializableModel:
    name = 'No name'
    status = None
    activated = False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'activated': self.activated,
        }


class CRUDNotifierModel(MockedSerializableModel, CRUDNotifierMixin, EventfulModel):
    pass


class ChangeNotifierModel(MockedSerializableModel, ChangeNotifierMixin, EventfulModel):
    notable_fields = ['status', 'activated']

    def retrieve_itself_from_database(self):
        return ChangeNotifierModel()


class SNSNotifierModel(MockedSerializableModel, ChangeNotifierMixin, CRUDNotifierMixin, EventfulModel):
    status = None
