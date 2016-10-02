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
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class TemplateHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(TemplateHandler):
    def render_front(self):
        posts = db.GqlQuery("select * from Blog "
                            "order by created DESC")

        self.render("index.html",posts=posts)
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #textarea = self.request.get("text")
        self.render_front()
        #self.response.out.write(form)
class NewPostHandler(TemplateHandler):
    def render_newpost(self, subject="",content="",error=""):
        #arts = db.GqlQuery("select * from Blog "
        #                    "order by created DESC")
        self.render("newpost.html",subject,content,error)
    def get(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        error = self.request.get("error")
        #self.response.headers['Content-Type'] = 'text/plain'
        #textarea = self.request.get("text")
        if subject or content or error:
            self.render_newpost(subject=subject,content=content,error=error)
        else:
            self.render("newpost.html")
        #self.response.out.write(form)
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if content and subject:
            b = Blog(subject=subject,content=content)
            b.put()
            self.redirect("/")
        else:
            error = "we need both a subject and content"
            self.render_newpost(subject,content,error)




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost',NewPostHandler)
], debug=True)