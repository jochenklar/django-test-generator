from django.core.urlresolvers import reverse

from .core import TestMixin, TestSingleObjectMixin


class TestListViewMixin(TestMixin):

    def _test_list_view(self, username):

        url = reverse(self.url_names['list_view'], args=self.get_list_url_args())
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['list_view'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def get_list_url_args(self):
        return []


class TestRetrieveViewMixin(TestMixin):

    def _test_retrieve_view(self, username):

        for instance in self.instances:
            url = reverse(self.url_names['retrieve_view'], args=self.get_retrieve_url_args(instance))
            response = self.client.get(url)

            self.assertEqual(response.status_code, self.status_map['retrieve_view'][username], msg=(
                ('username', username),
                ('url', url),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

    def get_retrieve_url_args(self, instance):
        return [instance.pk]


class TestCreateViewMixin(TestSingleObjectMixin):

    def _test_create_view_get(self, username):

        url = reverse(self.url_names['create_view'], args=self.get_create_url_args())
        response = self.client.get(url)

        self.assertEqual(response.status_code, self.status_map['create_view_get'][username], msg=(
            ('username', username),
            ('url', url),
            ('status_code', response.status_code),
            ('content', response.content)
        ))

    def _test_create_view_post(self, username):

        for instance in self.instances:
            instance = self.prepare_create_instance(instance)

            url = reverse(self.url_names['create_view'], args=self.get_create_url_args())
            data = self.get_instance_as_dict(instance)
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, self.status_map['create_view_post'][username], msg=(
                ('username', username),
                ('url', url),
                ('data', data),
                ('status_code', response.status_code),
                ('content', response.content)
            ))


    def get_create_url_args(self):
        return []

    def prepare_create_instance(self, instance):
        return instance


class TestUpdateViewMixin(TestSingleObjectMixin):

    def _test_update_view_get(self, username):

        for instance in self.instances:
            instance = self.prepare_update_instance(instance)

            url = reverse(self.url_names['update_view'], args=self.get_update_url_args(instance))
            response = self.client.get(url)

            self.assertEqual(response.status_code, self.status_map['update_view_get'][username], msg=(
                ('username', username),
                ('url', url),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

    def _test_update_view_post(self, username):

        for instance in self.instances:
            instance = self.prepare_update_instance(instance)

            url = reverse(self.url_names['update_view'], args=self.get_update_url_args(instance))
            data = self.get_instance_as_dict(instance)
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, self.status_map['update_view_post'][username], msg=(
                ('username', username),
                ('url', url),
                ('data', data),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

    def get_update_url_args(self, instance):
        return [instance.pk]

    def prepare_update_instance(self, instance):
        return instance


class TestDeleteViewMixin(TestSingleObjectMixin):

    restore_instance = True

    def _test_delete_view_get(self, username):

        for instance in self.instances:
            instance = self.prepare_update_instance(instance)

            url = reverse(self.url_names['delete_view'], args=self.get_delete_url_args(instance))
            response = self.client.get(url)

            self.assertEqual(response.status_code, self.status_map['delete_view_get'][username], msg=(
                ('username', username),
                ('url', url),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

    def _test_delete_view_post(self, username):

        for instance in self.instances:
            instance = self.prepare_delete_instance(instance)

            url = reverse(self.url_names['delete_view'], args=self.get_delete_url_args(instance))
            response = self.client.post(url)

            self.assertEqual(response.status_code, self.status_map['delete_view_post'][username], msg=(
                ('username', username),
                ('url', url),
                ('status_code', response.status_code),
                ('content', response.content)
            ))

            if self.restore_instance:
                # save the instance again so we can delete it again later
                instance.save()

    def get_delete_url_args(self, instance):
        return [instance.pk]

    def prepare_delete_instance(self, instance):
        return instance


class TestModelViewMixin(TestListViewMixin,
                         TestRetrieveViewMixin,
                         TestCreateViewMixin,
                         TestUpdateViewMixin,
                         TestDeleteViewMixin):
    pass
