from django.test import TestCase
from django.urls import reverse_lazy


class DashTest(TestCase):
    def test_public_access(self):
        response = self.client.get(reverse_lazy('posts'))
        self.assertTemplateUsed(response, 'dashboard.html')

    # def test_public_nav_bar(self):
    #     response = self.client.get(reverse_lazy('posts'))
    #     response.body.