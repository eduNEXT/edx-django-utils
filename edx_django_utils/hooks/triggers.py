"""
Triggers for actions and filters.
"""
from .pipeline import run_pipeline
from .utils import get_pipeline_configuration


class Trigger:
    """Trigger base class."""

    def __init__(self, trigger_name):
        self.pipeline, self.is_async = get_pipeline_configuration(trigger_name)

    def __call__(self, *args, **kwargs):
        self.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        raise NotImplementedError()


class TriggerFilter(Trigger):

    def execute(self, *args, **kwargs):
        """
        Function that manages the execution of filters listening on a trigger. The execution
        follows the Pipeline pattern using the pipeline runner.

        Example usage:
            result = trigger_filter(
                'trigger_name_used_in_hooks_config',
                request,
                user=user,
            )
            >>> result
        {
            'result_test_function': Object,
            'result_test_function_2nd': Object_2nd,
        }

        Arguments:
            trigger_name (str): determines which trigger we are listening to. It also specifies which
            hook configuration to use when calling trigger_filter.

        Returns:
            result (dict): result of the pipeline execution, i.e the accumulated output of the filters defined in
            the hooks configuration.
        """
        if not self.pipeline:
            return kwargs

        if self.is_async:
            result = run_pipeline(
                self.pipeline, *args, raise_exception=True, **kwargs
            )  # TODO: change to async call.
        else:
            result = run_pipeline(self.pipeline, *args, raise_exception=True, **kwargs)

        return result


class TriggerAction(Trigger):

    def execute(self, *args, **kwargs):
        """
        Function that manages the execution of actions listening on a trigger action. The execution
        follows the Pipeline pattern using the pipeline runner.

        Example usage:
            trigger_action(
                'trigger_name_used_in_hooks_config',
                course_mode,
                user=user,
            )

        Arguments:
            trigger_name (str): determines which trigger we are listening to. It also specifies which
            hook configuration to use when calling trigger_action.

        Returns:
            None. By definition actions don't return any value.
        """
        if not self.pipeline:
            return

        if self.is_async:
            run_pipeline(self.pipeline, *args, **kwargs)  # TODO: change to async call.
        else:
            run_pipeline(self.pipeline, *args, **kwargs)
