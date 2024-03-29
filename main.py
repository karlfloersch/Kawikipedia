#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import handlers
import ep_handlers
import ll_handlers
import signup_handler
import random
import string
import hashlib
import re
import data
from google.appengine.ext import db



###
# USE FOR MAPPING PAGE TO HANDLER
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
	('/login', ll_handlers.LoginHandler),
    ('/logout', ll_handlers.LogoutHandler),
    ('/signup', signup_handler.SignupHandler),
    ('/_edit', ep_handlers.EditHandler),
    ('/_edit' + PAGE_RE, ep_handlers.EditHandler),
    (PAGE_RE, ep_handlers.PageHandler)
], debug=True)
#-	-	-	-	-	-	-	-	-#

###
#FOR USE WITH RENDERING STUFF SON
jinja_auto = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
jinja_no_auto = jinja2.Environment(autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
#-	-	-	-	-	-	-	-	-#

####
#FOR USE WITH USER DATABASE PASSWORD MAKING#
def make_salt():
    ans = ""
    for i in range(0,5):
        ans += random.choice(string.letters)
    return ans

def make_pw_hash(name, pw, salt = None):
    if salt is None:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)
#-	-	-	-	-	-	-	-	-	-	-	-#









####
#FOR USE WITH CHECKING IF INPUT WAS VALID FOR USERS#
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#-	-	-	-	-	-	-	-	-	-	-	-	-#



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello worrdd!')



