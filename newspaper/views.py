from django.shortcuts import render , render_to_response , redirect , get_object_or_404
from django.http import HttpResponse , Http404 , JsonResponse
from .models import UserAccount, Article, Comment , Like
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.db import IntegrityError
from django.utils import timezone

## decorator that tests whether user is logged in
def checkIfLoggedIn( function ) :
    def test( request ) :
        ## check if the username is in cookie
        if ( 'username' in request.session ) :
            return function( request )
        else : ## raise permission error
            raise PermissionDenied( 'ILLEGAL ACTION' )
    return test

## this is index page
def index( request ) :
    ## get comments in reverse order
    commentsList = Comment.objects.order_by( '-publicationDate' )[  : 5 ]
    articleList  = getArticleList( commentsList )
    idList       = getIdList( commentsList )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = {

                     'commentsList' : commentsList,
                     'articleList'  : articleList,
                     'idList'       : idList

                  }
        return render( request , 'newspaper/index1.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name = getName( request.session['username'] )
        context = {

                     'fName'             :name,
                     'commentsList' : commentsList,
                     'articleList'  : articleList,
                     'idList'       : idList

                  }
        return render( request , 'newspaper/index2.html' , context )

## register redirect
def registerRedirect( request ) :
    return render( request , 'newspaper/register.html' , {} )

## login redirect
def loginRedirect( request ) :
    return render( request , 'newspaper/login.html' , {} )

## update redirect
def updateRedirect( request ) :
    return render( request , 'newspaper/updateDetails.html' , {} )

## logout redirect
def logoutRedirect( request ) :
    return render( request , 'newspaper/loggedOut.html' , {} )

## lifestyle redirect
def lifestyleRedirect( request ) :
    ## get all the articles of type LIFESTYLE
    article_list = Article.objects.filter( articleType  = 'lifestyle' )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = { 'article_list' : article_list }
        return render( request , 'newspaper/lifestyle.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        context      = {

                           'fName'        : name ,
                           'article_list' : article_list

                       }
        return render( request , 'newspaper/lifestyle2.html' , context )

## sports redirect
def sportRedirect( request ) :
    ## get all the articles of type SPORT
    article_list = Article.objects.filter( articleType  = 'sport' )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = { 'article_list' : article_list }
        return render( request , 'newspaper/sport.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        context      = {

                           'fName'        : name ,
                           'article_list' : article_list

                       }
        return render( request , 'newspaper/sport2.html' , context )

## politics redirect
def politicsRedirect( request ) :
    ## get all the articles of type POLITICS
    article_list = Article.objects.filter( articleType  = 'politics' )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = { 'article_list' : article_list }
        return render( request , 'newspaper/politics.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        context      = {

                           'fName'        : name ,
                           'article_list' : article_list

                       }
        return render( request , 'newspaper/politics2.html' , context )

## business + finance redirect
def businessfinanceRedirect( request ) :
    ## get all the articles of type BUSINESS + FINANCE
    article_list = Article.objects.filter( articleType  = 'businessfinance' )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = { 'article_list' : article_list }
        return render( request , 'newspaper/businessfinance.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        context      = {

                           'fName'        : name ,
                           'article_list' : article_list

                       }
        return render( request , 'newspaper/businessfinance2.html' , context )

## tech. redirect
def technologyRedirect( request ) :
    ## get all the articles of type TECHNOLOGY
    article_list = Article.objects.filter( articleType  = 'technology' )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = { 'article_list' : article_list }
        return render( request , 'newspaper/technology.html' , context )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        context      = {

                           'fName'        : name ,
                           'article_list' : article_list

                       }
        return render( request , 'newspaper/technology2.html' , context )

## login method
def login( request ) :
    ## check if request is of type POST
    if ( request.method == 'POST' ) :
        ## extract name + description + price from request
        Email    = request.POST[ 'email' ]
        Password = request.POST[ 'password' ]

        try: ## user may enter a non-registered username
            ## get user obj. in question
            user = UserAccount.objects.get( email = Email )

            ## check if password's match
            if ( user.password == Password ) : ## password's match

                ## set session cookie
                request.session['username'] = Email
                request.session['password'] = Password

                context = {

                              'success'    : True

                          }
                return JsonResponse( context )

            else :   ## return bad JSON
                context = {

                              'success'    : False

                          }
                return JsonResponse( context )

        except Exception : ## catch the DoesNotExist exception
            context = {

                          'success'    : False

                      }
            return JsonResponse( context )

## logout procedure
@checkIfLoggedIn
def logout( request ) :
    request.session.flush()

    ## get comments in reverse order
    commentsList = Comment.objects.order_by( '-publicationDate' )[  : 5 ]
    idList       = getIdList( commentsList )

    ## check if not logged in
    if ( 'username' not in request.session ) :
        context = {

                     'commentsList' : commentsList,
                     'idList'       : idList

                  }
        return render( request , 'newspaper/index1.html' , context )


## update a user's details
@checkIfLoggedIn
def updateDetails( request ) :
    ## check if request is of type POST
    if ( request.method == 'POST' ) :
        ## extract name + description + price from request
        fName    = request.POST[ 'fName' ]
        pNumber  = request.POST[ 'pNumber' ]
        Email    = request.session[ 'username' ]
        Password = request.session[ 'password' ]

        ## validate inputs
        infoValid   = checkValidity( fName , pNumber , Email , Password )

        if ( infoValid ) :
            ## get object in question
            user = UserAccount.objects.get( email = Email )
            user.first_name  = fName
            user.phoneNumber = pNumber
            user.save()
            context = {

                          'success'    : True,
                          'fName'      : fName,
                          'pNumber'    : pNumber

                      }
            return JsonResponse( context )

        else :   ## return bad JSON
            context = {

                          'success'    : False

                      }
            return JsonResponse( context )

## register method
def createUser( request ) :
    ## check if request is of type POST
    if ( request.method == 'POST' ) :
        ## extract name + description + price from request
        fName    = request.POST[ 'fName' ]
        pNumber  = request.POST[ 'pNumber' ]
        Email    = request.POST[ 'email' ]
        Password = request.POST[ 'password' ]

        ## validate inputs
        infoValid   = checkValidity( fName , pNumber , Email , Password )

        try :
            if ( infoValid ) : ## return good JSON
                newUser = UserAccount( username = Email , password = Password , first_name = fName ,
                                       phoneNumber = pNumber , email = Email )
                newUser.save()
                context = {

                              'success'    : True

                          }
                return JsonResponse( context )

            else :   ## return bad JSON
                context = {

                              'success'    : False

                          }
                return JsonResponse( context )

        except IntegrityError :
            context = {

                          'success'    : False

                      }
            return JsonResponse( context )

## calls .get() on model, but raises HTTP404 instead of model's DoesNotExist exception
def detail( request , articleID ) :
    ## check if not logged in
    if ( 'username' not in request.session ) :
        article = get_object_or_404( Article , pk = articleID )
        return render( request , 'newspaper/detail.html' , { 'article' : article } )

    else : ## logged in
        ## get name (via username) to return with render for welcome message
        name         = getName( request.session['username'] )
        article      = get_object_or_404( Article , pk = articleID )
        context      = {

                           'fName'   : name ,
                           'article' : article

                       }
        return render( request , 'newspaper/detail2.html' , context )

## post a comment on an article
@checkIfLoggedIn
def postComment( request ) :
    infoValid = True
    ## extract data to form new comment obj.
    username  = request.session[ 'username' ]
    id        = request.POST[ 'articleID' ]
    post      = request.POST[ 'post' ]
    date      = timezone.now()

    ## get the UserAccount obj. for whoever is logged in
    user = UserAccount.objects.get( email = username )

    ## get the Article obj. for the article
    article = Article.objects.get( pk = id )

    ## check if name is in correct format + != empty
    if ( post.isspace() or not post ) :
        context = {

                    'success'  : False

                  }
        return JsonResponse( context )

    comment = Comment( username = user , articleID = article , post = post , publicationDate = date , email = username)
    comment.save()
    context = {

                'success'  : True

              }
    return JsonResponse( context )

## delete a comment
def deleteComment( request , id ):
    Comment.objects.filter( pk = id ).delete()
    return JsonResponse({})

## get comments for an article
def getComments( request , id ) :
    comments     = Comment.objects.filter( articleID = id )
    commentsList = list( comments.values() )
    return JsonResponse( commentsList , safe = False )

## get likes for an article
def getLikes( request , articleID ) :
    ## get the article in question
    article     = Article.objects.get( pk = articleID )
    likeCount    = getVoteCount( 'like' , article )
    dislikeCount = getVoteCount( 'dislike' , article )
    if ( 'username' in request.session ) :
        ## check if user has liked/disliked before
        try :
            ## get the user in question
            username  = request.session[ 'username' ]
            user        = UserAccount.objects.get( email = username )
            status      = ''
            like        = Like.objects.filter( articleID = article ).get( userID = user )
            status      = like.typeOfLike
            context = {

                        'likeCount'    : likeCount,
                        'dislikeCount' : dislikeCount,
                        'status'       : status

                      }
            return JsonResponse( context )

        ## user hasn't liked/dislikd before
        except Exception :
            context = {

                        'likeCount'    : likeCount,
                        'dislikeCount' : dislikeCount,
                        'status'       : 'unselected'
                      }
            return JsonResponse( context )

    ## not logged in
    else :
        context = {

                    'likeCount'    : likeCount,
                    'dislikeCount' : dislikeCount,
                  }
        return JsonResponse( context )



## add a like to an article
@checkIfLoggedIn
def likeArticle( request ) :
    username  = request.session[ 'username' ]
    articleID = request.POST['articleID']

    ## get the user + article in question
    user      = UserAccount.objects.get( email = username )
    article   = Article.objects.get( pk = articleID )

    ## check if the article is currently liked
    try :
        status      = ''
        likeDeleted = False
        like        = Like.objects.filter( articleID = article ).get( userID = user )

        ## check if we have deleted the like
        if ( like.typeOfLike == 'dislike' ) :
            ## change type of like from DISLIKE --> LIKE
            like.typeOfLike = 'like'
            like.save()
            status   = 'like'

        else :
            like.delete()
            status   = 'unselected'

        ## get a count for all of the likes
        likeCount    = getVoteCount( 'like' , article )
        dislikeCount = getVoteCount( 'dislike' , article )
        context = {

                    'likeCount'    : likeCount,
                    'dislikeCount' : dislikeCount,
                    'status'   : status

                  }
        return JsonResponse( context )

    ## no record match --> therefore this is being liked for the first time
    except Exception :
        ## make + save new like

        like = Like( typeOfLike = 'like' , userID = user , articleID = article )
        like.save()

        ## get a count for all of the likes
        likeCount    = getVoteCount( 'like' , article )
        dislikeCount = getVoteCount( 'dislike' , article )
        context = {

                    'likeCount'    : likeCount,
                    'dislikeCount' : dislikeCount,
                    'status'   : 'like'

                  }
        return JsonResponse( context )


## add a dilike to an article
@checkIfLoggedIn
def dislikeArticle( request ) :
    username  = request.session[ 'username' ]
    articleID = request.POST['articleID']

    ## get the user + article in question
    user      = UserAccount.objects.get( email = username )
    article   = Article.objects.get( pk = articleID )

    ## check if the article is currently liked
    try :
        status         = ''
        dislikeDeleted = False
        dislike        = Like.objects.filter( articleID = article ).get( userID = user )

        ## check if we have deleted the like
        if ( dislike.typeOfLike == 'like' ) :
            ## change type of like from LIKE --> DISLIKE
            dislike.typeOfLike = 'dislike'
            dislike.save()
            status   = 'dislike'

        else :
            dislike.delete()
            status   = 'unselected'

        ## get a count for all of the likes
        likeCount    = getVoteCount( 'like' , article )
        dislikeCount = getVoteCount( 'dislike' , article )
        context = {

                    'likeCount'    : likeCount,
                    'dislikeCount' : dislikeCount,
                    'status'   : status

                  }
        return JsonResponse( context )

    ## no record match --> therefore this is being disliked for the first time
    except Exception :
        ## make + save new like

        dislike = Like( typeOfLike = 'dislike' , userID = user , articleID = article )
        dislike.save()

        ## get a count for all of the likes
        likeCount    = getVoteCount( 'like' , article )
        dislikeCount = getVoteCount( 'dislike' , article )
        context = {

                    'likeCount'    : likeCount,
                    'dislikeCount' : dislikeCount,
                    'status'   : 'dislike'

                  }
        return JsonResponse( context )


#########################################################################################


## helper method which checks if an entered email is available
def checkIfUniqueLogin( request ) :
    try :
        Email = request.POST[ 'email' ]
        user  = UserAccount.objects.get( username = Email )
        return HttpResponse("<p style = 'color : red;'>&nbsp;&#x2718; This username is taken</p>")

    except UserAccount.DoesNotExist :
        return HttpResponse("<p style = 'color : green;'>&nbsp;&#x2714; This username is available</p>")

## helper method which checks if login email is valid
def checkIfEmailIsRegistered( request ) :
    try :
        Email = request.POST[ 'email' ]
        user  = UserAccount.objects.get( username = Email )
        return HttpResponse("<p style = 'color : green;'>&nbsp;&#x2714; This username is registered</p>")

    except UserAccount.DoesNotExist :
        return HttpResponse("<p style = 'color : red;'>&nbsp;&#x2718; This username is NOT registered</p>")

## helper method which checks if input is acceptable
def checkValidity( fName , pNumber , Email , Password ) :

    import re

    ## check if name is in correct format + != empty
    if ( fName.isspace() or not fName ) :
        return False

    ## check if password is in correct format + != empty
    if ( not Password or Password.isspace() ) :
        return False

    ## check if email is in correct format
    emailRegex = re.compile( "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,10})$" )
    isEmail    = re.match( emailRegex , Email )
    if ( isEmail is None ):
        return False

    ## check if telephone is in correct format
    telephoneNumberRegex = re.compile( "^[0-9]{11,11}$" )
    isTelephoneNumber    = re.match( telephoneNumberRegex , pNumber )
    if ( isTelephoneNumber is None ):
        return False

    return True

## helper method returns the username of a user
def getUsername( request , id ) :
    ## get the UserAccount obj.
    user    = get_object_or_404( UserAccount , pk = id )
    context = {

                'username' : user.username

              }
    return JsonResponse( context )

## helper method which returns the name of a user
def getName( username ) :
    user     = get_object_or_404( UserAccount , email = username )
    return user.first_name

## helper method which returns a list of id's linked to each comments from arg.
def getIdList( commentsList ) :
    toReturn = []

    for comment in commentsList :
        article = comment.articleID
        id      = article.id
        toReturn = toReturn + [ id ]

    return toReturn

## helper method which returns a list of article's linked to each comments from arg.
def getArticleList( commentsList ) :
    toReturn = []

    for comment in commentsList :
        article = comment.articleID
        headline = article.headline
        toReturn = toReturn + [ headline ]

    return toReturn


def getLoggedINUsername(request):
    if ( 'username' in request.session ) :
        username  = request.session[ 'username' ]
        context = {
                        'result'   : True,
                        'username'  : username

                  }
        return JsonResponse(context)
    else:
        context = {
                        'result'   : False,
                        'username'  : ""

                  }
        return JsonResponse(context)

## this helper method return a int of the total likes/dislikes an article has
def getVoteCount( voteType , article ) :
    ## get a count for all of the LIKES / DISLIKES
    voteList = Like.objects.filter( typeOfLike = voteType ).filter( articleID = article )
    return len( voteList )
