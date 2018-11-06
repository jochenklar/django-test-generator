from collections import OrderedDict

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.utils.http import urlencode

from .core import TestMixin, TestSingleObjectMixin


class TestViewMixin(TestMixin):

    def assert_view(self, key, method, url_name, username, kwargs={}, query_params={}, data={}):

        url = reverse(self.url_names[url_name], kwargs=kwargs)

        if method == 'get':
            response = self.client.get(url, query_params)
        else:
            if query_params:
                url += '?' + urlencode(query_params)

            if method == 'post':
                response = self.client.post(url, data)
            elif method == 'put':
                response = self.client.put(url, data)
            elif method == 'delete':
                response = self.client.delete(url)
            else:
                raise RuntimeError('method \'%s\' not supported' % method)

        try:
            content = response.content
        except AttributeError:
            content = None

        msg = OrderedDict((
            ('username', username),
            ('url', url),
            ('method', method),
            ('data', data),
            ('status_code', response.status_code),
            ('content', content)
        ))

        self.assertEqual(response.status_code, self.status_map[key][username], msg=msg)
        return msg

    def assert_list_view(self, username, kwargs={}):
        return self.assert_view('list_view', 'get', 'list_view', username, kwargs=kwargs)

    def assert_detail_view(self, username, kwargs={}):
        return self.assert_view('detail_view', 'get', 'detail_view', username, kwargs=kwargs)

    def assert_create_view_get(self, username, kwargs={}):
        return self.assert_view('create_view_get', 'get', 'create_view', username, kwargs=kwargs)

    def assert_create_view_post(self, username, kwargs={}, data={}):
        return self.assert_view('create_view_post', 'post', 'create_view', username, kwargs=kwargs, data=data)

    def assert_update_view_get(self, username, kwargs={}):
        return self.assert_view('update_view_get', 'get', 'update_view', username, kwargs=kwargs)

    def assert_update_view_post(self, username, kwargs={}, data={}):
        return self.assert_view('update_view_post', 'post', 'update_view', username, kwargs=kwargs, data=data)

    def assert_delete_view_get(self, username, kwargs={}):
        return self.assert_view('delete_view_get', 'get', 'delete_view', username, kwargs=kwargs)

    def assert_delete_view_post(self, username, kwargs={}):
        return self.assert_view('delete_view_post', 'post', 'delete_view', username, kwargs=kwargs)


class TestListViewMixin(TestViewMixin):

    def _test_list_view(self, username):
        self.assert_list_view(username)


class TestDetailViewMixin(TestViewMixin):

    def _test_retrieve_view(self, username):
        for instance in self.instances:
            self.assert_detail_view(username, {
                'pk': instance.pk
            })


class TestCreateViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_create_view_get(self, username):
        self.assert_create_view_get(username)

    def _test_create_view_post(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_create_view_post(username, {}, data)


class TestUpdateViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_update_view_get(self, username):
        for instance in self.instances:
            self.assert_update_view_get(username, {
                'pk': instance.pk
            })

    def _test_update_view_post(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_update_view_post(username, {
                'pk': instance.pk
            }, data)


class TestDeleteViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_delete_view_get(self, username):
        for instance in self.instances:
            self.assert_delete_view_get(username, {
                'pk': instance.pk
            })

    def _test_delete_view_post(self, username):
        for instance in self.instances:
            self.assert_delete_view_post(username, {
                'pk': instance.pk
            })
            instance.save(update_fields=None)


class TestModelViewMixin(TestListViewMixin,
                         TestDetailViewMixin,
                         TestCreateViewMixin,
                         TestUpdateViewMixin,
                         TestDeleteViewMixin):
    pass
