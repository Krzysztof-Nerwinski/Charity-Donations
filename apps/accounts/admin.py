from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db.models import Case, When, Value
from .forms import CustomRegistrationForm, CustomAdminUserChangeForm
from .models import CustomUser


def change_is_active_status(modeladmin, request, queryset):
    queryset.update(is_active=Case(
        When(is_active=True, then=Value(False)),
        When(is_active=False, then=Value(True))
    ))


def change_is_staff_status(modeladmin, request, queryset):
    queryset.update(is_staff=Case(
        When(is_staff=True, then=Value(False)),
        When(is_staff=False, then=Value(True))
    ))


change_is_active_status.short_description = _('Zmień aktywność dla wybranych użytkowników')
change_is_staff_status.short_description = _('Zmień status zespołu dla wybranych użytkowników')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    min_admins_number = 2
    message_min_admins_number = _('Nie można usunąć części zaznaczonych userów. '
                                  'Na stronie musi pozostać co najmniej {} superuser/(ów)').format(min_admins_number)
    # list view
    actions = [change_is_active_status, change_is_staff_status]
    list_display = ['username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
    # add view
    add_form = CustomRegistrationForm
    add_fieldsets = (
        (_('Informacje o użytkowniku'), {'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}),
        (_('Uprawnienia'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    # change view
    form = CustomAdminUserChangeForm
    fieldsets = (
        (_('Informacje osobiste'), {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        (_('Uprawnienia'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # don't allow single admin object removal when less admins than min_admins_number
    def has_delete_permission(self, request, obj=None):
        adminset = self.model.objects.filter(is_superuser=True)
        if obj and obj.is_superuser and (adminset.count() <= self.min_admins_number):
            self.message_user(request, self.message_min_admins_number, messages.ERROR)
            return False
        return super(CustomUserAdmin, self).has_delete_permission(request, obj)

    # when using delete selected action remove admins from selection or stop action
    def response_action(self, request, queryset):
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
        admins = self.model.objects.filter(is_superuser=True)
        admins_pks = admins.values_list('pk', flat=True)
        admins_in_selected = [pk_num for pk_num in admins_pks if str(pk_num) in selected]
        admins_left = admins.count() - len(admins_in_selected)
        data = request.POST.copy()
        delete_action = data['action'] == 'delete_selected'
        enough_admins_left = admins_left >= self.min_admins_number
        if delete_action and admins_in_selected and not enough_admins_left:
            for pk_num in admins_in_selected:
                selected.remove(str(pk_num))
            if len(selected) > 0:
                func = self.get_actions(request)[data['action']][0]
                queryset = self.model.objects.filter(pk__in=selected)
                self.message_user(request, self.message_min_admins_number, messages.ERROR)
                return func(self, request, queryset)
            else:
                self.message_user(request, self.message_min_admins_number, messages.ERROR)
        else:
            return super(CustomUserAdmin, self).response_action(request, queryset)
