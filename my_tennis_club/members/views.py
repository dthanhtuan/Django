from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Member
from .forms import MemberForm
import json


# ========== HTML VIEWS (CRUD Operations) ==========

def member_list(request):
    """
    INDEX - List all members
    Rails equivalent: MembersController#index
    """
    members = Member.objects.all()
    context = {'members': members}
    return render(request, 'members/index.html', context)


def member_detail(request, pk):
    """
    SHOW - Display single member
    Rails equivalent: MembersController#show
    """
    member = get_object_or_404(Member, pk=pk)
    context = {'member': member}
    return render(request, 'members/show.html', context)


def member_create(request):
    """
    NEW + CREATE - Show form and handle submission
    Rails equivalent: MembersController#new + MembersController#create

    Django combines both GET (show form) and POST (process form) in one view
    """
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Member {member} created successfully!')
            return redirect('members:detail', pk=member.pk)
    else:
        form = MemberForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'members/form.html', context)


def member_update(request, pk):
    """
    EDIT + UPDATE - Show form and handle submission
    Rails equivalent: MembersController#edit + MembersController#update

    Django combines both GET (show form) and POST (process form) in one view
    """
    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Member {member} updated successfully!')
            return redirect('members:detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)

    context = {'form': form, 'member': member, 'action': 'Update'}
    return render(request, 'members/form.html', context)


def member_delete(request, pk):
    """
    DELETE - Delete member
    Rails equivalent: MembersController#destroy

    Shows confirmation page on GET, deletes on POST
    """
    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':
        member_name = str(member)
        member.delete()
        messages.success(request, f'Member {member_name} deleted successfully!')
        return redirect('members:list')

    context = {'member': member}
    return render(request, 'members/confirm_delete.html', context)


# ========== AJAX/JSON API VIEWS ==========

def member_list_json(request):
    """
    API: List all members as JSON
    Rails equivalent: respond_to { |format| format.json { render json: @members } }
    """
    members = Member.objects.all()
    data = [{
        'id': m.pk,
        'firstname': m.firstname,
        'lastname': m.lastname,
        'email': m.email,
        'phone': m.phone,
        'joined_date': m.joined_date.isoformat()
    } for m in members]
    return JsonResponse({'members': data})


def member_detail_json(request, pk):
    """
    API: Get single member as JSON
    """
    try:
        member = Member.objects.get(pk=pk)
        data = {
            'id': member.pk,
            'firstname': member.firstname,
            'lastname': member.lastname,
            'email': member.email,
            'phone': member.phone,
            'joined_date': member.joined_date.isoformat()
        }
        return JsonResponse({'member': data})
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)


@require_http_methods(["POST"])
def member_create_json(request):
    """
    API: Create member via AJAX
    Rails equivalent: format.json { render json: @member, status: :created }
    """
    try:
        data = json.loads(request.body)
        member = Member.objects.create(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data.get('phone', '')
        )
        return JsonResponse({
            'success': True,
            'member': {
                'id': member.pk,
                'firstname': member.firstname,
                'lastname': member.lastname,
                'email': member.email
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST", "PUT", "PATCH"])
def member_update_json(request, pk):
    """
    API: Update member via AJAX
    """
    try:
        member = Member.objects.get(pk=pk)
        data = json.loads(request.body)

        member.firstname = data.get('firstname', member.firstname)
        member.lastname = data.get('lastname', member.lastname)
        member.email = data.get('email', member.email)
        member.phone = data.get('phone', member.phone)
        member.save()

        return JsonResponse({
            'success': True,
            'member': {
                'id': member.pk,
                'firstname': member.firstname,
                'lastname': member.lastname,
                'email': member.email
            }
        })
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST", "DELETE"])
def member_delete_json(request, pk):
    """
    API: Delete member via AJAX
    """
    try:
        member = Member.objects.get(pk=pk)
        member_data = {'id': member.pk, 'name': str(member)}
        member.delete()
        return JsonResponse({
            'success': True,
            'deleted': member_data
        })
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)