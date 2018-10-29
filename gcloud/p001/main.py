# Copyright 2016 Google Inc.
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

import webapp2
import temp
import niceTag
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class TempPage(webapp2.RequestHandler):
    def get(self):

        t = temp.Measure.query_probe("siguenza").fetch(10)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(t)

class NewTempPage(webapp2.RequestHandler):
    def get(self):

        t = temp.Measure.create()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(t)


class Build(webapp2.RequestHandler):
    def get(self):

        #get params
        id = self.request.get('id')

        #ddbb query
        try:
            r = temp.Measure.fetch(id)[0]
            name  = str(r.name)
            value = str(r.value)
        except:
            name = "none"
            value = "na"

        #generate image
        nt = niceTag.Tag(name,value)     
        t = nt.getSVG()

        self.response.headers['Content-Type'] = 'image/svg+xml'
        self.response.write(t)

    def post(self):

        body = json.loads(self.request.body)
        id    = body.get('id')
        name  = body.get('name')
        value = body.get('value')

        temp.Measure.update(id, name, value)

        r = { "id" : id, "value": value }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(r)


app = webapp2.WSGIApplication([
    ('/',      MainPage),
    ('/temp',  TempPage),
    ('/new',   NewTempPage),
    ('/build', Build)
], debug=True)
