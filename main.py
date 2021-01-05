
from flask import Flask
from markupsafe import escape
from post import Post

app = Flask(__name__)



@app.route('/')
def index():
	return 'Index Page'

@app.route('/user/<username>')
def profile(username):
	return '{}\'s profile'.format(escape(username))

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return 'Subpath %s' % escape(subpath)

# Unique URLs / Redirection Behavior¶
@app.route('/projects/')		# This can be accessed by '127.0.0.1:5000/projects' and '127.0.0.1:5000/projects/'
def projects():
	return 'The projects Page'

@app.route('/about')			# this can only be accessed by '127.0.0.1:5000/login'
def about():
	return 'The about page'

# URL Building
from flask import url_for
with app.test_request_context():
	print(url_for('index'))
	print(url_for('about'))
	print(url_for('about', next="/"))
	print(url_for('profile', username='John'))

"""
The code above will print:
/
/login
/login?next=%2F
/user/John
"""
# HTTP Methods
from flask import request
@app.route('/regester', methods=['GET', 'POST']) # only answers to POST and GET
def regester():
	if request.method == 'POST':
		return do_the_regester()
	else:
		return show_the_regester_form()

def do_the_regester():
	return escape("Do the regester here")

def show_the_regester_form():
	# Static files
	style_css = url_for('static', filename='style.css')
	print(f"Style css : {style_css}")
	return escape("Show ther ")


# Rendering Templates by using Jinjia2 template engine
from flask import render_template
@app.route('/home/')
@app.route('/home/<name>')
def home(name=None):
	return render_template('home.html', name=name)


# The Request Object
from flask import request
from flask import redirect
@app.route('/login', methods=['POST', 'GET'])	# this can only be accessed by '127.0.0.1:5000/login'
def login():
	error = None
	get_username_password_from_request(request)
	if request.method == 'GET':
		username = request.args.get('username')
		password = request.args.get('password')
		print(f'accoutn: {username}, pw: {password}')
		if valid_login(username, password):
			return redirect(url_for('home'))
		else:
			error = 'Invalid username and password'
			return render_template('login.html', error=error)
			
	else:
		error = 'Request is not POST'
	return render_template('login.html')

def get_username_password_from_request(request):
	print(f"request form: {request.form}")
	# method 1
	try:
		username = request.form['username']
		password = request.form['password']
	except KeyError:
		print ("Please append username and password")

	# method 2
	username = request.args.get('username')
	password = request.args.get('password')

	print(f"request {request}")
	print(f'accoutn: {username}, pw: {password}')

import re
def valid_login(username, password):
	if username and password:
		print("username and password are valid")
		pwR = re.match(r'[0-9a-zA-Z]+', password)
		usR = re.match(r'[0-9a-zA-Z]+', username)
		return pwR and usR
		# return re.match(r'\A\w{6,10}\z\A(?=\w{6,10}\z)(?=[^a-z]*[a-z])(?=(?:[^A-Z]*[A-Z]){3})\D*\d.*\z', password)
		# 	pattern = re.compile(r'[0-9a-zA-Z]{0, 8}')
		# return re.match(pattern, password) and re.match(pattern, username)
	else:
		print("username and password are not valid")
		return False

# API with JSON
from flask import jsonify
import json
@app.route("/posts/")
def get_posts():
	posts = Post.get_all_posts()
	return jsonify(posts)

# Cookies and Session
from flask import make_response

@app.route('/cookies/')
def cookies():
	# Reading cookies
	username = request.cookies.get('username'
		)

	# Storing cookies
	resp = make_response(f"here how to handle cookies. The cookie which your sent to me: {request.cookies}")
	resp.set_cookie('username', 'hut')
	return resp

from flask import session
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/session/')
def session_s():
	if 'hut' in session:
		return 'Logged in as %s' % escape(session['username'])
	return 'You are not logged in'

@app.route('/log_in/', methods=['GET', 'POST'])
def log_in():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for(index))
	return '''
			<form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
    
@app.route('/logout/')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))    


