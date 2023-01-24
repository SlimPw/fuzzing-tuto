import sys

class Coverage(object):

    def __init__(self):
        self._trace = []

    def trace(self):
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def coverage(self):
        """The set of executed lines, as (function_name, line_number) pairs"""
        return set(self.trace())

    # Trace function
    def traceit(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            self._trace.append((function_name, lineno))

        return self.traceit

    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)




