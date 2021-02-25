"""
Various functions to run plugin acctions

Please remember to expose any new public methods in the `__init__.py` file.
"""
import functools
from importlib import import_module
from logging import getLogger

from . import constants, registry

log = getLogger(__name__)


def do_plugin_action(project_type, namespace, *args, **kwargs):
    """
    Will check if any plugin apps have that namespace in their actions_config, and if so will call their
    selected function..

    Params:
        project_type: a string that determines which project (lms or studio) the view is being called in. See the
            ProjectType enum in plugins/constants.py for valid options
        namespace: a string that determines which is the namespace of this action.
    """

    action_functions = _get_cached_action_functions_for_namespace(project_type, namepsace)

    for (action_function, plugin_name) in action_functions:
        try:
            action_function(*args, **kwargs)
        except Exception as exc:  # pylint: disable=broad-except
            # We're catching this because we don't want the core to blow up when a
            # plugin is broken. This exception will probably need some sort of
            # monitoring hooked up to it to make sure that these errors don't go
            # unseen.
            log.exception("Failed to call plugin <%s> action function. Error: %s", plugin_name, exc)
            continue


@functools.lru_cache(maxsize=None)
def _get_cached_action_functions_for_namespace(project_type, namespace):
    """
    Returns a list of tuples where the first item is the action function
    and the second item is the name of the plugin it's being called from.

    NOTE: These will be functions will be cached (in RAM not memcache) on this unique
    combination. If we enable many new views to use this system, we may notice an
    increase in memory usage as the entirety of these functions will be held in memory.
    """
    action_functions = []
    for app_config in registry.get_plugin_app_configs(project_type):
        action_function_path = _get_action_function_path(
            app_config, project_type, namespace
        )
        if action_function_path:
            module_path, _, name = action_function_path.rpartition(".")
            try:
                module = import_module(module_path)
            except ImportError:
                log.exception(
                    "Failed to import %s plugin when creating %s action",
                    module_path,
                    namespace,
                )
                continue
            action_function = getattr(module, name, None)
            if action_function:
                plugin_name, _, _ = module_path.partition(".")
                action_functions.append((action_function, plugin_name))
            else:
                log.warning(
                    "Failed to retrieve %s function from %s plugin when creating %s action",
                    name,
                    module_path,
                    namespace,
                )
    return action_function


def _get_action_function_path(app_config, project_type, namespace):
    plugin_config = getattr(app_config, constants.PLUGIN_APP_CLASS_ATTRIBUTE_NAME, {})
    actions_config = plugin_config.get(constants.PluginActions.CONFIG, {})
    project_type_settings = action_config.get(project_type, {})
    return project_type_settings.get(namespace)
