from django.shortcuts import render
import twitter_tools
import os
from django.http import HttpResponse


def query_by_ext(ext):
  mimetype = {
          'css': 'text/css',
          'js': 'application/x-javascript',
          'png': 'image/png',
          'PNG': 'image/png',
          'jpg': 'image/jpeg',
          'jpeg': 'image/jpeg',
          'JPG': 'image/jpeg',
          'JPEG': 'image/jpeg',
          'gif': 'image/gif',
          'GIF': 'image/gif',
          'xml': 'text/xml',
          'swf': 'application/x-shockwave-flash',
          'html': 'text/html',
      }
  return mimetype.get(ext, '')

def get_file(request, ext):
  path = request.path
  abspath = os.path.abspath('.') + path
  stream = open(abspath, 'rb').read()

  mimetype = query_by_ext(ext)
  return HttpResponse(stream, mimetype = mimetype)

def home(request):
  return render(request, 'search.html')

def recommend(request):
  if request.method == 'GET' and request.GET.get('user_name', ''):
    user_name = request.GET['user_name']
    friends = twitter_tools.get_friends(user_name)
    if not friends:
      error = 'Not Following Anyone?'
      return render(request, 'error.html', {'error':error, 'user_name':user_name})
    
    friends = [x['user_id'] for x in friends]
    friends_in_database = twitter_tools.get_friend_in_database(friends)
    
    if not friends_in_database:
      error = 'No Followee In Database?'
      return render(request, 'error.html', {'error':error, 'user_name':user_name})
    
    recommended = twitter_tools.get_recommended(friends_in_database)
      
    for f in friends_in_database:
      print f

    print '*'* 200
    for f in recommended:
      print f
    
    friends_in_database = twitter_tools.get_users(friends_in_database)
    recommended = twitter_tools.get_users(recommended)
    return render(request, 'result.html', {'friends':friends_in_database, 'recommended': recommended})
  else:
    error = 'Not User Name Provided?'
    return render(request, 'errors.html', {'error':error, 'user_name':user_name})
