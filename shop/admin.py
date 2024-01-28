from django.contrib import admin

from .models import Author,Book,Genre,Country,PublishingCompany,KeyWord,Comment,CommentOfComment
from markdownx.admin import MarkdownxModelAdmin

class KeyWordAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(KeyWord, KeyWordAdmin)

class PublishingCompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(PublishingCompany, PublishingCompanyAdmin)

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Author,AuthorAdmin)
#
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Genre,GenreAdmin)

class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Country,CountryAdmin)

admin.site.register(Comment)
admin.site.register(CommentOfComment)
admin.site.register(Book,MarkdownxModelAdmin)

