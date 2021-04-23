from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse


from .models import post

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='secret'

        )
        self.Post= post.objects.create(
            title='A good title',
            body= 'Nice body',
            author=self.user
        )

    def test_string_representation(self):
        Post= post(title='A simple title')
        self.assertEqual(str(Post), Post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.Post.title}', 'A good title')
        self.assertEqual(f'{self.Post.author}', 'testuser')
        self.assertEqual(f'{self.Post.body}', 'Nice body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detail_views(self):
        response= self.client.get('/post/1/')
        no_response= self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')