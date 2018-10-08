"""
events.py
these are simple event classes for 
stickman's new world.
there are 2 ways to use these.
in main_event_queue or _internal_event_queue.
in _internal_event_queue it will act in the 
thread with that sprite, and in main_event_queue,
it will act in the main loop itself.
"""


class _Event:
    """
    base class for the other events.
    """

    def __init__(self, code=None, mode=exec):
        self.code = code

    def __call__(self):
        self._exec()

    def __repr__(self):
        return '%a object at %s' % (self.__class__, hex(id(self)))

    def _exec(self):
        """
        to be overridden.
        """
        if self.code is not None:
            self.mode(self.code)


class Quit(_Event):
    def __init__(self):
        Quit.code = compile('import os; os._exit(0)', 'Quit Event', 'exec')
        self.mode = exec


class Pause(_Event):
    keep = True


class SayHello(_Event):
    """
    test event.
    """

    def __init__(self):
        SayHello.code = compile('print("Hello!")', 'SayHello event', 'exec')
        self.mode = exec

    def _exec(self):
        self.mode(self.code)


# print(SayHello())
