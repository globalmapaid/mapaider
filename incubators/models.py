from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Campaign(models.Model):
    name = models.CharField(_('campaign name'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80, unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this campaign should be treated as active. '
            'Unselect this instead of deleting campaigns.'
        ),
    )
    created_at = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
