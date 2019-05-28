from flask import Flask,render_template,request,redirect,url_for


app = Flask(__name__)
app.secret_key= '04c816ee38ea4ee1843c22a6e67d8406'

@app.route('/', methods = ['GET','POST'])
def home():	
	return render_template('home.html')

@app.route('/profile', methods = ['GET','POST'])
def profile():
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]
		from InstagramAPI import InstagramAPI
		import time
		InstagramAPI = InstagramAPI(username, str(password))
		InstagramAPI.login()
		InstagramAPI.getProfileData()
		user_id= InstagramAPI.LastJson['user']['pk']
		import time
		followers = []
		next_max_id = True
		while next_max_id:
		    print next_max_id
		    if next_max_id == True:
		            next_max_id = ''
		    _ = InstagramAPI.getUserFollowers(user_id,maxid = next_max_id)
		    followers.extend(InstagramAPI.LastJson.get('users',[]))
		    next_max_id = InstagramAPI.LastJson.get('next_max_id','')
		    time.sleep(1)
		followers_list = followers
		print(len(followers_list))
	return render_template('profile.html')




if __name__ == '__main__':
    app.run(port=5000,debug = True)