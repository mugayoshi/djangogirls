import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Post, Comment

from django.urls import reverse
from django.contrib.auth.models import User


class PostModelTests(TestCase):
    
    def test_published_date_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(published_date=time)
        self.assertIs(future_post.published_date_is_in_past(), False)

    def test_published_date_with_past_date(self):
        time = timezone.now() + datetime.timedelta(days=-30)
        past_post = Post(published_date=time)
        self.assertIs(past_post.published_date_is_in_past(), True)

    def test_comment_create_date_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_comment = Comment(created_date=time)
        self.assertIs(future_comment.created_date_is_in_past(), False)
    
    def test_comment_create_date_with_past_date(self):
        time = timezone.now() + datetime.timedelta(days=-30)
        past_comment = Comment(created_date=time)
        self.assertIs(past_comment.created_date_is_in_past(), True)
        
        
def create_post(post_title, post_text, days, user):
    """
        create a post with the given 'post_text' and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published)
        
        :return:
    """
    
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(author=user, title=post_title, text=post_text, published_date=time)


def create_test_user(user_name='john'):
    mail_addr = user_name + '@mail.com'
    password = user_name + 'password'
    return User.objects.create_user(user_name, mail_addr, password)


class PostIndexViewTests(TestCase):
    def test_no_post(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        print('test_no_post: ')
        print(response.context['posts'])
        self.assertQuerysetEqual(response.context['posts'], [])
    
    def test_past_post(self):
        user = create_test_user('paul')
        create_post(post_title="past post", post_text="post post text", days=-30, user=user)
        response = self.client.get(reverse('post_list'))
        print(response.context['posts'])
        
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: past post>']
        )

    def test_future_post(self):
        user = create_test_user('george')
        create_post(post_title="future post", post_text="post future text", days=30, user=user)
        response = self.client.get(reverse('post_list'))
        print('test_future_post: ')
        print(response.context['posts'])
        self.assertQuerysetEqual(response.context['posts'], [])


class PostDetailViewTest(TestCase):
    def test_future_post(self):
        """
            The detail view of a post with a pub_date in the future
            returns a 404 not found.
        """
        user = create_test_user()
        future_post = create_post(post_title="future post", post_text="post future text", days=30, user=user)
        url = reverse('post_detail', args=(future_post.id,))
        response = self.client.get(url)
        print('test_future_post detail: ')
        # print(response.context)
        self.assertEqual(response.status_code, 404)
    
    def test_past_post(self):
        """
            The detail view of a post with a pub_date in the past
            displays the post's text
        """
        user = create_test_user('micheal')
        past_post = create_post(post_title='past post', post_text='past post text', days=-30, user=user)
        url = reverse('post_detail', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.text)

