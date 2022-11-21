from django.contrib import admin
from .models import (
    MainEntity,
    Actor,
    SerialRole,
    Anime
)


class MainEntityAdmin(admin.ModelAdmin):
    model = MainEntity

    fieldsets = (
        ('Information', {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'apartment_number',
            )
        }),
        ('Permissions', {
            'fields': (
                'has_paid_taxes',
                'datetime_created',
                'datetime_updated',
                'datetime_deleted',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
        }),
    )

    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'apartment_number',
    )
    search_fields = (
        'first_name',
    )
    list_filter = (
        'first_name',
        'has_paid_taxes',
    )
    ordering = (
        'first_name',
    )
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
    )

class ActorsAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'first_appearance_in_serial',
    )
    list_filter = (
        'serial_role',
        'date_birthday',
    )


class SerialRoleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'bad_or_good',
        'main_person',
    )
    list_filter = (
        'name',
        'main_person',
    )

class AnimeAdmin(admin.ModelAdmin):

    list_display = (
        'studio',
        'rating',
    )
    list_filter = (
        'start_date',
    )


admin.site.register(MainEntity, MainEntityAdmin)
admin.site.register(Actor, ActorsAdmin)
admin.site.register(SerialRole, SerialRoleAdmin)
admin.site.register(Anime, AnimeAdmin)


