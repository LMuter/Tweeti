from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'tweets', views.TweetViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('tweet_data', views.get_tweet_data, name='get_tweet_data'),
    path('update_labels', views.update_labels, name='update_labels'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload', views.upload_tweets, name='upload_tweets'),
    path('download', views.download_tweets, name='download_tweets'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('exclude_tweet', views.exclude_tweet, name='exclude_tweet'),
    path('discuss_tweet', views.discuss_tweet, name='discuss_tweet'),
    # path('manual_remove_labels', views.manual_remove_labels, name='manual_remove_labels'),
    path('errornotifier', csrf_exempt(views.errornotifier), name="errornotifier"),
    path('send_test_email', views.send_test_email, name="send_test_email"),
]
