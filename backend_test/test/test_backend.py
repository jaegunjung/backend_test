import json
from rest_framework.test import APITestCase


class TestApplication(APITestCase):

    def test_names_delete(self):
        """
        Test Deleting all names
        """
        url = "/names"
        response = self.client.delete(url, follow=True)
        self.assertTrue(response.status_code == 204)

    def test_names_put_get(self):
        """
        Test Putting name and url and get the data
        """
        data = {"url": "http://alex.com"}
        url = "/names/alex"
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json; charset=utf-8', follow=True)
        self.assertTrue(response.status_code == 201)
        response2 = self.client.get(url, follow=True)
        response2_data = json.loads(response2.content)
        self.assertTrue(response2_data['url'] == "http://alex.com")
        self.assertTrue(response2_data['name'] == 'alex')

    def test_annotate(self):
        data = {"url": "http://alex.com"}
        url = "/names/alex"
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json; charset=utf-8', follow=True)
        self.assertTrue(response.status_code == 201)
        url = "/annotate"
        data = "my name is alex"
        response2 = self.client.post(url, data=data,
                                         content_type='text/plain; charset=utf-8', follow=True)
        self.assertTrue(response2.status_code == 200)
        self.assertTrue(response2.content == 'my name is <a href="http://alex.com">alex</a>')
