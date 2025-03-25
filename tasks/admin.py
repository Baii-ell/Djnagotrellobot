from django.contrib import admin
from .models import User, Card, Task





@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )  
    search_fields = ('name',)



@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)




@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'card', 'done', 'created_at')
    search_fields = ('title',)
    list_filter = ('done', 'created_at')
