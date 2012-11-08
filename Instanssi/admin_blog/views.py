# -*- coding: utf-8 -*-

from common.http import Http403
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Instanssi.ext_blog.models import BlogEntry, BlogComment
from Instanssi.kompomaatti.models import Event
from Instanssi.admin_blog.forms import BlogEntryForm, BlogEntryEditForm
from Instanssi.admin_base.misc.custom_render import admin_render
from Instanssi.admin_base.misc.auth_decorator import staff_access_required
from datetime import datetime


@staff_access_required
def index(request, sel_event_id):
    # Post
    if request.method == 'POST':
        # Check for permissions
        if not request.user.has_perm('ext_blog.add_blogentry'):
            raise Http403
        
        # Handle form
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.event_id = int(sel_event_id)
            entry.date = datetime.now()
            entry.user = request.user
            entry.save()
            return HttpResponseRedirect(reverse('manage:blog', args=(sel_event_id)))
    else:
        form = BlogEntryForm()
    
    # Get events
    entries = BlogEntry.objects.filter(event_id = sel_event_id)
    
    # Render response
    return admin_render(request, "admin_blog/index.html", {
        'entries': entries,
        'selected_event_id': int(sel_event_id),
        'addform': form,
    })

@staff_access_required
def edit(request, sel_event_id, entry_id):
    # Check for permissions
    if not request.user.has_perm('ext_blog.change_blogentry'):
        raise Http403
    
    # Get old entry
    entry = get_object_or_404(BlogEntry, pk=entry_id)
    
    # Go ahead and edit
    if request.method == 'POST':
        form = BlogEntryEditForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage:blog', args=(sel_event_id)))
    else:
        form = BlogEntryEditForm(instance=entry)
    
    # Render response
    return admin_render(request, "admin_blog/edit.html", {
        'editform': form,
        'selected_event_id': int(sel_event_id),
    })
    
    
@staff_access_required
def delete(request, sel_event_id, entry_id):
    # Check for permissions
    if not request.user.has_perm('ext_blog.delete_blogentry'):
        raise Http403
    
    # Delete entry
    try:
        BlogEntry.objects.get(id=entry_id).delete()
    except BlogEntry.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('manage:blog', args=(sel_event_id)))
