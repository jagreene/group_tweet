import pandas
import csv
import os.path
from cmd2 import Cmd
from twython import Twython



class Tweeter(object):
    """Utility class built for Cheryl Greene, sends tweets to a list of people"""
    def __init__(self):
        super(Tweeter, self).__init__()
        self.delay = 30000
        self.replaced = "[replace]"
        self.groups = {}
        self.APP_KEY = "OChCFw3S4DI2a5K5rMJddYuRl"
        self.APP_SECRET = "4zHhjozNQpugIJhMYwYvLKGAfUOAWy2dyTp9epmbn58dMMscYz"
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET)
        auth = self.twitter.get_authentication_tokens()
        self.OAUTH_TOKEN = auth['oauth_token']
        self.OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
        self.auth_url = auth['auth_url']

        try:
            if os.path.exists('oauth.csv'):
                oauth_df = pandas.read_csv('oauth.csv')
                with open('oauth.csv','wb') as f:
                    w = csv.writer(f)
                    w.writerows(oauth_df.items())
                self.authd = True
            else:
                self.authd = False
        except:
            self.authd = False


    def auth_self(self):
        try:
            pin = raw_input("Please go to "+self.auth_url+" and after authentication type in your pin code")
            twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

            final_step = twitter.get_authorized_tokens(pin)
            oauth_dict = {self.OAUTH_TOKEN: final_step['oauth_token'],
                          self.OAUTH_TOKEN_SECRET: final_step['oauth_token_secret']
            }

            with open('oauth.csv','wb') as f:
                w = csv.writer(f)
                w.writerows(oauth_dict.items())

            self.authd = True
        except:
            self.authd = False
            print("Authentication failed")

    def load_group(self):
        group_file = raw_input("What is the file path to your csv file")
        group_name = raw_input("What is the name of your group")
        self.groups[group_name] = pandas.read_csv(group_file)

    def check_groups(self):
        print(self.groups)

    def set_tweet(self):
        tweet = raw_input("Type the tweet you would like to send. Type [replace] where you'd like the handle to go")
        self.tweet = tweet

    def send_tweet(self):
        if self.authd:
            for group in self.groups:
                for handle in group:
                    mod_text = self.tweet.replace(handle, self.replaced)
                    print(mod_text)
                    self.twitter.update_status(status=mod_text)

class Interface(Cmd):
    def preloop(self):
        print("Welcome to Group_Tweet!")
        print("To see a list of fuctions type help")
        print("If first time, run auth_self first")
        print("Next load each group from file")
        print("Next set your tweet")
        print("Lastly send your tweet")
        
        self.tweeter = Tweeter()
        self.completekey ='tab'

    def do_auth_self(self, input):
        self.tweeter.auth_self()

    def do_load_group(self, input):
        self.tweeter.load_group()

    def do_check_groups(self, input):
        self.tweeter.check_groups()

    def do_set_tweet(self, input):
        self.tweeter.set_tweet()

    def send_tweet(self, input):
        self.tweeter.send_tweet()

if __name__ == "__main__":
    interface = Interface()
    interface.cmdloop()