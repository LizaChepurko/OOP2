from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from Exceptions import NotOnlineNotificationError
import User

class Like:
    """
    Represents a like action on a post.

    Attributes:
        user: The user who liked the post.
        author: The author of the post.
    """
    def __init__(self, user: User, author: User):
        self.user = user
        self.author = author
    """
    adds the notification to the author notifications list
    Prints a notification to the post author when a user likes their post.
    
    NOTE: the author can like the post but does not have notification about it. 
    """
    def printnotification(self, user):
        if user.username != self.author.username:
            self.author.add_notification(user.username + " liked your post")
            print("notification to " + self.author.username + ": " + user.username + " liked your post")


class Comment:
    """
       Represents a comment action on a post.

       Attributes:
           user: The user who commented on the post.
           text: The comment text.
           author: The author of the post.

       """

    def __init__(self, user: User, text: str, author: User):
        self.text = text
        self.user = user
        self.author = author

    """
    adds the notification to the author notifications list
    Prints a notification to the post author when a user comments on their post.
    
    NOTE: the author can comment on the post but does not have notification about it. 
    """

    def printnotification(self, user: User, text: str):
        if user.username != self.author.username:
            self.author.add_notification(user.username + " commented on your post")
            print("notification to " + self.author.username + ": " + user.username + " commented on your post: " + text)


class PostFactory:
    """
    Factory class for creating different types of posts.
    """
    """
     Creates a post of the specified type with the given arguments.

     Args:
         post_type (str): The type of post to create.
         *args: Positional arguments for initializing the post.
         **kwargs: Keyword arguments for initializing the post.

     Returns:
         Post: The created post object.
     """
    @staticmethod
    def create_post(post_type, *args, **kwargs):
        if post_type == "Text":
            return TextPost(*args, **kwargs)
        elif post_type == "Image":
            return ImagePost(*args, **kwargs)
        elif post_type == "Sale":
            return SalePost(*args, **kwargs)


class TextPost(Like, Comment):

    """
    Represents a text post in the social network.

    Inherits from:
        Like: Allows users to like text posts.
        Comment: Allows users to comment on text posts.

    Attributes:
        author (User): The author of the post.
        content (str): The content of the text post.
        likes (set): Set of users who liked the post.
        comments (dict): Dictionary of comments on the post.
    """
    def __init__(self, content: str, author: User):
        # self.text = "Text"
        self.author = author
        self.content = content
        self.likes = set()
        self.comments = dict()

    """
    Allows users to like text posts.
      Raises:
          NotOnlineNotificationError: If users try to give likes while they are not online.
    """
    def like(self, user: User):
        exception = NotOnlineNotificationError(user, self)
        exception.cantLike()
        self.likes.add(user)
        l = Like(user, self.author)
        l.printnotification(user)

    """
    Allows users to comment text posts.
      Raises:
          NotOnlineNotificationError: If users try to comment while they are not online.
    """

    def comment(self, user: User, text: str):
        exception = NotOnlineNotificationError(user, self)
        exception.cantComment()
        self.comments.update({user.username: text})
        c = Comment(user, text, self.author)
        c.printnotification(user, text)

    """
    A unique notification related to this post type.
    Uses: helps to print a global notification in the network
    """

    def notification(self):
        return (" published a post:\n"
                + "\"" +self.content+"\"")

    """
    Method for printing the TextPost object
    """
    def __str__(self):
        return self.author.username + self.notification()+"\n"


class ImagePost(Like, Comment):
    """
    Represents an image post in the social network.

    Inherits from:
        Like: Allows users to like image posts.
        Comment: Allows users to comment on image posts.

    Attributes:
        author (User): The author of the post.
        image (str): The image file path.
        likes (set): Set of users who liked the post.
        comments (dict): Dictionary of comments on the post.
    """

    def __init__(self,image: str, author: User):
        # self.post_type = "image"
        self.author = author
        self.image = mpimg.imread(image)
        self.likes = set()
        self.comments = dict()

    """
    Allows users to like image posts.
      Raises:
          NotOnlineNotificationError: If users try to give likes while they are not online.
    """
    def like(self, user: User):
        exception = NotOnlineNotificationError(user, self)
        exception.cantLike()
        self.likes.add(user)
        l = Like(user, self.author)
        l.printnotification(user)

    """
    Allows users to comment image posts.
      Raises:
          NotOnlineNotificationError: If users try to comment while they are not online.
    """

    def comment(self, user: User, text: str):
        exception = NotOnlineNotificationError(user, self)
        exception.cantComment()
        self.comments.update({user.username: text})
        c = Comment(user, text, self.author)
        c.printnotification(user, text)

    """
    A unique notification related to this post type.
    Uses: helps to print a global notification in the network
    """
    def notification(self):
        return " posted a picture"

    """
    Method for displaying the image in the image post.
    """
    def display(self):
        plt.imshow(self.image)
        plt.axis('off')  # Turn off axis
        print("Shows picture")
        plt.show()

    """
    Method for printing the ImagePost object
    """

    def __str__(self):
        return self.author.username + self.notification()+"\n"


class SalePost(Like, Comment):
    """
    Represents a sale post in the social network.

    Inherits from:
        Like: Allows users to like sale posts.
        Comment: Allows users to comment on sale posts.

    Attributes:
        item (str): The item for sale.
        price (float): The price of the item.
        author (User): The author of the post.
        location (str): The pickup location for the item.
        available (bool): Indicates whether the item is available for sale.
        likes (set): Set of users who liked the post.
        comments (dict): Dictionary of comments on the post.
    """

    def __init__(self, item: str, price, location: str, author: User):
        self.item = item
        self.price = price
        self.author = author
        self.location = location
        self.available = True
        self.likes = set()
        self.comments = dict()

    """
    Allows users to like sale posts.
      Raises:
          NotOnlineNotificationError: If users try to give likes while they are not online.
    """
    def like(self, user: User):
        exception = NotOnlineNotificationError(user, self)
        exception.cantLike()
        self.likes.add(user)
        l = Like(user, self.author)
        l.printnotification(user)

    """
    Allows users to comment sale posts.
      Raises:
          NotOnlineNotificationError: If users try to comment while they are not online.
    """
    def comment(self, user: User, text: str):
        exception = NotOnlineNotificationError(user, self)
        exception.cantComment()
        self.comments.update({user.username: text})
        c = Comment(user, text, self.author)
        c.printnotification(user, text)

    """
    A unique notification related to this post type.
    Uses: helps to print a global notification in the network
    """
    def notification(self):
        if self.available == True:
            return (" posted a product for sale:\n"
                    "For sale! " + self.item + ", price: " + str(self.price) + ", pickup from: " + self.location)
        else:
            return (" posted a product for sale:\n"
                    "Sold! " + self.item + ", price: " + str(self.price) + ", pickup from: " + self.location)

    """
    Marks the item as sold and notifies other users.
    """
    def sold(self, password: str):
        if password is None or password != self.author.password:
            self.available = True
            return False
        else:
            self.available = False
            print(self.author.username + "'s product is sold")
            return True
    """
    Applies a discount to the item price and notify others.
    Args:
        dis(int): discount on price by dis percentage 
    Raises:
        If users entered a worng password or the product is unavailable.
    
    """
    def discount(self, dis, password: str):
        if password != self.author.password:
            raise Exception("password isn't correct")
        elif not self.available:
            raise Exception("Cant preform discount on unavailable post")
        else:
            self.price = (self.price) * ((100 - dis) / 100)
            print("Discount on " + self.author.username + " product! the new price is: " + str(self.price))

    """
    Method for printing the SalePost object
    """
    def __str__(self):
        return self.author.username + self.notification()+"\n"

