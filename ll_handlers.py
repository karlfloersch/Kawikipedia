import main
import os
import webapp2
import logging
import handlers


class LoginHandler(handlers.WikiHandler):
	def get(self):
		self.write_login()

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')


		if self.login_user(username, password):
			self.redirect('/')
		else:
			self.write_login(username, "Invalid Login.")

	def write_login(self, username = "", error = ""):
		t_values = {
			'username': username,
			'error': error
		}
		self.write_template("login.html", t_values)

class LogoutHandler(handlers.WikiHandler):
	def get(self):
		user_cookie = ";"
		self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % user_cookie)
		self.redirect("/")

