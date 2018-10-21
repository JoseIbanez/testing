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



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/temp', TempPage),
    ('/new', NewTempPage)
], debug=True)
