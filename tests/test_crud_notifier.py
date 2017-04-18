import json

import pytest


pytestmark = pytest.mark.django_db


def test_CRUDNotifierModel_creation(mock_boto_client_sns, crud_notifier_model):
    """
    XXX: These tests SHOULD be separated in new functions,
    but there is SOMETHING that won't allow this way to
    function properly, so I simply glued everything
    together. Sorry for that...
    """
    with mock_boto_client_sns as mock_sns:
        mocked_publisher = mock_sns.return_value.publish
        instance = crud_notifier_model(name='creation test')
        instance.save()

        assert mocked_publisher.call_count == 1

        args, kwargs = mocked_publisher.call_args
        message = json.loads(kwargs['Message'])
        data = json.loads(message['default'])

        assert kwargs['TopicArn'] == 'arn:test_create_topic:crud_notifier_model__created'
        assert data['id'] == instance.id
        assert data['name'] == 'creation test'

        # ----------------------------------------------
        # def test_CRUDNotifierModel_update(mock_boto_client_sns, crud_notifier_model):
        instance.name = 'new name'
        instance.save()

        assert mock_sns.return_value.publish.call_count == 2  # For the UPDATE notification

        args, kwargs = mock_sns.return_value.publish.call_args
        message = json.loads(kwargs['Message'])
        data = json.loads(message['default'])

        assert kwargs['TopicArn'] == 'arn:test_create_topic:crud_notifier_model__updated'
        assert data['id'] == instance.id
        assert data['name'] == 'new name'

        # ----------------------------------------------
        # def test_CRUDNotifierModel_deletion(mock_boto_client_sns, crud_notifier_model):
        instance.delete()
        assert mock_sns.return_value.publish.call_count == 3  # For the DELETE notification

        args, kwargs = mock_sns.return_value.publish.call_args
        message = json.loads(kwargs['Message'])
        data = json.loads(message['default'])

        assert kwargs['TopicArn'] == 'arn:test_create_topic:crud_notifier_model__deleted'
        assert data['id'] == instance.id
        assert data['name'] == 'new name'
