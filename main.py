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
from pattern.web import Wikipedia
import webapp2
import logging
import jinja2
from convert2html import plaintext2html
from urllib2 import quote
from backend import plot,title_from_imdb,more_movie_info
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader("template"), autoescape = True)
import os, sys; sys.path.insert(0, os.path.join("..", ".."))
engine = Wikipedia(language="en")
class Handler(webapp2.RequestHandler):
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)
  def render_str(self,template,**params):
    t = jinja_env.get_template(template)
    return t.render(params)
  def render(self,template,**kw):
    self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
       self.render("index.html")

    def post(self):
		movie_name = self.request.get('movie_name')
		corrected_movie_name = title_from_imdb(movie_name) 
                movie_info = more_movie_info(corrected_movie_name)
                poster_url = movie_info["Poster"]
		try:
			story = plaintext2html(plot(corrected_movie_name))
    
			if story:
				#self.response.out.write("<img src= "+ poster_url+"><a href='http://tts-api.com/tts.mp3?q="+story.replace(" ","+").replace("<br>","")+"'>Who reads, give me mp3</a><br/>"+plaintext2html(plot(corrected_movie_name)))
                                self.render("story.html",title=corrected_movie_name,released=movie_info["Released"],story=story,imgsrc=movie_info["Poster"],rating=movie_info["imdbRating"],director=movie_info["Director"],mp3link = "http://tts-api.com/tts.mp3?q="+ quote(story) )
			else:
				self.render("index.html",error=1)
		except:
		   self.render("index.html",error=1)
app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
