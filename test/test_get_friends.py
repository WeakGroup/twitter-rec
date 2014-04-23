import twitter
api = twitter.Api(consumer_key = 'CYmLMxVw2u84w35DW0uQ',
        consumer_secret = 'vHrlCfVsN2U1r5S4aFg0Sww0GlC2uMzyK47WGK68',
        access_token_key = '222736994-C4eDZcrgFdKbHDBoHaIdnqBWxMkUrfgMOUJvKHYI',
        access_token_secret = 'mOezG78FDFLHHdNmWti5O2MLeOZ4j8aq4jgKqvtWwm6j5')

def get_follower_count(user_id):
    users = api.GetFollowerIDs(user_id = user_id)
    return len(users)
#users = api.GetFollowers(screen_name = 'Liao_Eason')
#users = api.GetFollowers(user_id = 1160999622)
users = api.GetFriends()
for u in users:
    print u.name, u.id
    if get_follower_count(u.id) > 200:
        print 'more than 200 followers'
    

