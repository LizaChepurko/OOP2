from User import User
from Exceptions import LogInLogoutError


# Represents a singleton instance of a social network.

class SocialNetwork:
    """
    Represents a singleton instance of a social network.

    Attributes:
        _instance (SocialNetwork): The singleton instance of the social network.
        users (list): A list of active users in the social network.
        name: The name of the social network.
        logedoutUsers (dict): A dictionary containing logged-out users and their passwords.

    """
    _instance = None

    """
    Creates a new instance of the SocialNetwork class if it doesn't exist, or returns the existing instance.

    Args:
        name (str): The name of the social network.

    Returns:
        SocialNetwork: The singleton instance of the social network.
    """

    def __new__(cls, name: str):
        cls.users = []
        cls.name = name
        cls.logedoutUsers = dict()
        # If an instance does not exist, create one
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("The social network Twitter was created!")
        return cls._instance

    """
    Registers a new user in the social network with the given username and password.

    Returns:
        User: The newly created user object.

    Raises:
        LogInLogoutError: If there is an error during sign-up process, such as existing username or invalid password.
    """

    def sign_up(self, username: str, password: str):
        exception = LogInLogoutError(self,username)
        exception.signUpError(username, password)
        exception.notValidPassword(password)
        user = User(username, password)
        self.users.append(user)
        return user

    """
    Allows a user to log in to the social network with the given credentials.

    Raises:
        LogInLogoutError: If there is an error during the login process, such as connected user or not existed user.
    """

    def log_in(self, username: str, password: str):
        exception = LogInLogoutError(self,username)
        exception.logInError(username, password)
        exception.logInUserIsentExistError(username, password)
        for user in self.logedoutUsers:
            if self.logedoutUsers[user] == password:
                user.connect()
                self.logedoutUsers.pop(user)
                self.users.append(user)
                print(user.username + " connected")
                break;

    """
     Logs out a user from the social network.

     Raises:
         LogInLogoutError: If there is an error during the logout process, such as user not found or already logged out.
     """
    def log_out(self, username: str):
        exception = LogInLogoutError(self,username)
        exception.logOutError(username)
        exception.loggedOutNotFound(username)
        for user in self.users:
            if user.username == username:
                user.disconnect()
                self.users.remove(user)
                self.logedoutUsers.update({user : user.password})
                print(user.username+" disconnected")
                break;

    """
    Returns a string representation of the social network, including its name and active users.
    Users are sorted alphabetically by username
    """
    def __str__(self):
        s = self.name +" social network:\n"
        self.users.sort(key=lambda user: user.username, reverse=False)
        for user in self.users:
            s += user.__str__()+"\n"
        return s

