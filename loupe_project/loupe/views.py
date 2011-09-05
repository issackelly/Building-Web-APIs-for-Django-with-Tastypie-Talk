from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from loupe.models import Project, Image, Corkboard, Note
from loupe.forms import ImageForm, CorkboardForm, NoteForm, ProjectForm

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@login_required
def dashboard(request, template_name="loupe/dashboard.html"):
    """
    Displays the dashboard listing all of the corkboards and images
    that have been added as well as the form for adding new corkboards
    """
    projects = Project.objects.filter(members=request.user)
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.user, request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()
            request.user.message_set.create(message=_("Successfully created project '%s'") % project.title)
                
            return HttpResponseRedirect(reverse('project_detail', args=(project.slug,)))

    return render_to_response(template_name, {
        "projects": projects,
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def project_detail(request, slug, template_name="loupe/project_detail.html"):
    """
    Displays the corkboards for the given porject 'slug'
    to the user

    expects a slug and expects the user has access to the parent project
    """

    if not request.user.is_staff:
        project = get_object_or_404(Project, slug=slug, members=request.user)
    else:
        project = get_object_or_404(Project, slug=slug)

    corkboards = Corkboard.objects.filter(project=project)
    form = CorkboardForm()
    
    if request.method == "POST":
        form = CorkboardForm(request.user, request.POST)
        if form.is_valid():
            corkboard = form.save(commit=False)
            corkboard.user = request.user
            corkboard.project = project
            corkboard.save()
            request.user.message_set.create(message=_("Successfully created corkboard '%s'") % corkboard.title)

            if notification:
                notification.send_now(project.members.all(), "corkboard_new_corkboard", {"user": request.user, "corkboard": corkboard, "corkboard_url": corkboard.get_absolute_url})

            return HttpResponseRedirect(reverse('corkboard_detail', args=(corkboard.slug,)))
        
    return render_to_response(template_name, {
        "project": project,
        "form": form,
        "corkboards": corkboards,
    }, context_instance=RequestContext(request))

@login_required
def corkboard_detail(request, slug, template_name="loupe/corkboard_detail.html"):
    """
    Displays the corkboard and all it's associated images
    to the user

    expects a slug and expects the user has access to the parent project
    """

    if not request.user.is_staff:
        corkboard = get_object_or_404(Corkboard, slug=slug, project__members=request.user)
    else:
        corkboard = get_object_or_404(Corkboard, slug=slug)

    images = Image.objects.filter(corkboard=corkboard)

    form = ImageForm()
    
    if request.method == "POST":
        form = ImageForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.corkboard = corkboard
            image.save()
            if notification:
                notification.send_now(corkboard.project.members.all(), "corkboard_new_image", {"user": request.user, "corkboard": corkboard, "image_url": image.get_absolute_url, "corkboard_url": corkboard.get_absolute_url})

            request.user.message_set.create(message=_("Successfully uploaded image '%s'") % image.title)
            
    return render_to_response(template_name, {
        "corkboard": corkboard,
        "form": form,
        "images": images,
    }, context_instance=RequestContext(request))

@login_required
def image_detail(request, id, template_name="loupe/image_detail.html"):
    """
    Displays the image to be discussed by the project members

    expects an id for the image and the user has access to the parent project
    """
    if not request.user.is_staff:
        image = get_object_or_404(Image, pk=id, corkboard__project__members=request.user)
    else:
        image = get_object_or_404(Image, pk=id)

    notes = Note.objects.filter(image=image)
    notes_count = notes.count()
    form = NoteForm()

    if request.method == "POST":
        form = NoteForm(request.user, request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.image = image
            note.save()
            if notification:
                notification.send_now(image.corkboard.project.members.all(), "corkboard_new_image_note", {"user": request.user, "image_url": image.get_absolute_url, "image": image})
            request.user.message_set.create(message=_("Successfully attached note to image '%s'") % image.title)
                
    return render_to_response(template_name, {
        "image": image,
        "notes": notes,
        "notes_count": notes_count,
        "form": form,
    }, context_instance=RequestContext(request))


@require_POST
@login_required
def corkboard_destroy(request, id):
    """
    Deletes the corkboard passed in from the form
    """
    corkboard = get_object_or_404(Corkboard, pk=id)
    title = corkboard.title
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard'))

    corkboard.delete()
    request.user.message_set.create(message=_("Successfully deleted corkboard '%s'") % title)
    return HttpResponseRedirect(reverse('dashboard'))

@require_POST
@login_required
def image_destroy(request, id):
    """
    Deletes the corkboard passed in from the form
    """
    image = get_object_or_404(Image, pk=id)
    corkboard = image.corkboard
    title = image.title
    
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('dashboard'))

    image.delete()
    request.user.message_set.create(message=_("Successfully deleted image '%s'") % title)
    return HttpResponseRedirect(request.POST['next'])
