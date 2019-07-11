from django.conf.urls import url

from . import views

app_name = 'newspaper'

urlpatterns = [
    ## main page
    url( r'^$' , views.index , name = 'index' ),
    ## login page
    url( r'^login/$' , views.login , name = 'login' ) ,
    ## login page
    url( r'^logout/$' , views.logout , name = 'logout' ) ,
    ## create page
    url( r'^createUser/$' , views.createUser , name = 'createUser' ) ,
    # detailed article page
    url(r'^(?P<articleID>[0-9]+)/$' , views.detail , name = 'detail' ) ,
    ## get likes for an article
    url( r'^getLikes/([0-9]+)/$' , views.getLikes , name = 'getLikes' ) ,
    ## post a comment
    url( r'^postComment/$' , views.postComment , name = 'postComment' ) ,
    ## like an article
    url( r'^likeArticle/$' , views.likeArticle , name = 'LikeArticle' ) ,
    ## sports page redirect
    url( r'^sportRedirect/$' , views.sportRedirect , name = 'sportRedirect' ) ,
    ## update details
    url( r'^updateDetails/$' , views.updateDetails , name = 'updateDetails' ) ,
    ## login page redirect
    url( r'^loginRedirect/$' , views.loginRedirect , name = 'loginRedirect' ) ,
    ## dislike an article
    url( r'^dislikeArticle/$' , views.dislikeArticle , name = 'dislikeArticle' ) ,
    ## get comments
    url( r'^getComments/([0-9]+)/$' , views.getComments , name = 'getComments' ) ,
    ## get username
    url( r'^getUsername/([0-9]+)/$' , views.getUsername , name = 'getUsername' ) ,
    ## updateRedirect
    url( r'^updateRedirect/$' , views.updateRedirect , name = 'updateRedirect' ) ,
    ## logout redirect
    url( r'^logoutRedirect/$' , views.logoutRedirect , name = 'logoutRedirect' ) ,
    ## delete a comment
    url( r'^deleteComment/([0-9]+)/$' , views.deleteComment , name = 'deleteComment' ) ,
    ## politics page redirect
    url( r'^politicsRedirect/$' , views.politicsRedirect , name = 'politicsRedirect' ) ,
    ## register page redirect
    url( r'^registerRedirect/$' , views.registerRedirect , name = 'registerRedirect' ) ,
    ## lifestyle page redirect
    url( r'^lifestyleRedirect/$' , views.lifestyleRedirect , name = 'lifestyleRedirect' ) ,
    ## Ajax: check if user exists on registration page
    url(r'^checkIfUniqueLogin/$' , views.checkIfUniqueLogin , name = 'checkIfUniqueLogin' ) ,
    ## tech. page redirect
    url( r'^technologyRedirect/$' , views.technologyRedirect , name = 'technologyRedirect' ) ,
    ## return username of whoever is logged in
    url( r'^getLoggedINUsername/$' , views.getLoggedINUsername , name = 'getLoggedINUsername' ) ,
    ## business + finance page redirect
    url( r'^businessfinanceRedirect/$' , views.businessfinanceRedirect , name = 'businessfinanceRedirect' ) ,
    ## Ajax: check if user's email is registered
    url(r'^checkIfEmailIsRegistered/$' , views.checkIfEmailIsRegistered , name = 'checkIfEmailIsRegistered' ) ,

]
