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
    LABEL_COLOR_CHOICES = [
            ('red_label',          'RED'),
            ('blue_label',         'BLUE'),
            ('green_label',        'GREEN'),
            ('yellow_label',       'YELLOW'),
            ('purple_label',       'PURPLE'),
            ('orange_label',       'ORANGE'),
            ('cyan_label',         'CYAN'),
            ('brown_label',        'BROWN'),
            ('lime_label',         'LIME'),
            ('olive_label',        'OLIVE'),
            ('teal_label',         'TEAL'),
            ('aqua_label',         'AQUA'),
            ('azure_label',        'AZURE'),
            ('bisque_label',       'BISQUE'),
            ('fuchsia_label',      'FUCHSIA'),
            ('chocolate_label',    'CHOCOLATE'),
            ('coral_label',        'CORAL'),
            ('darksalmon_label',   'DARKSALMOn'),
            ('darkseagreen_label', 'DARKSEAGReen'),
            ('deeppink_label',     'DEEPPINK'),
            ('goldenrod_label',    'GOLDENROD'),
            ('greenyellow_label',  'GREENYELLOW'),
            ]


    label_name = models.CharField(max_length=255, help_text="name or reference to a label")
    #label_group = models.CharField(max_length=255, blank=True, null=True, help_text="additional parameter to group labels")
    parent_label = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text="optional parameter to allow hierarchical labels")
    order = models.IntegerField(default=0, help_text="sorting order of lables displayed on the tool (left-right, top-bottom) starts with 0")

    label_color = models.CharField(max_length=64, choices=LABEL_COLOR_CHOICES, blank=True, null=True, help_text="color of the labels shown when label is selected")

    shortcut = models.CharField(max_length=1, blank=True, null=True, help_text="optional parameter for keyboard shortcut")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.label_name)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
