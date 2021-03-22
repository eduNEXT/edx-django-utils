Hooks tooling: pipeline
=======================

Status
------

Draft

Context
-------

Taking into account the design considerations outlined in OEP-50 Hooks extension framework about

  1. The order of execution for multiple actions must be respected
  2. The result of a previous action must be available to the current one

We must implement a pattern that follows this considerations: a Pipeline for the set of functions, i.e actions or filters,
listening on a trigger.

Checkout https://github.com/edx/open-edx-proposals/pull/184 for more information.

To do this, we considered three similar approaches for the pipeline implementation:

1. Unix-like (how unix pipe operator works): the output of the previous function is the input of the next one. For the first function, includes the initial arguments.
2. Unix-like modified: the output of the previous function is the input of the next one including the initial arguments for all functions.
3. Accumulative: the output of every (i, …, i-n) function is accumulated using a data structure and fed into the next function i-n+1, including the initial arguments.

They follow the pipeline pattern and have as main difference what each function receive as input.

Decision
--------

We decided to use the accumulative approach as the only pipeline for both actions and filters.

Consequences
------------

1. Actions listening on a trigger must return None. Either way their result will be ignored.
2. Given that we are using just one pipeline with actions and filters listening on triggers, the behavior when executing them will be the same.
3. Given that actions and filters will expect the same input arguments, i.e accumulated output plus initial arguments, their signature will stay the same. And for this reason, these functions are interchangeable.
4. For the above reasons, actions and filters must have \*args and \*\*kwargs in their signature.
