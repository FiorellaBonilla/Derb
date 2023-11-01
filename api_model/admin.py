from django.contrib import admin

from api_model.models import Person, Room, Pet, Descriptor

# Register your models here.
admin.site.register(Person)
admin.site.register(Room)
admin.site.register(Pet)
admin.site.register(Descriptor)