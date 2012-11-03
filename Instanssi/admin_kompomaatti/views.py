# -*- coding: utf-8 -*-

from common.http import Http403
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from Instanssi.dbsettings.models import Setting
from Instanssi.kompomaatti.models import Compo,Entry,VoteCodeRequest,VoteCode,Event,Competition,CompetitionParticipation
from Instanssi.admin_kompomaatti.forms import *
from Instanssi.admin_base.misc.custom_render import admin_render
from Instanssi.kompomaatti.misc import entrysort

# For votecode stuff
from django.db import IntegrityError
from datetime import datetime
import random
import hashlib
    
# For generating a paper version of votecodes
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def index(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Render response
    return admin_render(request, "admin_kompomaatti/index.html", {
        'selected_event_id': int(sel_event_id),
    })

@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competition_score(request, sel_event_id, competition_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get competition
    competition = get_object_or_404(Competition, pk=competition_id)
    
    # Handle form
    if request.method == 'POST':
        # Check permissions
        if not request.user.has_perm('kompomaatti.change_competitionparticipation'):
            raise Http403
        
        # Handle form
        scoreform = AdminCompetitionScoreForm(request.POST, competition=competition)
        if scoreform.is_valid():
            scoreform.save()
            return HttpResponseRedirect(reverse('admin-competitions', args=(sel_event_id))) 
    else:
        scoreform = AdminCompetitionScoreForm(competition=competition)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/competition_score.html", {
        'competition': competition,
        'scoreform': scoreform,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competition_participations(request, sel_event_id, competition_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get competition
    participants = CompetitionParticipation.objects.filter(competition_id=int(competition_id))
    
    # Render response
    return admin_render(request, "admin_kompomaatti/competition_participations.html", {
        'participants': participants,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competition_participation_edit(request, sel_event_id, competition_id, pid):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.change_competitionparticipation'):
        raise Http403
    
    # Get competition, participation
    competition = get_object_or_404(Competition, pk=int(competition_id))
    participant = get_object_or_404(CompetitionParticipation, pk=int(pid))
    
    # Handle form
    if request.method == 'POST':
        pform = AdminParticipationEditForm(request.POST, instance=participant)
        if pform.is_valid():
            pform.save()
            return HttpResponseRedirect(reverse('admin-participations', args=(sel_event_id)))
    else:
        pform = AdminParticipationEditForm(instance=participant)
    
    
    # Render response
    return admin_render(request, "admin_kompomaatti/participation_edit.html", {
        'pform': pform,
        'selected_event_id': int(sel_event_id),
        'competition': competition,
    })
    
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competitions_browse(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get competitions
    competitions = Competition.objects.filter(event_id=int(sel_event_id))
    
    # Form handling
    if request.method == "POST":
        # CHeck for permissions
        if not request.user.has_perm('kompomaatti.add_competition'):
            raise Http403
        
        # Handle form
        competitionform = AdminCompetitionForm(request.POST)
        if competitionform.is_valid():
            data = competitionform.save(commit=False)
            data.event_id = int(sel_event_id)
            data.save()
            return HttpResponseRedirect(reverse('admin-competitions', args=(sel_event_id))) 
    else:
        competitionform = AdminCompetitionForm()
    
    # Render response
    return admin_render(request, "admin_kompomaatti/competitions.html", {
        'competitions': competitions,
        'competitionform': competitionform,
        'selected_event_id': int(sel_event_id),
        'LANGUAGE_CODE': getattr(settings, 'SHORT_LANGUAGE_CODE'),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competition_edit(request, sel_event_id, competition_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.change_competition'):
        raise Http403
    
    # Get competition
    competition = get_object_or_404(Competition, pk=competition_id)
    
    # Handle form
    if request.method == "POST":
        competitionform = AdminCompetitionForm(request.POST, instance=competition)
        if competitionform.is_valid():
            competitionform.save()
            return HttpResponseRedirect(reverse('admin_competitions', args=(sel_event_id))) 
    else:
        competitionform = AdminCompetitionForm(instance=competition)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/competition_edit.html", {
        'competition': competition,
        'competitionform': competitionform,
        'selected_event_id': int(sel_event_id),
        'LANGUAGE_CODE': getattr(settings, 'SHORT_LANGUAGE_CODE'),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def competition_delete(request, sel_event_id, competition_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.delete_competition'):
        raise Http403
    
    # Delete competition
    try:
        Competition.objects.get(pk=competition_id).delete()
    except:
        pass
    
    # Redirect
    return HttpResponseRedirect(reverse('admin-competitions', args=(sel_event_id))) 
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def compo_browse(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get compos
    compos = Compo.objects.filter(event_id=int(sel_event_id))
    
    # Form handling
    if request.method == "POST":
        # CHeck for permissions
        if not request.user.has_perm('kompomaatti.add_compo'):
            raise Http403
        
        # Handle form
        compoform = AdminCompoForm(request.POST)
        if compoform.is_valid():
            data = compoform.save(commit=False)
            data.event_id = int(sel_event_id)
            data.save()
            return HttpResponseRedirect(reverse('admin-compos', args=(sel_event_id))) 
    else:
        compoform = AdminCompoForm()
    
    # Render response
    return admin_render(request, "admin_kompomaatti/compo_browse.html", {
        'compos': compos,
        'compoform': compoform,
        'LANGUAGE_CODE': getattr(settings, 'SHORT_LANGUAGE_CODE'),
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def compo_edit(request, sel_event_id, compo_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.change_compo'):
        raise Http403
    
    # Get compo
    compo = get_object_or_404(Compo, pk=compo_id)
    
    # Handle form
    if request.method == "POST":
        editform = AdminCompoForm(request.POST, instance=compo)
        if editform.is_valid():
            editform.save()
            return HttpResponseRedirect(reverse('admin-compos', args=(sel_event_id))) 
    else:
        editform = AdminCompoForm(instance=compo)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/compo_edit.html", {
        'compo': compo,
        'editform': editform,
        'selected_event_id': int(sel_event_id),
        'LANGUAGE_CODE': getattr(settings, 'SHORT_LANGUAGE_CODE'),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def compo_delete(request, sel_event_id, compo_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.delete_compo'):
        raise Http403
    
    # Delete competition
    try:
        Compo.objects.get(pk=compo_id).delete()
    except:
        pass
    
    # Redirect
    return HttpResponseRedirect(reverse('admin-compos', args=(sel_event_id))) 
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def entry_browse(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get event
    event = get_object_or_404(Event, pk=sel_event_id)
    
    # Form handling
    if request.method == "POST":
        # CHeck for permissions
        if not request.user.has_perm('kompomaatti.add_entry'):
            raise Http403
        
        # Handle form
        entryform = AdminEntryAddForm(request.POST, request.FILES, event=event)
        if entryform.is_valid():
            entryform.save()
            return HttpResponseRedirect(reverse('admin-entries', args=(sel_event_id))) 
    else:
        entryform = AdminEntryAddForm(event=event)
    
    # Get Entries    
    compos = Compo.objects.filter(event=int(sel_event_id))
    entries = Entry.objects.filter(compo__in=compos)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/entry_browse.html", {
        'entries': entries,
        'entryform': entryform,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def entry_edit(request, sel_event_id, entry_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.change_entry'):
        raise Http403
    
    # Check ID
    entry = get_object_or_404(Entry, pk=entry_id)
    
    # Get event
    event = get_object_or_404(Event, pk=sel_event_id)
    
    # Handle form
    if request.method == "POST":
        editform = AdminEntryEditForm(request.POST, request.FILES, instance=entry, event=event)
        if editform.is_valid():
            editform.save()
            return HttpResponseRedirect(reverse('admin-entries', args=(sel_event_id))) 
    else:
        editform = AdminEntryEditForm(instance=entry, event=event)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/entry_edit.html", {
        'entry': entry,
        'editform': editform,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def entry_delete(request, sel_event_id, entry_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.delete_entry'):
        raise Http403
    
    # Delete competition
    try:
        Entry.objects.get(pk=entry_id).delete()
    except:
        pass
    
    # Redirect
    return HttpResponseRedirect(reverse('admin-entries', args=(sel_event_id))) 
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def results(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get compos. competitions
    compos = Compo.objects.filter(event_id=int(sel_event_id))
    competitions = Competition.objects.filter(event_id=int(sel_event_id))

    # Get the entries
    compo_results = {}
    for compo in compos:
        compo_results[compo.name] = entrysort.sort_by_score(Entry.objects.filter(compo=compo))
    
    # Get competition participations
    competition_results = {}
    for competition in competitions:
        rankby = '-score'
        if competition.score_sort == 1:
            rankby = 'score'
        competition_results[competition.name] = CompetitionParticipation.objects.filter(competition=competition).order_by(rankby)
    
    # Render response
    return admin_render(request, "admin_kompomaatti/results.html", {
        'compo_results': compo_results,
        'competition_results': competition_results,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def votecodes(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
        
    # Handle form
    if request.method == 'POST':
        # CHeck for permissions
        if not request.user.has_perm('kompomaatti.add_votecode'):
            raise Http403
        
        # Handle form
        gentokensform = CreateTokensForm(request.POST)
        if gentokensform.is_valid():
            amount = int(gentokensform.cleaned_data['amount'])
            for n in range(amount):
                try:
                    c = VoteCode()
                    c.event_id = int(sel_event_id)
                    c.key = unicode(hashlib.md5(str(random.random())).hexdigest()[:8])
                    c.save()
                except IntegrityError:
                    n = n-1 # Ugly, may cause infinite loop...
            return HttpResponseRedirect(reverse('admin-votecodes', args=(sel_event_id))) 
    else:
        gentokensform = CreateTokensForm()
        
    # Get tokens
    tokens = VoteCode.objects.filter(event_id=int(sel_event_id))
    
    # Render response
    return admin_render(request, "admin_kompomaatti/votecodes.html", {
        'tokens': tokens,
        'gentokensform': gentokensform,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def votecodes_print(request, sel_event_id):
    # Make sure the user is superuser.
    if not request.user.is_staff:
        raise Http403
    
    # Get free votecodes
    codes = VoteCode.objects.filter(event_id=int(sel_event_id), associated_to=None)
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=votecodes.pdf'

    # Create the PDF object,
    p = canvas.Canvas(response)
    p.setAuthor(u"Kompomaatti")
    p.setTitle(u"Äänestyskoodeja")
    p.setFont("Helvetica-Oblique", 18)

    # Print codes
    height = 0
    step = 2.12*cm
    perpage = 14
    codeno = 0
    for code in codes:
        p.line(0,height,21*cm,height)
        p.drawString(1*cm, height+0.8*cm, u"Äänestyskoodi: "+code.key)
        height += step
        codeno += 1
        if codeno >= perpage:
            p.showPage()
            p.setFont("Helvetica-Oblique", 18)
            height = 0
            codeno = 0
    p.showPage()

    # Close the PDF object & dump out the response
    p.save()
    return response
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def votecoderequests(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http403
    
    # Get all requests
    requests = VoteCodeRequest.objects.filter(event_id=int(sel_event_id))
    
    # Render response
    return admin_render(request, "admin_kompomaatti/vcrequests.html", {
        'requests': requests,
        'selected_event_id': int(sel_event_id),
    })
    
@login_required(login_url=getattr(settings, 'ADMIN_LOGIN_URL'))
def votecoderequests_accept(request, sel_event_id, vcrid):
    # Make sure the user is staff
    if not request.user.is_staff:
        raise Http403
    
    # CHeck for permissions
    if not request.user.has_perm('kompomaatti.change_votecode'):
        raise Http403
    
    # Get the request
    vcr = get_object_or_404(VoteCodeRequest, pk=vcrid)
        
    # Add votecode for user. Bang your head to the wall until you succeed, etc.
    # TODO: Do something about this shit!
    done = False
    for i in range(25):
        try:
            c = VoteCode()
            c.event_id = int(sel_event_id)
            c.key = unicode(hashlib.md5(str(random.random())).hexdigest()[:8])
            c.associated_to = vcr.user
            c.time = datetime.now()
            c.save()
            done = True
            break;
        except IntegrityError:
            pass
    
    if not done:
        return HttpResponse("Virhe yritettäessä lisätä satunnaista avainta ... FIXME!")
            
    # Delete request
    vcr.delete()
    
    # Return to admin page
    return HttpResponseRedirect(reverse('admin-votecoderequests', args=(sel_event_id))) 
