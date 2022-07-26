import builtins
import sys

__all__ = ['TypedDict']

if sys.version_info < (3, 9):
    _original_list = list
    _original_dict = dict
    _original_set = set
    _original_tuple = tuple


    class list(list):
        __module__ = builtins

        def __class_getitem__(self, item):
            self.__args__ = item
            return list


    class dict(dict):
        __module__ = builtins
        FAKE = True

        def __class_getitem__(self, item):
            self.__args__ = item
            return dict


    class tuple(tuple):
        __module__ = builtins

        def __class_getitem__(self, item):
            self.__args__ = item
            return tuple


    class set(set):
        __module__ = builtins

        def __class_getitem__(self, item):
            self.__args__ = item
            return set


    builtins.list = list
    builtins.dict = dict
    builtins.tuple = tuple
    builtins.set = set

try:
    from typing import TypedDict
except Exception:
    class TypedDictMeta(type):
        def __repr__(self):
            if self is TypedDict:
                return f"<class 'TypedDict'>"
            else:
                return f"<TypedDict '{self.__name__}'>"


    class TypedDict(metaclass=TypedDictMeta):
        __module__ = builtins


    builtins.TypedDict = TypedDict


class RecordMeta(type):
    def __repr__(self):
        if self is TypedDict:
            return f"<class 'Record'>"
        else:
            return f"<Record '{self.__name__}'>"


class Record(metaclass=RecordMeta):
    __module__ = builtins


import sys
import traceback


class record(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        annotations = self._get_annotations()
        matched = set()
        for name, arg in zip(annotations, args):
            self[name] = arg
            matched.add(name)
        for key, value in kwargs.items():
            self[key] = value
            matched.add(key)
        missing = set(annotations) - matched
        if missing:
            raise ValueError(
                "There were not enough arguments to make the '{clss}'.\n Given {matched}.\n Missing: {missing}".format(
                    missing=", ".join(repr(m) for m in missing),
                    matched=", ".join(repr(m) for m in matched),
                    clss=type(self).__name__
                ))

    def __setitem__(self, key, value):
        annotations = type(self).__annotations__
        if key not in annotations:
            raise ValueError("Unknown field '{key}' for {clss} instance.".format(
                clss=type(self).__name__,
                key=key
            ))
        elif not isinstance(value, annotations[key]):
            t = annotations[key]
            raise TypeError(
                "Expected {clss} field '{name}' to be of type '{t}', received {value} instead ('{wrong}').".format(
                    clss=type(self).__name__,
                    name=key,
                    t=t.__name__,
                    wrong=type(value).__name__,
                    value=value
                ))
        else:
            dict.__setitem__(self, key, value)

    def _fix_traceback(self):
        # extracts = traceback.extract_tb(sys.exc_info()[2])
        # find the first occurrence of the module file name
        # extracts = extracts[:-2]
        traceback.format_exc(limit=-2)

    @classmethod
    def _get_annotations(cls):
        d = {}
        for c in cls.mro():
            try:
                d.update(**c.__annotations__)
            except AttributeError:
                # object, at least, has no __annotations__ attribute.
                pass
        return d

