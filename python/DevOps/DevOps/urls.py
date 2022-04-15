"""DevOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin



import autodeploy.views
import autodeploy.InitInput
import autodeploy.HtmlRespose
import autodeploy._Rollback
import autodeploy._AMIManagement
import autodeploy.__DeleteSnapshot__
import autodeploy._DeployResult
import autodeploy.GetUserProfile
import awsresource.SelectDB
import awsresource.DeleteDB
import awsresource.SelectSnapshot
import awsresource.CreateDB
import MemcacheOps.index
import MemcacheOps.CheckResult
import EC2Control.GetEC2Info
import EC2Control.NatConnect
import EC2Control.ModifyTime
import EC2Control.DeleteSelfEC2


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
  #  url(r'^autodeploy/test', auto_test.index),
    url(r'^autodeploy/index/$', autodeploy.views.index),
    url(r'^autodeploy/deploy/$', autodeploy.views.autodeploy),
    url(r'^autodeploy/deploylog/$', autodeploy.views.deploylog),
    url(r'^autodeploy/login/$', autodeploy.views.login),
    url(r'^autodeploy/logout/$', autodeploy.views.logout),
    url(r'^autodeploy/__init__/$',autodeploy.InitInput.index),
    url(r'^autodeploy/HtmlResponse/$',autodeploy.HtmlRespose.index),
    url(r'^autodeploy/rollback/$', autodeploy._Rollback.index),
    url(r'^autodeploy/rollbackOpt/$', autodeploy._Rollback.OptRollback),
    url(r'^autodeploy/amimanagement/$', autodeploy._AMIManagement.index),
    url(r'^autodeploy/amidelete/$', autodeploy.__DeleteSnapshot__.DeleteAMI),
    url(r'^autodeploy/deployresult/$', autodeploy._DeployResult.GetResults),
    url(r'^autodeploy/userprofile/$', autodeploy.GetUserProfile.GetInfo),
    url(r'^autodeploy/modifyuser/$', autodeploy.GetUserProfile.ModifyUser),
    url(r'^src/getdb/$', awsresource.SelectDB.GetUserInfo),
    url(r'^src/deletedb/$', awsresource.DeleteDB.DeleteDB),
    url(r'^src/selectsnap/$', awsresource.SelectSnapshot.GetDBs),
    url(r'^src/createdb/$', awsresource.CreateDB.CreateDB),
    url(r'^memcache/index/$', MemcacheOps.index.Index),
    url(r'^memcache/optindex/$', MemcacheOps.index.OptIndex),
    url(r'^memcache/delete/$', MemcacheOps.index.Delete),
    url(r'^memcache/getresult/$', MemcacheOps.CheckResult.Start),
    url(r'^ec2control/getinfo/$', EC2Control.GetEC2Info.GetEC2Info),
    url(r'^ec2control/natIndex/$', EC2Control.NatConnect.Index),
    url(r'^ec2control/natStart/$', EC2Control.NatConnect.StartEC2),
    url(r'^ec2control/modifytime/$', EC2Control.ModifyTime.Modify),
    url(r'^ec2control/deleteEC2/$', EC2Control.DeleteSelfEC2.DeleteEC2),
]
