#here's where we'll interact with gcloud datastore to manage the database
from google.cloud import datastore

import data


_USER_ENTITY = 'ideaHubUser'
_IDEA_ENTITY = 'idea'

def _get_client():
    """Build a datastore client."""
    return datastore.Client()

def log(msg):
    """Log a simple message."""
    print('ideaHub datstore: %s' % msg)

def _load_key(client, entity_type, entity_id=None, parent_key=None):
    """Load a datastore key using a particular client, and if known, the ID.
    Note that the ID should be an int - we're allowing datastore to generate
    them in this example.

    Here we are initializing the key
    if we know the entity_id then we use the entity_type, entity_id, and parent_key
    
    Parameters
    -----------
    client: 
        data struct storing entity_type, entity_id, parent_key
    username: str
        client the user name of the user (generated from user.html)
    entity_id: str
        String containing the summary of the user (generated from user.html)
    parent_key: str
        A list of all of the ideas created by the user (generated from user.html)        
            
    Returns
    --------
    we are returning the clinet key
    """
    key = None
    if entity_id:
        key = client.key(entity_type, entity_id, parent=parent_key)
    else:
        # this will generate an ID
        key = client.key(entity_type)
    return key

def _load_entity(client, entity_type, entity_id, parent_key=None):
    """Load a datstore entity using a particular client, and the ID."""
    key = _load_key(client, entity_type, entity_id, parent_key)
    entity = client.get(key)
    log('retrieved entity for ' + str(entity_id))
    return entity

def load_user(username, passwordhash):
    """Load a user based on the passwordhash; if the passwordhash doesn't match
    the username, then this should return None.
    Here is where we store the data for the user self
    
    Parameters
    -----------
    username: str 
        The username given by login.html
    password: str
        The password given by login.html and see if it matches a hash values
            compared to the username
    
    Returns
    --------
    Returns the user if the hash matches the usernmae and returns nothing if the hash doesn't match
    """    
    
    client = _get_client()
    q = client.query(kind=_USER_ENTITY)
    q.add_filter('username', '=', username)
    q.add_filter('passwordhash', '=', passwordhash)
    for user in q.fetch():
        return data.User(user['username'], user['email'], user['owned_ideas'], user['followed_ideas'])
    return None

def load_idea(title):
    """
    Here is where we store the data for the user self
        
    Parameters
    -----------
    title: str 
        search to find if a valid title was searched
        
    Returns
    --------
    If the valid title was found return the idea. Otherwise return nothing
    """  
    client = _get_client()
    q = client.query(kind=_IDEA_ENTITY)
    
    q.add_filter('title', '=', title)
    
    for r in q.fetch():
        return data.Idea(r['owner'], r['title'], r['date'], r['description'], r['image'], r['tags'])
    return None

def load_all_ideas():
    """Returns all ideas in the databse.  Could take a long time if there are millions of ideas, but thats a good problem
    because then we've made it big and have millions of dollars"""
    client = _get_client()
    q = client.query(kind=_IDEA_ENTITY)
    idea_list = []
    for r in q.fetch():
        idea_list.append(data.Idea(r['owner'], r['title'], r['date'], r['description'], r['image'], r['tags']))
    return idea_list

def load_user_owned_ideas(username):
    """Return a list of titles of a user's owned ideas .
    Here is where we load all the ideas made by the user
    
    Parameters
    -----------
    username: str 
        The username is based from the entity. If it exists return all the ideas made by the owner
    
    Returns
    --------
    Returns all the ideas made by the username
    """      
    user = _load_entity(_get_client(), _USER_ENTITY, username)
    if user:
        return user['owned_ideas']
    else:
        return []

def load_user_followed_ideas(username):
    """Return a list of titles of a user's followed ideas .
        Here is where we load all the ideas followed by the username
        
        Parameters
        -----------
        username: str 
            The username is based from the entity. If it exists return all the ideas followed by the owner
        
        Returns
        --------
        Returns all the ideas followed by the user
    """  

    user = _load_entity(_get_client(), _USER_ENTITY, username)
    if user:
        return user['followed_ideas']
    else:
        return []

def save_user(user, passwordhash):
    """Save the user details to the datastore (passed as a user object shown in data.py)
            
        Parameters
        -----------
        user:  
            data struct of the user being saved into the entity
        passwordhash: str
            load the password hash to associate with the username
        
        Returns
        --------
        Loads the user profile to the entity to be accessed later
    """  

    client = _get_client()
    entity = datastore.Entity(_load_key(client, _USER_ENTITY, user.username))
    entity['username'] = user.username
    entity['email'] = user.email
    entity['passwordhash'] = passwordhash
    entity['owned_ideas'] = user.owned_ideas
    entity['followed_ideas'] = user.followed_ideas
    client.put(entity)


def save_idea(idea):
    """Save an idea object (shown in data.py) to the databse"""
    client = _get_client()
    entity = datastore.Entity(_load_key(client, _IDEA_ENTITY))
    entity['owner'] = idea.owner
    entity['title'] = idea.title
    entity['date'] = idea.projdate
    entity['description'] = idea.description
    entity['image'] = idea.image
    entity['tags'] = idea.tags
    client.put(entity)

def save_user_owned_ideas(username, ideas):
    """Save a list of ideas as the user's owned ideas (ideas should be a list of Strings representing the title of an idea)"""
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    if user:
        user['owned_ideas'] = ideas
    client.put(user)

def save_user_followed_ideas(username, ideas):
    """Save a list of ideas as the user's owned ideas (ideas should be a list of Strings representing the title of an idea)"""
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    if user:
        user['followed_ideas'] = ideas
        
    client.put(user)

def add_idea_to_user(username, idea):
    """Adds an idea (again, by title) to a user's list of owned ideas"""
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    if user:
        user['owned_ideas'].append(idea)
    client.put(user)

def add_followed_idea_to_user(username, idea):
    """Adds an idea (again, by title) to a user's list of owned ideas"""
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    if user:
        user['followed_ideas'].append(idea)
    client.put(user)

def user_exists_check(username):
    """Determine if a username already exists"""
    client = _get_client()
    q = client.query(kind=_USER_ENTITY)
    q.add_filter('username', '=', username)
    result = None
    for user in q.fetch():
        result = user
    return result

def email_exists_check(email):
    """Determine if an email already exists"""
    client = _get_client()
    q = client.query(kind=_USER_ENTITY)
    q.add_filter('email', '=', email)
    result = None
    for email in q.fetch():
        result = email
    return result