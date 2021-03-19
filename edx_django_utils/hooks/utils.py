"""
Utilities for the hooks module.
"""
from importlib import import_module
from logging import getLogger

from django.conf import settings

log = getLogger(__name__)


def get_functions_for_pipeline(pipeline):
    """
    Helper function that given a pipeline with functions paths gets the objects related
    to each path.

    Example usage:
        triggers = get_functions_for_pipeline(['1st_path_to_function', ...])
        >>> triggers
        [
            <function 1st_function at 0x00000000000>,
            <function 2nd_function at 0x00000000001>,
            ...
        ]

    Arguments:
        pipeline (list): paths where functions are defined.

    Returns:
        function_list (list): function objects defined in pipeline.
    """
    function_list = []
    for function_path in pipeline:
        module_path, _, name = function_path.rpartition(".")
        try:
            module = import_module(module_path)
            function = getattr(module, name)
            function_list.append(function)
        except (ImportError, ModuleNotFoundError):
            log.exception(
                "Failed to import '%s' module when getting '%s' function.",
                module_path,
                name,
            )
        except AttributeError:
            log.exception(
                "Failed to retrieve '%s' function from path '%s'.", name, function_path,
            )

    return function_list


def get_pipeline_configuration(trigger_name):
    """
    Helper function used to get the configuration needed to run a pipeline.

    Example usage:
        pipeline_config = get_pipeline_configuration('trigger')
        >>> pipeline_config
            (
                [
                    'my_plugin.hooks.filters.test_function',
                    'my_plugin.hooks.filters.test_function_2nd',
                ],
                False,
            )

    Arguments:
        trigger_name (str): determines which is the trigger of this pipeline.

    Returns:
        pipeline (list): paths where functions for the pipeline are defined.
        is_async (bool): indicating how the pipeline is going to be executed. True for
        asynchronous and False for synchronous.
    """
    hook_config = get_hook_configurations(trigger_name)

    pipeline = hook_config.get("pipeline", [])
    is_async = hook_config.get("async", True)

    return pipeline, is_async


def get_hook_configurations(trigger_name):
    """
    Helper function used to get configuration needed for using Hooks Extension Framework.

    Example usage:
            configuration = get_hook_configurations('trigger')
            >>> configuration
            {
                'pipeline':
                    [
                        'my_plugin.hooks.filters.test_function',
                        'my_plugin.hooks.filters.test_function_2nd',
                    ],
                'async': False,
            }

    Arguments:
        trigger_name (str): determines which configuration to use.

    Returns:
        hooks configuration (dict): taken from Django settings containing hooks configuration.
    """
    hooks_config = getattr(settings, "HOOKS_EXTENSIONS_CONFIG", {})

    return hooks_config.get(trigger_name, {})
