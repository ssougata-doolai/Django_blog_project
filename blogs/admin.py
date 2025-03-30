from django.contrib import admin
from . models import Post, Comment, PostPreference, CommentPreference, PostReport

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    search_fields = ['title','text']
    list_display = ['title','author','created_date','published_date','likes','dislikes','edited','thumbnail']
#    readonly_fields = []
#    list_filter = []
#    list_display_links = ['author']
    list_editable = ['edited']
#    prepopulated_fields = {}

    class Meta:
        model = Post


class PostReportAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['feedback','feedback_text','date','post','user']

    class Meta:
        model = PostReport

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostPreference)
admin.site.register(CommentPreference)
admin.site.register(PostReport, PostReportAdmin)
