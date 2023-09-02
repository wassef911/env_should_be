from __future__ import annotations


class ValueUnassignableToDescription(Exception):
    'Raised when a description field has unacceptable value'
    # example
    # length: 5.2
    pass


class DescriptionFileNotLoading(Exception):
    pass


class FileHasNoExtension(Exception):
    pass


class EnvironmentFileNotLoading(Exception):
    pass


class RequiredVariableNotSet(Exception):
    pass


class CallBackNotRunning(Exception):
    pass
