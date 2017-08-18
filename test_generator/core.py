from six import with_metaclass

import inspect

from datetime import datetime, timedelta
from itertools import chain

from django.utils import translation


class TestMixinMeta(type):

    def __new__(cls, name, bases, attrs):
        # loop over base classes to get the tests and users array
        tests = []
        languages = []
        users = []
        for base in bases:
            # loop over members of the base class:
            for member_name, member in inspect.getmembers(base):

                # get the functions starting with _test_
                if member_name.startswith('_test_'):
                    tests.append(member_name)

                # get the languages
                if member_name.startswith('languages'):
                    languages += member

                # get the users
                if member_name.startswith('users'):
                    users += member

        for test in tests:
            for language in languages:
                for username, password in users:
                    attrs[test[1:] + '_' + language + '_' + username] = \
                        cls.generate_test(test, language, username, password)

        return super(TestMixinMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def generate_test(cls, test, language, username, password):
        def fn(self):
            translation.activate(language)

            if password:
                self.client.login(username=username, password=password)

            getattr(self, test)(username)

        return fn


class TestMixin(with_metaclass(TestMixinMeta, object)):

    # append explicit failure message to the end of the normal failure message
    longMessage = True


class TestSingleObjectMixin(TestMixin):

    def model_to_dict(self, instance):
        # the folowing is taken from the 1.9 version of django.forms.models.model_to_dict
        from django.db.models.fields.related import ManyToManyField
        opts = instance._meta
        data = {}
        for field in chain(opts.concrete_fields, opts.virtual_fields, opts.many_to_many):
            if not getattr(field, 'editable', False):
                continue

            if isinstance(field, ManyToManyField):
                # If the object doesn't have a primary key yet, just use an empty
                # list for its m2m fields. Calling f.value_from_object will raise
                # an exception.
                if instance.pk is None:
                    data[field.name] = []
                else:
                    # MultipleChoiceWidget needs a list of pks, not object instances.
                    qs = field.value_from_object(instance)
                    if qs._result_cache is not None:
                        data[field.name] = [item.pk for item in qs]
                    else:
                        data[field.name] = list(qs.values_list('pk', flat=True))

            elif field.__class__.__name__ == 'JSONField':
                data[field.name] = getattr(instance, field.name)

            else:
                data[field.name] = field.value_from_object(instance)

        return data

    def get_instance_as_dict(self, instance=None):
        if instance is None:
            instance = self.instance

        model_dict = self.model_to_dict(instance)

        model_data = {}
        for key in model_dict:
            model_value = model_dict[key]

            if model_value is not None:
                if isinstance(model_value, datetime):
                    model_data[key] = model_value.isoformat()
                elif isinstance(model_value, timedelta):
                    model_data[key] = str(model_value)
                else:
                    model_data[key] = model_value

        return model_data


class TestModelStringMixin(TestSingleObjectMixin):

    def test_model_str(self):
        for instance in self.instances:
            self.assertIsNotNone(instance.__str__())
