from django.db import models


class Tweet(models.Model):
    id_str = models.CharField(blank=True, null=True, max_length=255, help_text="id of original tweet")
    status = models.CharField(blank=True, null=True, max_length=255, help_text="statud of the tweet, for example inactive")
    url = models.URLField(blank=True, null=True, help_text="url to original tweet")
    full_text = models.TextField(help_text="text-content of the tweet")
    labels_manual = models.TextField(blank=True, null=True, help_text="manually added labels")
    labels_automatic = models.TextField(blank=True, null=True, help_text="calculated labels")
    tweet_group = models.CharField(blank=True, null=True, max_length=255, help_text="additional parameter to group tweets")
    keywords = models.TextField(blank=True, null=True, help_text="keywords extracted from the tweet-text")
    content = models.TextField(blank=True, null=True, help_text="full content of the tweet as json, provided by the api")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.full_text[:20])


class Label(models.Model):
    label_name = models.CharField(max_length=255, help_text="name or reference to a label")
    label_group = models.CharField(max_length=255, blank=True, null=True, help_text="additional parameter to group labels")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.label_name, self.label_group,)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
