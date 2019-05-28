from flask import Flask

app = Flask(__name__)
app.secret_key= '04c816ee38ea4ee1843c22a6e67d8406'

@app.route('/')
def home():	
	return('<h1>Instassitant</h1>')

if __name__ == '__main__':
    app.run(port=5000,debug = True)