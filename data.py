#here's where we'll put the user class and any other classes we need to store data
class User(object):
    """A user for the application."""

    def __init__(self, username, email, about='', owned_ideas=[], followed_ideas=[]):
        """
            Here is where we store the data for the user self
            
            Parameters
            -----------
            self: 
                data struct used to store everything unique about the user
            username: str
                the user name of the user (generated from user.html)
            about: str
                String containing the summary of the user (generated from user.html)
            owned_ideas: str[]
                A list of all of the ideas created by the user (generated from user.html)
            followed_ideas: str[]
                A list of all of the ideas that the user has found and appreciates (generated from user.html)
                
            
            Returns
            --------
            Returns the user of the website
        """
        self.username = username
        self.email = email
        self.owned_ideas = owned_ideas
        self.followed_ideas = followed_ideas
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'owned_ideas': self.owned_ideas,
            'followed_ideas': self.followed_ideas
        }
class Idea(object):
    def __init__(self, owner, title, projdate, description, image, tags):
        self.owner = owner
        self.title = title
        self.projdate = projdate
        self.description = description
        self.image = image
        self.tags = tags
    def to_dict(self):
        return{
            'owner': self.owner,
            'title': self.title,
            'date': self.projdate,
            'description': self.description,
            'image': self.image,
            'tags': self.tags
        }