from six import with_metaclass

import inspect

from datetime import datetime, timedelta
from itertools import chain


class TestMixinMeta(type):

    def __new__(cls, name, bases, attrs):
        # loop over base classes to get the tests and users array
        tests = []
        users = []

        for base in bases:
            # loop over members of the base classes:
            for member_name, member in inspect.getmembers(base):

                # get the functions starting with _test_
                if member_name.startswith('_test_'):
                    tests.append(member_name)

                # get the users
                if member_name.startswith('users'):
                    users += member

        # get tests from this class
        for attr in attrs:
            # get the functions starting with _test_
            if attr.startswith('_test_'):
                tests.append(attr)


        # get the users from this class
        if 'users' in attrs:
            users += attrs['users']

        for test in tests:
            for username, password in users:
                attrs[cls.get_function_name(test, username)] = \
                    cls.generate_test(test, username, password)

        return super(TestMixinMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def get_function_name(cls, test, username):
        return 'test_%s_for_%s' % (test[6:], username)

    @classmethod
    def generate_test(cls, test, username, password):
        def fn(self):
            if password:
                self.client.login(username=username, password=password)

            getattr(self, test)(username)
        
        fn.__test__ = 'declared by test_generator' # for nose/selector.py wantedMethod
        fn.__name__ = cls.get_function_name(test, username)
        
        return fn

class TestMixin(with_metaclass(TestMixinMeta, object)):

    # append explicit failure message to the end of the normal failure message
    longMessage = True


class TestSingleObjectMixin(TestMixin):

    def model_to_dict(self, instance):
        # the folowing is taken from the 1.9 version of django.forms.models.model_to_dict
        from django.db.models.fields.related import ManyToManyField
        meta = instance._meta
        data = {}

        # get the fields from the model
        fields = chain(meta.concrete_fields, meta.private_fields, meta.many_to_many)

        for field in fields:
            if not getattr(field, 'editable', False):
                continue

            if isinstance(field, ManyToManyField):
                data[field.name] = [value.pk for value in field.value_from_object(instance)]

            elif field.__class__.__name__ == 'JSONField':
                data[field.name] = getattr(instance, field.name)

            else:
                data[field.name] = field.value_from_object(instance)

        return data

    def get_instance_as_dict(self, instance=None):
        if instance is None:
            instance = self.instance

        model_data = {}
        for key, value in self.model_to_dict(instance).items():
            if not key.startswith('_') and value is not None:
                if isinstance(value, datetime):
                    model_data[key] = value.isoformat()
                elif isinstance(value, timedelta):
                    model_data[key] = str(value)
                else:
                    model_data[key] = value

        return model_data


class TestModelStringMixin(TestSingleObjectMixin):

    def test_model_str(self):
        for instance in self.instances:
            self.assertIsNotNone(instance.__str__())
