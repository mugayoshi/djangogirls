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
        
        
def create_post(post_title, post_text, days):
    """
        create a post with the given 'post_text' and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published)
        
        :return:
    """
    time = timezone.now() + datetime.timedelta(days=days)
    user = create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return Post.objects.create(author=user, title=post_title, text=post_text, published_date=time)


def create_user(user_name, mail_addr, user_password):
    return User.objects.create_user(user_name, mail_addr, user_password)


class PostIndexViewTests(TestCase):
    def test_no_post(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_past_post(self):
        create_post(post_title="past post", post_text="post post text", days=-30)
        response = self.client.get(reverse('post_list'))
        print(response.context['posts'])
        
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: past post>']
        )
        

   

