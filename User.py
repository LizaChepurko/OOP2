from abc import ABC, abstractmethod
from PostFactory import PostFactory
from Exceptions import UsertoUserError
from Exceptions import NotOnlineNotificationError


# Observer Design Pattern:
# The User and UserFollower classes demonstrate the Observer design pattern.
# User objects act as subjects, and UserFollower objects act as observers.
# When a User publishes a new post, it notifies all its followers (UserFollower objects)
# by calling the update method on each observer, passing the notification message.

class User(ABC):
    """
    Represents a user in the social network.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        followers (list): List of users who follow this user.
        following (list): List of users this user follows.
        posts (list): List of posts published by this user.
        notifications (list): List of notifications for this user.
        connected (bool): Indicates whether the user is currently connected to the network.
   """

    def __init__(self, username: str, password: str):
        self.followers = []
        self.following = []
        self.username = username
        self.password = password
        self.posts = []
        self.notifications = []
        self.connected = True

    """
    disconnects the user from the social network by changing the status of self.connected to False
    """

    def disconnect(self):
        if self.connected:
            self.connected = False

    """
    connects the user to the social network by changing the status of self.connected to True
    """

    def connect(self):
        if not self.connected:
            self.connected = True

    """
    Allows the user to follow another users.
    adding the followed user to the following list
    becomes an observer of the followed user by creating instance of UserFollower.
    Raises:
       UsertoUserError: user cant follow itself.
                        user cant follow while is not online

    """

    def follow(self, user):
        exception = UsertoUserError(self, user)
        exception.cantFollow(self, user)
        exception.cantFollowYourSelf()
        self.following.append(user)
        follower = UserFollower(self)
        user.followers.append(follower)
        print(self.username + " started following " + user.username)

    """
    Allows the user to unfollow another users.
    removes the followed user from the following list
    removing user from observers of the unfollowed user.
    Raises:
       UsertoUserError: user cant unfollow itself.
                        user cant unfollow while is not online
                        user cant unfollow an unfollowed user
    """

    def unfollow(self, user):
        exception = UsertoUserError(self, user)
        exception.cantUnFollow(self, user)
        exception.cantFollowYourSelf()
        exception.cantUnfollowIsntFollowed()
        self.following.remove(user)
        # Remove current user from the following list of the unfollowed user
        for follower in user.followers:
            if follower.get_user() == self:
                user.followers.remove(follower)
                print(self.username + " unfollowed " + user.username)

    """
    Notifies the user's followers about a new post.
    """

    def notify(self):
        for follower in self.followers:
            follower.update(f"{self.username} has a new post")

    """
    Publishes a new post of the specified type.

    Parameters:
        post_type (str): The type of post to be published ('Text', 'Image', or 'Sale').
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Post: The newly published post object.

    Raises:
        NotOnlineNotificationError: If the user is not connected, preventing them from publishing the post.

    This method creates a new post using the PostFactory, adds it to the user's list of posts,
    notifies followers about the new post, and returns the created post object.
    """

    def publish_post(self, post_type, *args, **kwargs):
        post = PostFactory.create_post(post_type, *args, **kwargs, author=self)
        exception = NotOnlineNotificationError(self, post)
        exception.cantPublish()
        self.posts.append(post)
        print(self.username + post.notification() + "\n")
        self.notify()
        return post

    """
    adds notification to notifications list of the user
    """

    def add_notification(self, notification: str):
        self.notifications.append(notification)

    """
    Prints the notifications of the user
    """

    def print_notifications(self):
        print(self.username + "'s notifications:")
        for notification in self.notifications:
            print(notification)

    """
    Method to print user data
    """

    def __str__(self):
        return "User name: " + self.username + ", Number of posts: " + str(
            len(self.posts)) + ", Number of followers: " + str(len(self.followers))


class Follower(ABC):
    """
    Abstract base class representing a follower of a user.

    Updates the follower with a new notification.

    """

    @abstractmethod
    def update(self, notification: str):
        pass


class UserFollower(Follower):
    """
    Represents a follower of a user in the social network.

    Attributes:
        user (User): The user being followed.
    """

    def __init__(self, user):
        self.user = user

    """
    Updates the follower with a new notification.
    """

    def update(self, notification: str):
        self.user.add_notification(notification)

    """
    Returns the user being followed.
    """

    def get_user(self):
        return self.user