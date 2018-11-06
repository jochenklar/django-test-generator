import json

from collections import OrderedDict

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.utils.http import urlencode

from .core import TestMixin, TestSingleObjectMixin


class TestViewsetMixin(TestMixin):

    def assert_viewset(self, key, method, route, username, kwargs={}, query_params={}, data={}):

        url_name = self.url_names['viewset'] + '-' + route
        status_map = self.status_map[key]

        url = reverse(url_name, kwargs=kwargs)

        if method == 'get':
            response = self.client.get(url, query_params)
        else:
            if query_params:
                url += '?' + urlencode(query_params)

            if method == 'post':
                response = self.client.post(url, data)
            elif method == 'put':
                response = self.client.put(url, json.dumps(data), content_type='application/json')
            elif method == 'delete':
                response = self.client.delete(url)
            else:
                raise RuntimeError('method \'%s\' not supported' % method)

        content_type = response.get('Content-Type')

        if content_type == 'text/html':
            content = response.content
        elif content_type == 'application/json':
            content = response.json()
        elif content_type == 'application/zip':
            content = '<zip>'
        else:
            content = None

        msg = OrderedDict((
            ('username', username),
            ('url', url),
            ('method', method),
            ('data', data),
            ('status_code', response.status_code),
            ('content_type', content_type),
            ('content', content)
        ))

        self.assertEqual(response.status_code, status_map[username], msg=msg)
        return msg

    def assert_list_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('list_viewset', 'get', 'list', username, kwargs=kwargs, query_params=query_params)

    def assert_detail_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('detail_viewset', 'get', 'detail', username, kwargs=kwargs, query_params=query_params)

    def assert_create_viewset(self, username, kwargs={}, query_params={}, data={}):
        return self.assert_viewset('create_viewset', 'post', 'list', username, kwargs=kwargs, query_params=query_params, data=data)

    def assert_update_viewset(self, username, kwargs={}, query_params={}, data={}):
        return self.assert_viewset('update_viewset', 'put', 'detail', username, kwargs=kwargs, query_params=query_params, data=data)

    def assert_delete_viewset(self, username, kwargs={}, query_params={}):
        return self.assert_viewset('delete_viewset', 'delete', 'detail', username, kwargs=kwargs, query_params=query_params)


class TestListViewsetMixin(TestViewsetMixin):

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username)


class TestCreateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(username, data=self.get_instance_as_dict(instance))


class TestDetailViewsetMixin(TestViewsetMixin):

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, kwargs={'pk': instance.pk})


class TestUpdateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_update_viewset(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_update_viewset(username, kwargs={'pk': instance.pk}, data=data)


class TestDeleteViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, kwargs={'pk': instance.pk})
            instance.save(update_fields=None)


class TestReadOnlyModelViewsetMixin(TestListViewsetMixin,
                                    TestDetailViewsetMixin):
    pass


class TestModelViewsetMixin(TestListViewsetMixin,
                            TestDetailViewsetMixin,
                            TestCreateViewsetMixin,
                            TestUpdateViewsetMixin,
                            TestDeleteViewsetMixin):
    pass
