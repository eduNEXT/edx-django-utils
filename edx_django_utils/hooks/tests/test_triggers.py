"""
Tests for `edx-django-utils` hooks triggers.
"""
from unittest.mock import Mock, patch

from django.test import TestCase

from ..triggers import trigger_action, trigger_filter


class TestTriggerFilter(TestCase):
    """
    Test class to verify standard behavior of trigger_filter.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.kwargs = {
            "request": Mock(),
        }

    @patch("edx_django_utils.hooks.triggers.run_pipeline")
    @patch("edx_django_utils.hooks.triggers.get_pipeline_configuration")
    def test_affecting_execution(self, get_configuration_mock, run_pipeline_mock):
        """
        This method runs trigget_filter affecting the application flow raising exceptions.

        Expected behavior:
            Run pipeline is called with raise_exception equals to True.
        """
        pipeline, is_async = [], False
        get_configuration_mock.return_value = (
            pipeline,
            is_async,
        )
        run_pipeline_mock.return_value = None

        trigger_filter("trigger_name", **self.kwargs)

        run_pipeline_mock.assert_called_once_with(
            pipeline, raise_exception=True, **self.kwargs
        )

    @patch("edx_django_utils.hooks.triggers.run_pipeline")
    @patch("edx_django_utils.hooks.triggers.get_pipeline_configuration")
    def test_sync_filter_pipeline(self, get_configuration_mock, run_pipeline_mock):
        """
        This method runs trigget_filter with a sync pipeline.

        Expected behavior:
            Returns the output dictionary with the accumulated results.
        """
        pipeline = Mock()
        is_async = False
        filter_return_value = {
            "user": Mock(),
            **self.kwargs
        }
        get_configuration_mock.return_value = (
            pipeline,
            is_async,
        )
        run_pipeline_mock.return_value = filter_return_value

        result = trigger_filter("trigger_name", **self.kwargs)

        self.assertDictEqual(result, filter_return_value)
        run_pipeline_mock.assert_called_once_with(
            pipeline, raise_exception=True, **self.kwargs
        )

    def test_async_filter_pipeline(self):
        """
        This method runs trigget_filter with an async pipeline with the arguments defined.

        Expected behavior:
            A task is started using the pipeline function.
        """


class TestTriggerAction(TestCase):
    """
    Test class to verify standard behavior of trigger_action.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.kwargs = {
            "request": Mock(),
        }

    @patch("edx_django_utils.hooks.triggers.run_pipeline")
    @patch("edx_django_utils.hooks.triggers.get_pipeline_configuration")
    def test_not_affect_execution(self, get_configuration_mock, run_pipeline_mock):
        """
        This method runs trigger_action with a pipeline defined in configurations
        without affecting execution using exceptions.

        Expected behavior:
            Run pipeline is called with raise_exception equals to the default (False).
        """
        pipeline, is_async = Mock(), False
        get_configuration_mock.return_value = (
            pipeline,
            is_async,
        )

        trigger_action("trigger_name", **self.kwargs)

        run_pipeline_mock.assert_called_once_with(pipeline, **self.kwargs)

    @patch("edx_django_utils.hooks.triggers.run_pipeline")
    @patch("edx_django_utils.hooks.triggers.get_pipeline_configuration")
    def test_getting_no_result(self, get_configuration_mock, _):
        """
        This method runs trigger_action with a pipeline defined in configurations
        without returning processed data.

        Expected behavior:
            The return value of the action is None.
        """
        pipeline, is_async = Mock(), False
        get_configuration_mock.return_value = (
            pipeline,
            is_async,
        )

        self.assertIsNone(trigger_action("trigger_name", **self.kwargs))

    def test_async_action_pipeline(self):
        """
        This method runs an async action pipeline with the arguments defined.

        Expected behavior:
            A task is started using the pipeline function.
        """
