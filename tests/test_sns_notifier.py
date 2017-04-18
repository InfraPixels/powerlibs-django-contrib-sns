from unittest import mock

import pytest


pytestmark = pytest.mark.django_db


def test_common_change_crud_notifier(mock_boto_client_sns, sns_notifier_model):
    with mock_boto_client_sns, mock.patch('powerlibs.aws.sns.publisher.SNSPublisher.publish') as mock_sns_publisher:
        instance = sns_notifier_model(name='Test name', status='created')
        instance.save()
        assert mock_sns_publisher.call_count == 1
