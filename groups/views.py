from groups.forms import JoinForm
from django.shortcuts import redirect, render
from .models import Group
from events.models import Event
from django.contrib.auth.decorators import login_required


def groups(request):
    groups = Group.objects.all()
    context = {'groups':groups}
    return render(request, 'groups/groups.html',context)

def joinGroup(request,pk):
    group = Group.objects.get(id=pk)
    if group.members.filter(id=request.user.profile.id).exists():
        group.members.remove(request.user.profile)
    else:
        group.members.add(request.user.profile)
    return redirect('group',pk)


@login_required(login_url='/login')
def group(request, pk):
    form = JoinForm()
    user_obj= 0
    group_obj = Group.objects.get(id=pk)
    group = Group.objects.get(id=pk)
    group_events = Event.objects.filter(group=pk)
    user_obj = request.user.profile.id
    userMembership = group_obj.members.filter(id=user_obj).exists()

    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['group_status']
            if userMembership and not action:
                group_obj.members.remove(user_obj)
            elif not userMembership and action:
                group_obj.members.add(user_obj)

    context = {'group_obj':group_obj, 'group_events':group_events,'form':form,'group':group}

    return render(request,'groups/single-group.html', context)