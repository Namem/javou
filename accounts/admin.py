from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Esta classe permite que o Perfil seja editado dentro da página do Usuário no admin.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'

# Define um novo User admin que inclui o nosso ProfileInline.
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-registra o User admin com a nossa versão customizada.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)