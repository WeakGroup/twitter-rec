from django.shortcuts import render
import twitter_tools

def home(request):
  return render(request, 'search.html')

def recommend(request):
  if request.method == 'GET' and request.GET.get('user_name', ''):
    user_name = request.GET['user_name']
    friends = twitter_tools.get_friends(user_name)
    if not friends:
      return render(request, 'error.html', {'error', error})
    
    friends = [x['user_id'] for x in friends]
    friends_in_database = twitter_tools.get_friend_in_database(friends)
    
    if not friends_in_database:
      return render(request, 'error.html', {'errors', errors})
    
    recommended = twitter_tools.get_recommended(friends_in_database)
      
    for f in friends_in_database:
      print f

    print '*'* 200
    for f in recommended:
      print f
    
    return render(request, 'result.html', {'friends':friends_in_database, 'recommended': recommended})
  else:
    return errors(request, 'errors.html', {'errors':errors})
