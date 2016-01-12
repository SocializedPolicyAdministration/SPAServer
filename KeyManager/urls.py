"""KeyManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from AddKeys.views import add_keys
from CommunicationServer.views import get_spa_request
from PollServer.views import polling_key_manager
from MergeServer.views import get_merge_response

urlpatterns = [
    url(r'^addKeys', add_keys),
    url(r'pollingKeyManager', polling_key_manager),
    url(r'getSPARequest', get_spa_request),
    url(r'getSPAResponse', get_merge_response)
]
