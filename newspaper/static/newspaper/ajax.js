// listener for registering new accounts
jQuery('#register').click(function(){
	jQuery.ajax({
		type    : 'POST',
		url     : '/newspaper/createUser/' ,
    data    : {
    			'fName'               : jQuery('#fName').val(),
    			'pNumber'             : jQuery('#pNumber').val(),
    			'email'               : jQuery('#email').val(),
    			'password'            : jQuery('#password').val(),
          'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
    		},
    success  : checkRegisterCredentials,
		dataType : 'json'
	});
});

// listener for logging in
jQuery('#login').click(function(){
	jQuery.ajax({
		type     : 'POST',
		url      : '/newspaper/login/' ,
    data     : {
    			 'email'	             : jQuery('#emailLogin').val(),
           'password'            : jQuery('#password').val(),
           'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
    		},
    success  : checkLoginCredentials,
		dataType : 'json'
	});
});

// listener for logging out
jQuery('#logout').click(function(){
	jQuery.ajax({
		type     : 'GET',
		url      : '/newspaper/logout/' ,
    data     : {},
    success  : loadIndexPage,
		dataType : 'json'
	});
});

// listener for updating accounts
jQuery('#updateDetails').click(function(){
	jQuery.ajax({
		type    : 'POST',
		url     : '/newspaper/updateDetails/' ,
    data    : {
    			'fName'               : jQuery('#fName').val(),
    			'pNumber'             : jQuery('#pNumber').val(),
          'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
    		},
    success  : checkUpdateCredentials,
		dataType : 'json'
	});
});

// listener for loading lifestyle PAGE
jQuery('#lifestyle').click(function(){
	  jQuery.ajax({
		type     : 'GET',
		url      : '/newspaper/lifestyleRedirect/' ,
		dataType : 'html'
	});
});

// listener for posting a comment
jQuery('#postComment').click(function(){
    jQuery.ajax({
    type     : 'POST',
    url      : '/newspaper/postComment/' ,
    data     :
    {

      'articleID'           : jQuery('#articleID').val(),
      'post'                : jQuery('#comment').val(),
      'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()

    },
    success  : reloadComments,
    dataType : 'json'
  });
	jQuery('#comment').val('')
});

// listener method for when deleting a comment
function deleteComment( id )
{

		jQuery.ajax({
		type     : 'POST' ,
		url      : '/newspaper/deleteComment/' + id + '/' ,
		data     :
		{
			'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
		},
		success  :reloadComments,
		});

}

// listener for adding a like to an article
jQuery('#likeButton').click(function(){
    jQuery.ajax({
    type     : 'POST',
    url      : '/newspaper/likeArticle/' ,
    data     :
    {

      'articleID'           : jQuery('#articleID').val(),
      'type'                : 'like',
      'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()

    },
    success  : refreshLikes,
    dataType : 'json'
  });
});

// listener for adding a dislike to an article
jQuery('#dislikeButton').click(function(){
    jQuery.ajax({
    type     : 'POST',
    url      : '/newspaper/dislikeArticle/' ,
    data     :
    {

      'articleID'           : jQuery('#articleID').val(),
      'type'                : 'dislike',
      'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()

    },
    success  : refreshLikes,
    dataType : 'json'
  });
});

/*************************------- HELPER METHODS ------****************************/

// helper methods request the index page
function loadIndexPage()
{

    jQuery.ajax({
      type     : 'GET',
      url      : '/newspaper/registerRedirect/' ,
      success  : refreshFrontEnd ,
      dataType : 'html'
    });

}

// helper method which checks whether a request to add a new user is SUCCESSFULL
function checkRegisterCredentials( response )
{

    if ( response.success )
    {

        // go back to index
        location.href = "/newspaper/";

    }

    else
    {

        alert( 'ERROR : pls use common sense + fill in fields properly' ) ;

    }

}

// helper method which checks whether a request to add a new user is SUCCESSFULL
function checkLoginCredentials( response )
{

    if ( response.success )
    {

        // go back to index
        location.href = "/newspaper/";

    }

    else
    {

        alert( 'ERROR : wrong login credentials, pls fill in fields properly' ) ;

    }

}

// helper method which checks whether a request to add a new user is SUCCESSFULL
function checkUpdateCredentials( response )
{

    if ( response.success )
    {

        // get info. from response
        var name = response.fName;
        var num  = response.pNumber;

        // build success message
        var newLine    = "\r\n"
        var successMSG = 'SUCCESS : your details have been updated!';
            successMSG = successMSG + newLine ;
            successMSG = successMSG + 'Full Name : ' + name ;
            successMSG = successMSG + newLine ;
            successMSG = successMSG + 'Telephone : ' + num ;

        // confirm to user that info. has been updated
        alert( successMSG );

        // go back to index
        location.href = "/newspaper/";

    }

    else
    {

        alert( 'ERROR : pls use common sense + fill in fields properly' ) ;

    }

}

// helper method which checks in real time if a candidate email is available
jQuery('#email').blur(function(){
	jQuery.ajax({
		type     : 'POST',
		url      : '/newspaper/checkIfUniqueLogin/',
		data     : {
				  'email'	              : jQuery('#email').val(),
				  'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
			  },
		success  : appendResponse,
		dataType : 'html'
	});
});

// helper method which checks in real time if an email used to login is registered
/*jQuery('#emailLogin').blur(function(){
	jQuery.ajax({
		type     : 'POST',
		url      : '/newspaper/checkIfEmailIsRegistered/',
		data     : {
				  'email'	              : jQuery('#emailLogin').val(),
				  'csrfmiddlewaretoken' : jQuery("input[name=csrfmiddlewaretoken]").val()
			  },
		success  : appendResponse,
		dataType : 'html'
	});
});*/

// helper method which appends a response depending on whether an email is available or nah
function appendResponse( response )
{

	 jQuery( '#availabilityCheck' ).html( response );

}

// helper method which loads the returned render
function refreshFrontEnd( response )
{

    jQuery( 'html' ).empty();
    jQuery( 'html' ).append( response );

}

// helper method which refreshes the comments
function refreshComments( response, userList )
{
		currentUsername = getLoggedINUsername();

    // clear the current comments
    jQuery( 'h6' ).empty();
    jQuery( '#comments' ).empty();

    var commentID , username , post , postDate ;

    for( var i = response.length-1 ; i >= 0 ; i-- )
    {

          var toAppend = ""
          commentID    = response[i].id;
          username     = response[i].email;
          post 				 = response[i].post ;
          postDate     = response[i].publicationDate ;


          toAppend = toAppend + '<div id = c-' + commentID + ' >'
          toAppend = toAppend + '<br><poster>'     + username  + '</poster>' ;
          toAppend = toAppend + '<pTime> • '   + postDate  + '</pTime>'
          toAppend = toAppend + '<br>'
          toAppend = toAppend + '<p>'          +   post    + '</p>'
					// check if the current comment being appended is logged in
					if( currentUsername == username )
					{

							toAppend = toAppend + '<button class = "smallButton" onclick="deleteComment(\''+commentID+'\')" style="margin-top:-5px; margin-bottom:0px;"> Delete </button>'

					}


          toAppend = toAppend + '</div>'

          // append comment
          jQuery( "#comments" ).append( toAppend );

      }

      jQuery( "h6" ).append( response.length + " Comments" );
}

// helper method gets username from a given ID
function getUsername( id )
{

		  jQuery.ajax({
		  type     : 'GET' ,
		  url      : '/newspaper/getUsername/' + id + '/' ,
		  dataType : 'json'
			});

}

// get the username of whoever is logged in
function getLoggedINUsername()
{

		var username = "";
		jQuery.ajax({
			async    : false,
			type     : 'GET' ,
			url      : '/newspaper/getLoggedINUsername/' ,
			dataType : 'json',
			success  : function(response)
			{
				if(response.result)
				{
						username=response.username
				}

			}
			});

			return username;

}
