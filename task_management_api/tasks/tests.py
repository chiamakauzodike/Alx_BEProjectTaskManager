from django.test import TestCase
from rest_framework.test import APIRequestFactory
from tasks.models import Task, User
from datetime import datetime, timedelta

# Create your tests here.

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=datetime.now() + timedelta(days=1),
            priority='High',
            status='Pending',
            owner=self.user,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.priority, 'High')
        self.assertEqual(self.task.status, 'Pending')
        self.assertEqual(self.task.owner, self.user)

    def test_task_due_date_in_future(self):
        self.assertTrue(self.task.due_date > datetime.now())

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), self.task.title)
