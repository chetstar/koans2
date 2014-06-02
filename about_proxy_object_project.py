#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Create a Proxy Class
#
# In this assignment, create a proxy class (one is started for you
# below).  You should be able to initialize the proxy object with any
# object.  Any attributes called on the proxy object should be forwarded
# to the target object.  As each attribute call is sent, the proxy should
# record the name of the attribute sent.
#
# The proxy class is started for you.  You will need to add a method
# missing handler and any other supporting methods.  The specification
# of the Proxy class is given in the AboutProxyObjectProject koan.

# Note: This is a bit trickier than its Ruby Koans counterpart, but you
# can do it!

from runner.koan import *

class Proxy(object):
    __slots__ = ["_obj", "__weakref__"]
    def __init__(self, obj):
        object.__setattr__(self, "_obj", obj)
    
    #
    # proxying (special cases)
    #
    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "_obj"), name)
    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)
    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_obj"), name, value)
    
    def __nonzero__(self):
        return bool(object.__getattribute__(self, "_obj"))
    def __str__(self):
        return str(object.__getattribute__(self, "_obj"))
    def __repr__(self):
        return repr(object.__getattribute__(self, "_obj"))
    
    #
    # factories
    #
    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__', 
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__', 
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', 
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__', 
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', 
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', 
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', 
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__', 
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__', 
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__', 
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', 
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__', 
        '__truediv__', '__xor__', 'next',
    ]
    
    @classmethod
    def _create_class_proxy(cls, theclass):
        """creates a proxy for the given class"""
        
        def make_method(name):
            def method(self, *args, **kw):
                return getattr(object.__getattribute__(self, "_obj"), name)(*args, **kw)
            return method
        
        namespace = {}
        for name in cls._special_names:
            if hasattr(theclass, name):
                namespace[name] = make_method(name)
        return type("%s(%s)" % (cls.__name__, theclass.__name__), (cls,), namespace)
    
    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an 
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(obj.__class__)
        ins = object.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins
class AboutProxyObjectProject(Koan):
    def test_proxy_method_returns_wrapped_object(self):
        # NOTE: The Television class is defined below
        tv = Proxy(Television())

        self.assertTrue(isinstance(tv, Proxy))

    def test_tv_methods_still_perform_their_function(self):
        tv = Proxy(Television())

        tv.channel = 10
        tv.power()

        self.assertEqual(10, tv.channel)
        self.assertTrue(tv.is_on())

    def test_proxy_records_messages_sent_to_tv(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 10

        self.assertEqual(['power', 'channel'], tv.messages())

    def test_proxy_handles_invalid_messages(self):
        tv = Proxy(Television())

        ex = None
        try:
            tv.no_such_method()
        except AttributeError as ex:
            pass

        self.assertEqual(AttributeError, type(ex))

    def test_proxy_reports_methods_have_been_called(self):
        tv = Proxy(Television())

        tv.power()
        tv.power()

        self.assertTrue(tv.was_called('power'))
        self.assertFalse(tv.was_called('channel'))

    def test_proxy_counts_method_calls(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 48
        tv.power()

        self.assertEqual(2, tv.number_of_times_called('power'))
        self.assertEqual(1, tv.number_of_times_called('channel'))
        self.assertEqual(0, tv.number_of_times_called('is_on'))

    def test_proxy_can_record_more_than_just_tv_objects(self):
        proxy = Proxy("Py Ohio 2010")

        result = proxy.upper()

        self.assertEqual("PY OHIO 2010", result)

        result = proxy.split()

        self.assertEqual(["Py", "Ohio", "2010"], result)
        self.assertEqual(['upper', 'split'], proxy.messages())


# ====================================================================
# The following code is to support the testing of the Proxy class.  No
# changes should be necessary to anything below this comment.

# Example class using in the proxy testing above.
class Television(object):
    def __init__(self):
        self._channel = None
        self._power = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def power(self):
        if self._power == 'on':
            self._power = 'off'
        else:
            self._power = 'on'

    def is_on(self):
        return self._power == 'on'


# Tests for the Television class.  All of theses tests should pass.
class TelevisionTest(Koan):
    def test_it_turns_on(self):
        tv = Television()

        tv.power()
        self.assertTrue(tv.is_on())

    def test_it_also_turns_off(self):
        tv = Television()

        tv.power()
        tv.power()

        self.assertFalse(tv.is_on())

    def test_edge_case_on_off(self):
        tv = Television()

        tv.power()
        tv.power()
        tv.power()

        self.assertTrue(tv.is_on())

        tv.power()

        self.assertFalse(tv.is_on())

    def test_can_set_the_channel(self):
        tv = Television()

        tv.channel = 11
        self.assertEqual(11, tv.channel)
