from unittest import mock

import pytest

from tests.factories import CRUDNotifierModel, ChangeNotifierModel, SNSNotifierModel


@pytest.fixture
def mock_boto_client_sns():

    topics_page1 = {
        'Topics': [
            {'TopicArn': 'arn:aws:region:id:TEST__test1'},
            {'TopicArn': 'arn:aws:region:id:TEST__test2'},
            {'TopicArn': 'arn:aws:region:id:TEST2__test1'},
        ],
        'NextToken': 'TOKEN-FOR-PAGE-2',
    }

    topics_page2 = {
        'Topics': [
            {'TopicArn': 'arn:aws:region:id:TEST3__TEST3'},
            {'TopicArn': 'arn:aws:region:id:test__test_status'},
        ],
    }

    def list_topics(NextToken=None):
        if not NextToken:
            return topics_page1
        else:
            return topics_page2

    def create_topic(Name):
        return {'TopicArn': 'arn:test_create_topic:{}'.format(Name)}

    client = mock.Mock(
        list_topics=list_topics,
        publish=mock.Mock(),
        create_topic=create_topic,
    )

    return mock.patch('boto3.client', return_value=client)


@pytest.fixture
def crud_notifier_model():
    return CRUDNotifierModel


@pytest.fixture
def change_notifier_model():
    return ChangeNotifierModel


@pytest.fixture
def sns_notifier_model():
    return SNSNotifierModel
