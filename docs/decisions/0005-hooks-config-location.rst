Where to configure Hooks Extensions Framework
=============================================

Status
------

Draft

Context
-------

We need a way to configure a list of functions (actions or filters) that will be called at different places (triggers) in the code of edx-platform.

So, for a string like:

"openedx.lms.auth.post_login.action.v1"

We need to define a list of functions:

.. code-block:: python

    [
        "from_a_plugin.actions.action_1",
        "from_a_plugin.actions.action_n",
        "from_some_other_package.actions.action_1",
        # ... and so.
    ]

And also some extra variables:

.. code-block:: python

    {
        "async": True, # ... and so.
    }

We have considered two alternatives:

* A dict in the Django settings.
    * Advantages:
        * It is very standard, everyone should know how to change it by now.
        * Can be altered without installing plugins.
    * Disadvantages:
        * It is hard to document a large dict.
        * Could grow into something difficult to manage.

* In a view of the AppConfig of your plugin.
    * Advantages:
        * Each plugin can extend the config to add its own actions and filters without collisions.
    * Disadvantages:
        * It’s not possible to control the ordering of different actions being connected to the same trigger by different plugins.
        * For updates, an operator must install a new version of the dependency which usually is longer and more difficult than changing vars and restart.
        * Not easy to configure by tenant if you use site configs.
        * Requires a plugin.

Decision
--------

We decided to use a dict in Django settings.

Consequences
------------

The only way of configure Hooks Extensions Framework is via Django settings using the specified format.
