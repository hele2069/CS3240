from django.test import TestCase
from django.utils import timezone
from .models import Profile, Courses, Schedule
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
import datetime
from django.utils import timezone
import pytz



# Create your tests here.
class LoginTest(TestCase):
    """
            Created to check test was working
            """
    def test_login(self):
        self.assertIs(False, False)

class ProfileTest(TestCase):
    """
            Ensures user is made
            """
    def test_setUp(self):
        usertest = User.objects.create_user(username='user4444', password='password4444')
        userprof = Profile(user=usertest)
        self.assertTrue(str(userprof)=="user4444")
    """
            Ensure users with same username do not get made
            """
    def test_duplicate_users(self):
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        userprof1 = Profile(user=usertest1)

        self.assertRaises(IntegrityError, User.objects.create_user, username='user4444', password='password4444')

    """
             Ensures multiple users with different usernames are allowed
             """
    def test_multiple_users_different_user_names(self):
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        userprof1 = Profile(user=usertest1)
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        userprof2 = Profile(user=usertest2)

        self.assertFalse(str(userprof1) == str(userprof2))

    """
              Ensures that empty username throws a value error
              """
    def test_empty_username(self):
        self.assertRaises(ValueError, User.objects.create_user, username='', password='password4444')

class CoursesTest(TestCase):
    """
    Ensures class is made
    """
    def test_setUp(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        self.assertTrue(str(testcourse)=="test0000")

    """
     Checks that course can be made without instructor
     """
    def test_no_instructor(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        self.assertTrue(str(testcourse)=="test0000")

    """
     Ensures that a course can be duplicated with multiple professors
     """
    def test_same_course_different_instructor(self):
        subject = "test"
        number = "0000"
        instructor1 = "tester1"
        instructor2 = "tester2"
        testcourse1 = Courses(subject = subject, number = number, instructor = instructor1)
        testcourse2 = Courses(subject = subject, number = number, instructor = instructor1)
        self.assertTrue(str(testcourse1)==str(testcourse2))

class AddCoursesTest(TestCase):
    """
    Creates 2 profiles, puts them in a course then checks that both appear in course list
    """
    def test_two_added_courses(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        userprof1.courses.add(testcourse)
        userprof2.courses.add(testcourse)

        self.assertTrue(userprof1 in testcourse.profile_set.all() and userprof2 in testcourse.profile_set.all())

    """
    Creates 2 profiles, puts one in a course and one not,
    then checks that only one appears in the course student list
    """
    def test_one_course(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        userprof1.courses.add(testcourse)

        self.assertTrue(userprof1 in testcourse.profile_set.all() and not(userprof2 in testcourse.profile_set.all()))

    """
        Creates 2 profiles, does not add either to course.
        Course should have zero entries.
        """

    def test_no_course(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject=subject, number=number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()


        self.assertTrue(not(userprof1 in testcourse.profile_set.all()) and not (userprof2 in testcourse.profile_set.all()))


class ToggleCoursesTest(TestCase):
    """
    Creates 2 profiles, puts them in a course then checks that both appear in course toggled on list
    """
    def test_two_toggled_courses(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        userprof1.courses.add(testcourse)
        userprof1.toggled_courses.add(testcourse)
        userprof2.courses.add(testcourse)
        userprof2.toggled_courses.add(testcourse)
        self.assertTrue(testcourse in userprof1.toggled_courses.all() and testcourse in userprof2.toggled_courses.all())

    """
    Creates 2 profiles, puts one in a course and one not,
    then toggles only one on, checks that only one appears in the course toggled student list
    """
    def test_one_toggled_course(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject = subject, number = number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        userprof1.courses.add(testcourse)
        userprof1.toggled_courses.add(testcourse)
        userprof2.courses.add(testcourse)

        self.assertTrue(testcourse in userprof1.toggled_courses.all() and not(testcourse in userprof2.toggled_courses.all()))

    """
        Creates 2 profiles, adds course to both but toggles neither on.
        Toggled courses should have zero entries.
        """

    def test_no_toggled_course(self):
        subject = "test"
        number = "0000"
        testcourse = Courses(subject=subject, number=number)
        testcourse.save()
        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        userprof1.courses.add(testcourse)
        userprof2.courses.add(testcourse)


        self.assertTrue(not(testcourse in userprof1.toggled_courses.all()) and not(testcourse in userprof2.toggled_courses.all()))

class ScheduleTest(TestCase):
    """
            Creates 2 profiles, creates meeting, ensures both profiles are in meeting
            """

    def test_scheduling_two_profiles(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course = 'CS3240', time = time1, location = 'Clemons')
        schedule1.save()


        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()

        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)

        self.assertTrue(userprof1 in schedule1.study_buddies.all() and userprof2 in schedule1.study_buddies.all())

    """
            Creates 3 profiles, creates meeting, ensures all profiles are in meeting
            """
    def test_scheduling_three_profiles(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course = 'CS3240', time = time1, location = 'Clemons')
        schedule1.save()


        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        usertest3 = User.objects.create_user(username='user444456', password='password4444')
        usertest3.save()
        userprof3 = Profile(user=usertest3, id=3)
        userprof3.save()

        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)
        schedule1.study_buddies.add(userprof3)

        self.assertTrue(userprof1 in schedule1.study_buddies.all() and userprof2 in schedule1.study_buddies.all() and userprof3 in schedule1.study_buddies.all())

    """
            Creates 3 profiles, deletes meeting, ensures that no profile sees meeting
            """
    def test_scheduling_delete_three_profiles(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course='CS3240', time=time1, location='Clemons')
        schedule1.save()

        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        usertest3 = User.objects.create_user(username='user444456', password='password4444')
        usertest3.save()
        userprof3 = Profile(user=usertest3, id=3)
        userprof3.save()

        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)
        schedule1.study_buddies.add(userprof3)
        schedule1.delete()

        self.assertTrue(len(userprof1.schedule_set.all())==0 and len(userprof2.schedule_set.all())==0 and len(userprof3.schedule_set.all())==0)

    """
            Creates 2 profiles, deletes one, checks if 1 profile remains
            """

    def test_scheduling_delete_user_profiles_two_profiles(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course='CS3240', time=time1, location='Clemons')
        schedule1.save()

        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()


        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)
        userprof2.delete()

        self.assertTrue(len(schedule1.study_buddies.all())==1)

    """
            Creates 3 profiles, deletes one, checks if 2 profiles remain
            """
    def test_scheduling_delete_user_profiles_three_profiles(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course='CS3240', time=time1, location='Clemons')
        schedule1.save()

        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        usertest3 = User.objects.create_user(username='user444456', password='password4444')
        usertest3.save()
        userprof3 = Profile(user=usertest3, id=3)
        userprof3.save()

        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)
        schedule1.study_buddies.add(userprof3)
        userprof3.delete()

        self.assertTrue(len(schedule1.study_buddies.all())==2)

    """
            Ensures different users can schedule different meetings without error
            """

    def test_scheduling_two_different_meetings(self):
        time1 = timezone.now()
        schedule1 = Schedule(common_course='CS3240', time=time1, location='Clemons')
        schedule1.save()

        schedule2 = Schedule(common_course='CS3102', time=time1, location='Alderman')
        schedule2.save()

        usertest1 = User.objects.create_user(username='user4444', password='password4444')
        usertest1.save()
        userprof1 = Profile(user=usertest1, id=1)
        userprof1.save()
        usertest2 = User.objects.create_user(username='user44445', password='password4444')
        usertest2.save()
        userprof2 = Profile(user=usertest2, id=2)
        userprof2.save()
        usertest3 = User.objects.create_user(username='user444456', password='password4444')
        usertest3.save()
        userprof3 = Profile(user=usertest3, id=3)
        userprof3.save()

        schedule1.study_buddies.add(userprof1)
        schedule1.study_buddies.add(userprof2)
        schedule1.study_buddies.add(userprof3)

        schedule2.study_buddies.add(userprof1)
        schedule2.study_buddies.add(userprof2)
        schedule2.study_buddies.add(userprof3)

        self.assertTrue(userprof1 in schedule1.study_buddies.all() and userprof2 in schedule1.study_buddies.all() and userprof3 in schedule1.study_buddies.all() and userprof1 in schedule2.study_buddies.all() and userprof2 in schedule2.study_buddies.all() and userprof3 in schedule2.study_buddies.all())




