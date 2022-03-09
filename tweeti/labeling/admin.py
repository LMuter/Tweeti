from django.contrib import admin
from .models import Tweet, Label, Document


def finalize_tweets(modeladmin, request, queryset):
    queryset.update(status='final')
finalize_tweets.short_description = "Finalize tweets"


def exclude_tweets(modeladmin, request, queryset):
    queryset.update(status='excluded')
exclude_tweets.short_description = "Exclude tweets"


def activate_tweets(modeladmin, request, queryset):
    queryset.update(status='full_text, active')
activate_tweets.short_description = "Activate tweets"


def discuss_tweets(modeladmin, request, queryset):
    queryset.update(status='discuss')
discuss_tweets.short_description = "Discuss tweets"


class TweetAdmin(admin.ModelAdmin):
    fields = ['id', 'id_str', 'status', 'url', 'full_text', 'labels_manual', 'labels_automatic', 'tweet_group', 'keywords', 'content', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ('id', 'id_str', 'status', 'full_text', 'labels_manual', 'created_at', 'updated_at')
    search_fields = ['id', 'id_str', 'status', 'full_text', 'labels_manual', 'labels_automatic', 'keywords']
    actions = [finalize_tweets, exclude_tweets, activate_tweets, discuss_tweets]
    list_filter = ['status']


class LabelAdmin(admin.ModelAdmin):
    fields = ['label_name', 'parent_label', 'order', 'label_color', 'shortcut', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display = ('label_name', 'parent_label', 'order', 'label_color', 'shortcut', 'created_at', 'updated_at')


class DocumentAdmin(admin.ModelAdmin):
    fields = ['description', 'document', 'uploaded_at']
    readonly_fields = ['document', 'uploaded_at']
    list_display = ('description', 'uploaded_at')


admin.site.register(Tweet, TweetAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Document, DocumentAdmin)
