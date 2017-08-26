from django.core.urlresolvers import reverse

from .core import TestMixin, TestSingleObjectMixin


class TestViewMixin(TestMixin):

    def assert_list_view(self, username, kwargs={}):

        url = reverse(self.url_names['list_view'], kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['list_view'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_detail_view(self, username, kwargs={}):

        url = reverse(self.url_names['detail_view'], kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['detail_view'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_create_view_get(self, username, kwargs={}):

        url = reverse(self.url_names['create_view'], kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['create_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_create_view_post(self, username, kwargs={}, data={}):

        url = reverse(self.url_names['create_view'], kwargs=kwargs)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, self.status_map['create_view_post'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_update_view_get(self, username, kwargs={}):

        url = reverse(self.url_names['update_view'], kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['update_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_update_view_post(self, username, kwargs={}, data={}):

        url = reverse(self.url_names['update_view'], kwargs=kwargs)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, self.status_map['update_view_post'][username], msg=(
            ('username', username),
            ('url', url),
            ('data', data),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def assert_delete_view_get(self, username, kwargs={}):

        url = reverse(self.url_names['delete_view'], kwargs=kwargs)
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['delete_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))


    def assert_delete_view_post(self, username, kwargs={}):

        url = reverse(self.url_names['delete_view'], kwargs=kwargs)
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
