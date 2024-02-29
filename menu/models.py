from django.db import models


class Menu(models.Model):
    name = models.CharField("Название меню блока", max_length=120, unique=True)
    description = models.TextField("Описание", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField("Название пункта меню", max_length=50, unique=True)
    description = models.TextField(
        "Описание пункта", max_length=300, null=True, blank=True
    )
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_items")

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.name
