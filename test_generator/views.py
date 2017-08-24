from django.core.urlresolvers import reverse

from .core import TestMixin, TestSingleObjectMixin


class TestViewMixin(TestMixin):

    def assert_list_view(self, username, url_kwargs={}):

        url = reverse(self.url_names['list_view'], kwargs=url_kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['list_view'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_detail_view(self, username, id, url_kwargs={}):

        url_kwargs.update({'id': id})
        url = reverse(self.url_names['retrieve_view'], kwargs=url_kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['retrieve_view'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_create_view_get(self, username, url_kwargs={}):

        url = reverse(self.url_names['create_view'], kwargs=url_kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['create_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_create_view_post(self, username, data, url_kwargs={}):

        url = reverse(self.url_names['create_view'], kwargs=url_kwargs)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, self.status_map['create_view_post'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_update_view_get(self, username, id, url_kwargs={}):

        url_kwargs.update({'id': id})
        url = reverse(self.url_names['update_view'], kwargs=url_kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['update_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_update_view_post(self, username, id, data, url_kwargs={}):

        url_kwargs.update({'id': id})
        url = reverse(self.url_names['update_view'], kwargs=url_kwargs)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, self.status_map['update_view_post'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_delete_view_get(self, username, id, url_kwargs={}):

        url_kwargs.update({'id': id})
        url = reverse(self.url_names['delete_view'], kwargs=url_kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['delete_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))


    def assert_delete_view_post(self, username, id, url_kwargs={}):

        url_kwargs.update({'id': id})
        url = reverse(self.url_names['delete_view'], kwargs=url_kwargs)
        response = self.client.post(url)

        self.assertEqual(response.status_code, self.status_map['delete_view_post'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))


class TestListViewMixin(TestViewMixin):

    def _test_list_view(self, username):
        self.assert_list_view(username)


class TestRetrieveViewMixin(TestViewMixin):

    def _test_retrieve_view(self, username):
        for instance in self.instances:
            self.assert_detail_view(username, instance.pk)


class TestCreateViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_create_view_get(self, username):
        self.assert_create_view_get(username)

    def _test_create_view_post(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_create_view_get(username, data)


class TestUpdateViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_update_view_get(self, username):
        for instance in self.instances:
            self.assert_update_view_get(username, instance.pk)

    def _test_update_view_post(self, username):
        for instance in self.instances:
            data = self.get_instance_as_dict(instance)
            self.assert_update_view_post(username, instance.pk, data)


class TestDeleteViewMixin(TestSingleObjectMixin, TestViewMixin):

    def _test_delete_view_get(self, username):
        for instance in self.instances:
            self.assert_delete_view_get(username, instance.pk)


    def _test_delete_view_post(self, username):
        for instance in self.instances:
            self.assert_delete_view_post(username, instance.pk)


class TestModelViewMixin(TestListViewMixin,
                         TestRetrieveViewMixin,
                         TestCreateViewMixin,
                         TestUpdateViewMixin,
                         TestDeleteViewMixin):
    pass
