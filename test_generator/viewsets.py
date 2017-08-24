import json

from django.core.urlresolvers import reverse

from django.utils.http import urlencode

from .core import TestMixin, TestSingleObjectMixin


class TestViewsetMixin(TestMixin):

    def assert_list_viewset(self, username, list_route='list', query_params={}):

        url = reverse(self.url_names['viewset'] + '-' + list_route)
        response = self.client.get(url, query_params)

        self.assertEqual(response.status_code, self.status_map[list_route + '_viewset'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_detail_viewset(self, username, pk, detail_route='detail', query_params={}):

        url = reverse(self.url_names['viewset'] + '-' + detail_route, args=[pk])
        response = self.client.get(url, query_params)

        self.assertEqual(response.status_code, self.status_map[detail_route + '_viewset'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_create_viewset(self, username, data, query_params={}):

        url = reverse(self.url_names['viewset'] + '-list')

        if query_params:
            url += '?' + urlencode(query_params)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, self.status_map['create_viewset'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_update_viewset(self, username, pk, data, query_params={}):

        url = reverse(self.url_names['viewset'] + '-detail', args=[pk])

        if query_params:
            url += '?' + urlencode(query_params)

        response = self.client.put(url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, self.status_map['update_viewset'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_delete_viewset(self, username, pk, query_params={}):
        url = reverse(self.url_names['viewset'] + '-detail', args=[pk])

        if query_params:
            url += '?' + urlencode(query_params)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, self.status_map['delete_viewset'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))


class TestListViewsetMixin(TestViewsetMixin):

    def _test_list_viewset(self, username):
        self.assert_list_viewset(username)


class TestCreateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_create_viewset(self, username):
        for instance in self.instances:
            self.assert_create_viewset(username, self.get_instance_as_dict(instance))


class TestDetailViewsetMixin(TestViewsetMixin):

    def _test_detail_viewset(self, username):
        for instance in self.instances:
            self.assert_detail_viewset(username, instance.pk)


class TestUpdateViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_update_viewset(self, username):
        for instance in self.instances:
            self.assert_update_viewset(username, instance.pk, self.get_instance_as_dict(instance))


class TestDeleteViewsetMixin(TestSingleObjectMixin, TestViewsetMixin):

    def _test_delete_viewset(self, username):
        for instance in self.instances:
            self.assert_delete_viewset(username, instance.pk)
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
