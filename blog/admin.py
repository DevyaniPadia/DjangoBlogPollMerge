from django.contrib import admin
from .models import Post, Category, Comment, User, Tag
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin
import csv
admin.site.register(Category)
admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text','published_date','thumbnailimage','was_published_recently')
    list_filter = ['published_date']
    search_fields = ['title', 'text']
    
    def viewonsite(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active','reply')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    
admin.site.register(Comment,CommentAdmin)


class UserProfileAdmin(UserAdmin):
    fieldsets=[
        (None,             {'fields': ['first_name','last_name','email','city','state','country','mobile_no','profile_img']})

    ]
    
    actions = ("export_as_csv",)
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
    
admin.site.register(User, UserProfileAdmin)