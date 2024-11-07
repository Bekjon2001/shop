from django.contrib import admin

from apps.users.models import CustomUser,Permission

@admin.register(Permission)
class AdminPermission(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.password != CustomUser.objects.get(pk=obj.pk).password:
            obj.set_password(obj.password)
        obj.save()


