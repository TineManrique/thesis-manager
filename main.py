import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    gender = ndb.StringProperty(indexed=True)
    age = ndb.IntegerProperty()
    address = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<h1>Main Page</h1>')


class AboutPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to my site\'s about page!')

class CreateStudentPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create_student_page_bootstrap.html')
        self.response.write(template.render())

    def post(self):
        student = Student()

        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.gender = self.request.get('gender')
        student.age = int(self.request.get('age'))
        student.address = self.request.get('address')
        student.key = student.put()
        student.put()
        self.redirect('/success')

class SuccessPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success_page.html')
        self.response.write(template.render())
        

class StudentListPage(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.date).fetch()
        logging.info(students)
        template_data = {
            'student_list': students
        }
        template = JINJA_ENVIRONMENT.get_template('student_list_page.html')
        self.response.write(template.render(template_data))

class StudentPage(webapp2.RequestHandler):
    def get(self, student_id):
        students = Student.get_by_id(int(student_id))
        template_data = {
            'student': students
        }
        template = JINJA_ENVIRONMENT.get_template('student_page.html')
        self.response.write(template.render(template_data))
    def post(self, student_id):
        student = Student.get_by_id(int(student_id))
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.gender = self.request.get('gender')
        student.age = int(self.request.get('age'))
        student.address = self.request.get('address')
        student.put()

class EditPage(webapp2.RequestHandler):
    def get(self, student_id):
        students = Student.get_by_id(int(student_id))
        template_data = {
            'student': students
        }
        template = JINJA_ENVIRONMENT.get_template('edit_page.html')
        self.response.write(template.render(template_data))
    def post(self, student_id):
        student = Student.get_by_id(int(student_id))
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.gender = self.request.get('gender')
        student.age = int(self.request.get('age'))
        student.address = self.request.get('address')
        student.put()
        self.redirect('/success')
        

class DeletePage(webapp2.RequestHandler):
    def get(self, student_id):
        student = Student.get_by_id(int(student_id))
        student.key.delete()
        self.redirect('/success')
        
app = webapp2.WSGIApplication([
    ('/student/list/(.*)', StudentPage),
    ('/student/delete/(.*)', DeletePage),
    ('/student/edit/(.*)', EditPage),
    ('/student/create', CreateStudentPage),
    ('/student/list', StudentListPage),
    ('/about', AboutPage),
    ('/success', SuccessPage),
    ('/home', MainPage),
    ('/', MainPage)
], debug=True)
