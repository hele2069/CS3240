from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, UpdateProfileCourseForm, ScheduleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.template import loader
from .models import Courses, Schedule, Profile
import datetime
import pytz
from chat.models import Room
from django.contrib.auth.models import User


def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'studybuddy/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def my_courses(request):
    # remove courses
    if request.method == "POST" and 'remove' in request.POST:
        course_id = request.POST.get("course_pk")
        course = Courses.objects.get(id=course_id)
        request.user.profile.courses.remove(course)
        messages.success(request, f'{course} removed from list.')
        return redirect(to='my_courses')

    return render(request, 'studybuddy/usercourses.html')  # {'course_form': course_form})


@login_required
def add_remove_courses(request):
    # add courses
    if request.method == "POST" and 'add' in request.POST:
        course_id = request.POST.get("course_pk")
        course = Courses.objects.get(id=course_id)
        print(request.user.profile.courses.__str__())
        request.user.profile.courses.add(course)
        messages.success(request, f'{course} added to list.')
        return redirect(to='my_courses')
    # remove courses
    elif request.method == "POST" and 'remove' in request.POST:
        course_id = request.POST.get("course_pk")
        course = Courses.objects.get(id=course_id)
        request.user.profile.courses.remove(course)
        messages.success(request, f'{course} removed from list.')
        return redirect(to='my_courses')
    elif request.method == "POST" and 'toggle_on' in request.POST:
        course_id = request.POST.get("course_pk")
        course = Courses.objects.get(id=course_id)
        request.user.profile.toggled_courses.add(course)
        messages.success(request, f'{course} will now appear in searches for a study buddy.')
        return redirect(to='my_courses')

    elif request.method == "POST" and 'toggle_off' in request.POST:
        course_id = request.POST.get("course_pk")
        course = Courses.objects.get(id=course_id)
        request.user.profile.toggled_courses.remove(course)
        messages.success(request, f'{course} will no longer appear in searches for a study buddy.')
        return redirect(to='my_courses')


@login_required
def search_courses(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        courses = Courses.objects.filter(subject__icontains=searched).order_by('number')
        return render(request, 'search_courses.html', {'searched': searched, 'courses': courses})
    else:
        return render(request, 'usercourses.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'studybuddy/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def course_list(request):
    return render(request, 'course_list.html')


    latest_question_list = Courses.objects.order_by('id')
    template = loader.get_template('course_list.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))

    # return render(request, 'course_list.html')

@login_required
def start_matching(request):
    print(request.user.profile.courses.all)
    # if request.method == "POST":
    #     searched = request.POST.get('searched', False)
    #     courses = Courses.objects.filter(subject__contains=searched)
    return render(request, 'start_matching.html')
    # else:
    #     return render(request, 'usercourses.html')

@login_required
def get_matches(request):
    # add courses
    unique_classmates = []
    for i in request.user.profile.toggled_courses.all():
        course = i
        for j in [x for x in course.profile_set.all() if x != request.user.profile]:
            if((i in j.toggled_courses.all()) and (j not in unique_classmates)):
                unique_classmates.append(j)
    template = loader.get_template('get_matches.html')
    context = {
        'unique_classmates': unique_classmates
    }

    return HttpResponse(template.render(context, request))

@login_required
def match_room(request):
    if request.method == 'POST':
        match_slug = request.user.username + request.POST.get('classmate')
        match_slug_rev = request.POST.get('classmate') + request.user.username
        if Room.objects.filter(slug=match_slug).exists():
            redirect_url = '/rooms/'+match_slug
            return redirect(to=redirect_url)
        elif Room.objects.filter(slug=match_slug_rev).exists():
            redirect_url = '/rooms/'+match_slug_rev
            return redirect(to=redirect_url)
        else:
            course_matches = []
            for i in request.user.profile.toggled_courses.all():
                for j in User.objects.filter(username=request.POST.get('classmate')):
                    for k in j.profile.toggled_courses.all():
                        if((i == k) and (i not in course_matches)):
                            course_matches.append(i)
            subjects = ""
            for i in course_matches:
                subjects = subjects+i.subject+" "+i.number+", "
            subjects = subjects[0:-2]
            new_room = Room.objects.create(
                name=subjects,
                slug=match_slug,
                description='Match: '+request.user.username+' & '+request.POST.get('classmate')+' Subject: '+subjects
            )
            redirect_url = '/rooms/'+match_slug
            return redirect(to=redirect_url)

@login_required
def schedule_class(request):
    if request.method == "POST" and 'schedule' in request.POST:
        print('hello')
        # course_id = request.POST.get("course_pk")
        # course = Courses.objects.get(id=course_id)
        # request.user.profile.courses.remove(course)
        # messages.success(request, f'{course} removed from list.')
        return render(request, 'studybuddy/usercourses.html')  # {'course_form': course_form})



    return render(request, 'studybuddy/usercourses.html')  # {'course_form': course_form})
@login_required
def schedule_view(request):
    # if request.method == "POST" and 'classmates' in request.POST:
    #     print(request.POST.get("classmates"))
    # classmate = request.POST.get("classmate")
    # print(classmate)
    # clminit = ""
    # for i in request.user.profile.toggled_courses.all():
    #     if(not(clminit == "")):
    #         break
    #     course=i
    #     for j in [x for x in course.profile_set.all() if x != request.user.profile]:
    #         if(str(j)==classmate):
    #             clminit = j
    #             break

    
    data = {'study_buddies': request.user.profile}
    form = ScheduleForm(request.POST or None, initial = data)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting was successfully scheduled!')
            return redirect(to='schedule')
    context = {
        'form': form,
    }
    return render(request, "schedule_create.html", context)
@login_required
def schedule(request):
    if request.method == "POST" and 'remove_meeting' in request.POST:
        meeting_id = request.POST.get("meeting_pk")
        meeting = Schedule.objects.get(id=meeting_id)
        meeting.delete()
        # request.user.profile.schedule_set.all().remove(meeting)
        messages.success(request, f'Meeting removed.')
        return redirect(to='schedule')
    # print()
    utc = pytz.UTC
    current_date = datetime.datetime.today()
    current_date = utc.localize(current_date)
    all_meetings = request.user.profile.schedule_set.all()
    for i in range(len(all_meetings)):
        if(all_meetings[i].time<current_date):
            all_meetings[i].delete()

    meetings = request.user.profile.schedule_set.all().order_by('time')
    # print(meetings[0].id)
    context = {
        'meetings': meetings,
    }
    return render(request, "schedule.html", context)
