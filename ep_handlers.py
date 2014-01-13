import main
import os
import webapp2
import logging
import handlers
import data
from google.appengine.ext import db

class EditHandler(handlers.WikiHandler):

	def get(self, url = "/"):
		if not self.check_login():
			self.redirect('/login')
			return
		entry = db.GqlQuery("SELECT * FROM Entry WHERE url = \'%s\' ORDER BY created DESC" % url).get()
		content = ''
		if entry is not None:
			content = entry.content
		t_values = {
			'content': content,
			'item1': 'View',
			'item2': 'Logout',
			'link1': url,
			'link2': '/logout'
		}
		self.write_template('edit.html', t_values, True)


	def post(self, url = "/"):
		content = self.request.get('content')
		a = data.Entry(url = url, content = content)
		a.put()
		self.redirect(url)


class PageHandler(handlers.WikiHandler):
	def get(self, url):
		entry = db.GqlQuery("SELECT * FROM Entry WHERE url = \'%s\' ORDER BY created DESC" % url).get()
#data.Entry.all().filter("url =", url).order('created').get()
		#entry = None
		if entry is None:
			if self.check_login():
				self.redirect('/_edit' + url)
				return
			else:
				self.redirect('/login')
				return
		t_values = {
			'content': entry.content
		}
		self.write_template("page.html", t_values, False, False)

