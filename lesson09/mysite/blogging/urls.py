from django.urls import path
from blogging.views import list_view, detail_view, add_model
# from blogging.feeds import LatestEntriesFeed
from django.conf.urls import url


urlpatterns = [
    path('', list_view, name="blog_index"),
    path('posts/<int:post_id>/', detail_view, name= "blog_detail"),
    path('create/post', add_model, name='create_post')
    # path('latest/feed/', LatestEntriesFeed()),
]