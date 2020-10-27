import json
from flask import Flask, render_template, request
from email.utils import parseaddr
from datetime import date
import hashlib
import flask
import datastore
import data

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Y6A8DyIVLQIx4qGKgmPmm31e56WEQYLGqn15E5uu'

@app.route("/")
def root():
    user = get_user()
    if user:
        return flask.redirect('/profile')
    return show_page('home.html', 'Main Page')

@app.route("/home")
def home():
    return show_page('home.html', 'Main Page')
    
@app.route("/createProject")
def createProject():
    user=get_user()
    if user:
        return show_page('createProject.html', 'Create a Project')
    else:
        return login();

@app.route('/login',)
def login():
    return show_page('login.html', 'Log in')

@app.route('/createAccount',)
def createAccount():
    return show_page('createAccount.html', 'Create Account')

@app.route('/signout',)
def signout():
    flask.session['user'] = None
    return flask.redirect('/')
    
@app.route('/about')
def pitch():
    return show_page('about.html', 'About')

@app.route('/FAQ')
def FAQ():
    return show_page('FAQ.html', 'FAQ')

@app.route('/profile')
def profile():
    user = get_user()
    owned_ideas = get_user_owned_ideas(user)
    followed_ideas = get_user_followed_ideas(user)
    return show_page('profile.html','profile', owned_ideas = owned_ideas[0:3], followed_ideas=followed_ideas[0:3])

@app.route('/my-ideas')
def my_ideas():
    user = get_user()
    owned_ideas = get_user_owned_ideas(user)
    return show_page('owned-ideas.html', 'My ideas', idea_list=owned_ideas)

@app.route('/followed-ideas')
def followed_ideas():
    user = get_user()
    followed_ideas = get_user_followed_ideas(user)
    return show_page('following.html', 'Following', idea_list=followed_ideas)

@app.route('/idea')
def idea():
    title = request.args.get('ideaTitle')
    idea = datastore.load_idea(title)
    return show_page('idea.html', title, idea)

@app.route('/browse')
def browseIdeas():
    idea_list = datastore.load_all_ideas()
    return show_page('browse.html', 'Browse Ideas', idea_list=idea_list)

@app.route('/apply')
def apply():
    return show_page('apply.html', 'Apply')

@app.route('/doCreateProject', methods=['POST'])
def doCreateProject():
    owner = get_user()
    title = flask.request.form.get('title')
    projdate = date.today().strftime('%m-%d-%y')
    description = {
        'Conjecture': flask.request.form.get('conjecture'),
        'Quality': flask.request.form.get('quality'),
        'Qualifications': flask.request.form.get('qualifications'),
        'Work': flask.request.form.get('work'),
        'Additional Info': flask.request.form.get('additionalInfo')
    }
    image = flask.request.form.get('image')
    tags = flask.request.form.getlist('tags')
    newIdea = data.Idea(owner, title, projdate, description, image, tags)
    
    datastore.save_idea(newIdea)
    datastore.add_idea_to_user(owner, title)
    return show_page('idea.html', title, idea=newIdea)

@app.route('/dosignin', methods=['POST'])
def dosignin():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    passwordhash = get_password_hash(password)
    user = datastore.load_user(username, passwordhash)
    if user:
        flask.session['user'] = user.username
        return flask.redirect('/profile')
    else:
        return login()

@app.route('/makeAccount', methods=['POST'])
def makeAccount():
    #Here's where the python code will go to setup the user account
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    email = flask.request.form.get('email')
    errors = []
    email_parts = parseaddr(email)
    if len(email_parts) != 2 or not email_parts[1]:
        errors.append('Invalid email address: ' + str(email))

    #validate username doesnt already exist
    result = datastore.user_exists_check(username)
    if(result is not None):
        errors.append( 'ERROR: user already exists! Please choose a different username')

    #validate email doesn't already exist
    result = datastore.email_exists_check(email)
    if(result is not None):
        errors.append( 'ERROR: email already in use! Please choose a different email')

    followed_ideas = ['ideaHub']
    user = data.User(username, email, followed_ideas=followed_ideas)
    if errors:
        return show_page('/createAccount.html', 'Sign Up', errors = errors)
    else:
        passwordhash = get_password_hash(password)
        datastore.save_user(user, passwordhash)
        flask.session['user'] = user.username
        return flask.redirect('/profile')
    return None

@app.route('/toggleFollow', methods=['POST'])
def toggleFollow():
    idea = request.args.get('idea')
    user = get_user()
    followed_ideas = datastore.load_user_followed_ideas(user)
    if idea not in followed_ideas:
        followed_ideas.append(idea)
    else:
        followed_ideas.remove(idea)
    datastore.save_user_followed_ideas(user, followed_ideas)
    return show_page('idea.html', idea, idea=datastore.load_idea(idea))

def get_password_hash(pw):
    encoded = pw.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

def show_page(page, title, idea=None, idea_list=None, owned_ideas=None, followed_ideas=None, errors=None):
    return flask.render_template(page, 
                                page_title=title, 
                                user=get_user(), 
                                idea=idea, 
                                ideaList=idea_list, 
                                ownedIdeas=owned_ideas, 
                                followedIdeas=followed_ideas, 
                                errors=errors)

def get_user():
    return flask.session.get('user', None)

def get_user_owned_ideas(username):
    user = username
    id_list = datastore.load_user_owned_ideas(user) #list of titles of all the ideas
    idea_list = []
    for idea in id_list:
        idea_list.append(datastore.load_idea(idea))
    return idea_list

def get_user_followed_ideas(username):
    user = username
    id_list = datastore.load_user_followed_ideas(user) #list of titles of all the ideas
    idea_list = []
    for idea in id_list:
        idea_list.append(datastore.load_idea(idea))
    return idea_list

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True) #127.0.0.1
