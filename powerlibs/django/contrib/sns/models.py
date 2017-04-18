import re

from powerlibs.django.restless.models import serialize_model
from powerlibs.aws.sns.publisher import SNSPublisher
from powerlibs.string_utils import snake_case


class SNSMixin:
    _sns_publishers = {}
    _sns_publisher_class = SNSPublisher

    def serialize(self):  # pragma: no cover
        return serialize_model(self)

    def sns_publisher(self, prefix):
        if prefix not in self._sns_publishers:
            publisher = self._sns_publisher_class(prefix)
            self._sns_publishers[prefix] = publisher

        return self._sns_publishers[prefix]

    @property
    def sns_prefixes(self):
        return [snake_case(type(self).__name__)]

    def sns_publish(self, topic, message):
        for prefix in self.sns_prefixes:
            publisher = self.sns_publisher(prefix)
            publisher.publish(topic, message)


class CRUDNotifierMixin(SNSMixin):
    def post_creation_crud_notifier(self, **context):
        self.sns_publish('created', self.serialize())

    def post_update_crud_notifier(self, **context):
        self.sns_publish('updated', self.serialize())

    def post_delete_crud_notifier(self, **context):
        self.sns_publish('deleted', self.serialize())


class ChangeNotifierMixin(SNSMixin):
    notable_fields = ['status']

    def retrieve_itself_from_database(self):  # pragma: no cover
        return type(self).objects.get(pk=self.pk)

    def pre_creation_change_notifier(self, **context):
        self._notable_fields_values = dict((field_name, None) for field_name in self.notable_fields)

    def post_creation_change_notifier(self, **context):
        return self.post_update_change_notifier(**context)

    def pre_update_change_notifier(self, **context):
        old_object = self.retrieve_itself_from_database()

        self._notable_fields_values = {}
        for field_name in self.notable_fields:
            value = getattr(old_object, field_name)
            self._notable_fields_values[field_name] = value

    def post_update_change_notifier(self, **context):
        for field_name, old_value in self._notable_fields_values.items():
            new_value = getattr(self, field_name)
            if new_value != old_value:

                if isinstance(new_value, bool):
                    safe_value = 'true' if new_value else 'false'
                elif new_value == '':
                    safe_value = 'blank'
                else:
                    safe_value = re.sub(r'[^a-z0-9_]+', '_', str(new_value).lower())

                if field_name == 'status':
                    if isinstance(self, CRUDNotifierMixin) and new_value in ('created', 'updated', 'deleted'):
                        return
                    topic_name = safe_value
                else:
                    topic_name = "{}__{}".format(field_name, safe_value)

                message = self.serialize()
                message['_old_value'] = old_value
                message['_changed_field'] = field_name

                self.sns_publish(topic_name, message)
