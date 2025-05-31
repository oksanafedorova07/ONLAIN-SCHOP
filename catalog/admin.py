from django.contrib import admin
from django.utils.safestring import mark_safe


from catalog.models import Category, Product, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}

    def description_short(self, obj):
        return f"{obj.description[:50]}..." if obj.description else ""

    description_short.short_description = "Описание"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "created_at")  # Добавлено "id"
    list_display_links = ("id", "name")  # Делаем ID и название кликабельными
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "category")}),
        ("Детали", {"fields": ("description", "photo", "price")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')



