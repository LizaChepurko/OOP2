import SocialNetwork
import User
import PostFactory

# A class for defining custom exceptions used in the project.

class NotOnlineNotificationError(Exception):
    """
    Custom exception class for handling notifications when the user is not online.

    Attributes:
        user: The user associated with the notification.
        post: The post associated with the notification.

    """

    def __init__(self, user: User, post: PostFactory):
        self.post = post
        self.user = user

    """
    Raises an exception if the user is not connected when trying to like a post.
    """
    def cantLike(self):
        try:
            not self.user.connected and self.post.like(self.user)
        except Exception:
            raise Exception("User is not connected")

    """
    Raises an exception if the user is not connected when trying to comment on a post.
    """
    def cantComment(self):
        try:
            not self.user.connected and self.post.comment(self.user)
        except Exception:
            raise Exception("User is not connected")

    """
    Raises an exception if the user is not connected when trying to publish a post.
    """
    def cantPublish(self):
        if not self.user.connected:
            raise Exception("User cant publish a post while disconnected")



class UsertoUserError(Exception):
    """
    Custom exception class for handling user-to-user related errors.

    Attributes:
        user1: The first user involved in the error.
        user2: The second user involved in the error.
    """
    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2

    """
    Raises an exception if user1 is not connected when trying to follow user2.
        user1: The user attempting to follow.
        user2: The user being followed.
    """
    def cantFollow(self, user1, user2):
        try:
            not user1.connected and user1.follow(user2)
        except Exception:
            raise Exception("User is not connected, cant follow")

    """
    Raises an exception if user1 is not connected when trying to unfollow user2.
        user1: The user attempting to unfollow.
        user2: The user being unfollowed.
    """

    def cantUnFollow(self, user1, user2):
        try:
            not user1.connected and user1.unfollow(user2)
        except Exception:
            raise Exception("User is not connected, cant unfollow")

    """
    Raises an exception if user1 tries to unfollow a user who isn't being followed.
    """
    def cantUnfollowIsntFollowed(self):
        if self.user2 not in self.user1.following:
            raise Exception("This user cant unfollow unfollowed user")

    """
    Raises an exception if user tries to follow themselves.
    """
    def cantFollowYourSelf(self):
        if self.user1 is self.user2:
            raise Exception("You can't follow yourself!")



class LogInLogoutError(Exception):

    """
    Custom exception class for handling login and logout related errors.

    Attributes:
        network: The social network instance associated with the error.
        name: The name of the user involved in the error.
    """

    def __init__(self,network:SocialNetwork,name:str):
        self.network = network
        self.name = name

    """
    Raises an exception if the user is already logged in.
    """

    def logInError(self, username, passward):
        for user in self.network.users:
            if user.username == username and user.password == passward:
             raise Exception("User already logged in")

    """
    Raises an exception if the user isn't exist and try to log in.
    """
    def logInUserIsentExistError(self, username, password):
        size_users = len(self.network.users)
        i = 0
        c = 0
        size_loggedout = len(self.network.logedoutUsers)
        for user in self.network.users:
            if not(user.username == username and user.password == password):
                i+=1
        for user in self.network.logedoutUsers:
            if not(user.username == username and user.password == password):
                c+=1
        if i == size_users and c == size_loggedout:
            raise Exception("User does not exist")

    """
    Raises an exception if the user is already logged out.
    """
    def logOutError(self, username):
        for user in self.network.logedoutUsers:
            if user.username == username:
             raise Exception("User already logged out")

    """
    Raises an exception if the user is not found (user is either connected or not exist).
    """
    def loggedOutNotFound(self,username):
        size = len(self.network.users)
        i = 0
        for user in self.network.users:
            if user.username != username:
                i+=1
        if i == size:
            raise Exception("User not found")

    """
    Raises an exception if the user already exists during sign-up.
    """
    def signUpError(self, username, password):
       for user in self.network.users:
          if user.username is username and user.password is password:
                raise Exception("User already exist")

    """
    Raises an exception if the password is not valid during sign-up.
    """
    def notValidPassword(self, password):
        if not 4 <= len(password) <= 8:
            raise Exception("You should enter a valid password")
