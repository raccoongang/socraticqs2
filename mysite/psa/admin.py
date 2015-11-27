from django.contrib import admin

from psa.models import UserSession, AnonymEmail, SecondaryEmail, TokenForgotPassword


@admin.register(SecondaryEmail)
class SecondaryEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'provider')


@admin.register(TokenForgotPassword)
class TokenForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'next_url', 'created')


admin.site.register(UserSession)
admin.site.register(AnonymEmail)
