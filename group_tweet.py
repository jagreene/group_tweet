import time
import csv
import os.path
import random
from cmd2 import Cmd
from twython import Twython



class Tweeter(object):
    """Utility class built for Cheryl Greene, sends tweets to a list of people"""
    def __init__(self):
        super(Tweeter, self).__init__()
        self.tweets = []
        self.replaced = "[replace]"
        self.groups = {}
        self.APP_KEY = "OChCFw3S4DI2a5K5rMJddYuRl"
        self.APP_SECRET = "4zHhjozNQpugIJhMYwYvLKGAfUOAWy2dyTp9epmbn58dMMscYz"
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET)
        auth = self.twitter.get_authentication_tokens()
        self.OAUTH_TOKEN = auth['oauth_token']
        self.OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
        self.auth_url = auth['auth_url']

        # try:
        if os.path.exists('oauth.csv'):
            oauth_dict = dict(csv.reader(open('oauth.csv','r')))
            self.OAUTH_TOKEN = oauth_dict["OAUTH_TOKEN"]
            self.OAUTH_TOKEN_SECRET = oauth_dict["OAUTH_TOKEN_SECRET"]
            self.twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
            self.twitter.verify_credentials()
            self.authd = True
            print("Authorized")
        else:
            print("Not already authorized")
            self.authd = False
        # except:
        #     print("Not already authorized")
        #     self.authd = False


    def auth_self(self):
        if not self.authd:
            try:
                pin = raw_input("Please go to "+self.auth_url+" and after authentication type in your pin code: ")
                print("")
                self.twitter = Twython(self.APP_KEY, self.APP_SECRET, self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

                final_step = self.twitter.get_authorized_tokens(pin)
                oauth_dict = {"OAUTH_TOKEN": final_step['oauth_token'],
                              "OAUTH_TOKEN_SECRET": final_step['oauth_token_secret'],
                              "PIN": pin
                }

                with open('oauth.csv', 'wb') as f:
                    w = csv.writer(f)
                    # print oauth_dict
                    w.writerows(oauth_dict.items())
                    f.close()

                self.authd = True
            except:
                self.authd = False
                print("Authentication failed")
        else:
            print("Already authorized")

    def load_group(self):
        group_file = raw_input("What is the file path to your csv file: ")
        print("")
        group_name = raw_input("What is the name of your group: ")
        self.groups[group_name] = list(csv.reader(open(group_file, 'r')))

    def check_groups(self):
        print(self.groups)

    def check_tweets(self):
        print(self.tweets)

    def set_tweet(self):
        tweet = raw_input("Type the tweet you would like to send. Type [replace] where you'd like the handle to go: ")
        self.tweets.append(tweet)

    def send_tweet(self):
        if self.authd:
            if len(self.tweets) >  0:
                for group in self.groups:
                    for handle in self.groups[group]:
                        tweet = random.choice(self.tweets)
                        mod_text = tweet.replace(self.replaced, handle[0])
                        print(mod_text)
                        self.twitter.update_status(status=mod_text)
                        time.sleep(random.randrange(1800, 3600))
            else:
                print("You need to set a tweet first")
        else:
            print("You are not authorized, run auth_self")

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

    def do_check_tweets(self, input):
        self.tweeter.check_tweets

    def do_send_tweet(self, input):
        self.tweeter.send_tweet()

if __name__ == "__main__":
    interface = Interface()
    interface.cmdloop()
