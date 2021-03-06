from flask import Flask,render_template,request,redirect,url_for
from InstagramAPI import InstagramAPI
import time

app = Flask(__name__)
app.secret_key= ''

def getPosts(InstagramAPI,user_id):
	import time
	myposts=[]
	has_more_posts = True
	next_max_id = True
	max_id=""
	while has_more_posts:
	    InstagramAPI.getSelfUserFeed(maxid=max_id)
	    if InstagramAPI.LastJson['more_available'] is not True:
	        has_more_posts = False 
	        # print "stopped"
	    
	    max_id = InstagramAPI.LastJson.get('next_max_id','')
	    myposts.extend(InstagramAPI.LastJson['items']) #merge lists
	    time.sleep(2) # Slows the script down to avoid flooding the servers 
	return myposts

def getFollowers(InstagramAPI,user_id):
	followers = []
	InstagramAPI.getProfileData()
	user_id= InstagramAPI.LastJson['user']['pk']
	next_max_id = True
	while next_max_id:
	    if next_max_id == True:
	        next_max_id = ''
	    _ = InstagramAPI.getUserFollowers(user_id,maxid = next_max_id)
	    followers.extend(InstagramAPI.LastJson.get('users',[]))
	    next_max_id = InstagramAPI.LastJson.get('next_max_id','')
	    time.sleep(1)
	return followers

def getFollowing(InstagramAPI,user_id):
	following = []
	InstagramAPI.getProfileData()
	user_id= InstagramAPI.LastJson['user']['pk']
	next_max_id = True
	while next_max_id:
	    if next_max_id == True:
	            next_max_id = ''
	    _ = InstagramAPI.getUserFollowings(user_id,maxid = next_max_id)
	    following.extend(InstagramAPI.LastJson.get('users',[]))
	    next_max_id = InstagramAPI.LastJson.get('next_max_id','')
	    time.sleep(1)
	return following

@app.route('/', methods = ['GET','POST'])
def home():	
	return render_template('home.html')

@app.route('/profile', methods = ['GET','POST'])
def profile():
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]

		from InstagramAPI import InstagramAPI
		InstagramAPI = InstagramAPI(username, str(password))
		InstagramAPI.login()
		InstagramAPI.getProfileData()
		user_id= InstagramAPI.LastJson['user']['pk']

		bio = InstagramAPI.LastJson['user']['biography']
		bio = bio.split('\n')
		me = [ InstagramAPI.LastJson['user']['username'] ,
		 		InstagramAPI.LastJson['user']['full_name'] ,
		 		InstagramAPI.LastJson['user']['profile_pic_url'] ,
		 		bio ]
		import time

		myposts = getPosts(InstagramAPI,user_id)
		# print(myposts[0])
		  
		# print len(myposts)

		followers = []
		following = []
		followers_list = getFollowers(InstagramAPI,user_id)
		following_list = getFollowing(InstagramAPI,user_id)
		followers_list_usernames = [ele['username'] for ele in followers_list]
		following_list_usernames = [ele['username'] for ele in following_list]

		fans = set(followers_list_usernames).difference(set(following_list_usernames))
		celebs = set(following_list_usernames).difference(set(followers_list_usernames))

	return render_template('profile.html' ,myposts = myposts, me = me ,followers = followers_list , following = following_list , fans = fans , celebs = celebs)

if __name__ == '__main__':
    app.run(port=5000,debug = True)
