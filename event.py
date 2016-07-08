#!/usr/bin/env python2
#
# Copyright 2016 Red Hat, Inc.
#
# Authors:
#     Fam Zheng <famz@redhat.com>
#
# This work is licensed under the MIT License.  Please see the LICENSE file or
# http://opensource.org/licenses/MIT.

"""
The patchew event framework
"""

_handlers = {}

_events = {}

def register_handler(event, handler):
    """Register an event hander. It will be called when the event is emitted."""
    _handlers.setdefault(event, [])
    _handlers[event].append(handler)

def declare_event(event, **params):
    """Declare an event that the caller will emit later, with kwarg names as
    the event argument names, and values as the descriptions."""
    assert event not in _events
    _events[event] = params
    emit_event("NewEvent", name=event, params=params)

def emit_event(event, **params):
    """Emit an event that was previously declared, and call all the registered
    handlers."""
    assert event in _events
    for keyword in params:
        assert keyword in _events[event]
    for handler in _handlers.get(event, []):
        try:
            handler(event, **params)
        except Exception as e:
            import traceback
            traceback.print_exc(e)

def get_events_info():
    return _events.copy()

declare_event("NewEvent",
              name="The name of the newly declared event",
              params="The params dict")
