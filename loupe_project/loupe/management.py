from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
 
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("corkboard_new_corkboard", _("New Corkboard"), _("a new corkboard was created"), default=1)
        notification.create_notice_type("corkboard_new_comment", _("New Corkboard Comment"), _("a new comment on a corkboard"), default=1)
        notification.create_notice_type("corkboard_new_image", _("New Image Uploaded"), _("a new image was uploaded"), default=2)
        notification.create_notice_type("corkboard_new_image_comment", _("New Image Comment"), _("a new comment on an image"), default=1)
        notification.create_notice_type("corkboard_new_image_note", _("New Image Note"), _("a new image note created"), default=1)
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
