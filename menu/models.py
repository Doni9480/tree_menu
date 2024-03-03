from django.db import models
from django.urls import reverse


class BaseAbstractModel(models.Model):
    """
    Базовая абстрактная модель.
    Обеспечивает параметры видимости, упорядочение и создание/обновление поля.
    """

    is_visible = models.BooleanField(default=True, verbose_name="Visibility")
    order = models.IntegerField(default=10, verbose_name="Order")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Menu(BaseAbstractModel):
    """
    Модель для пункта меню.
    Slug предназначен для использования в templatetag 'draw menu' для отображения меню
    """

    name = models.CharField("Название меню блока", max_length=120, unique=True)
    slug = models.SlugField(
        max_length=255,
        verbose_name="Slug",
        null=True,
        help_text="Будет использоватся в шаблоне для отображения меню",
    )
    named_url = models.CharField(
        max_length=255,
        verbose_name="Named URL",
        blank=True,
        help_text="Именованный url из файла urls.py",
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name

    def get_full_path(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = "/{}/".format(self.slug)
        return url


class MenuItem(BaseAbstractModel):
    """
    Модель для пункта меню.
    Поле 'menu' необходимо только для элементов верхнего уровня.
    Можно указать любой элемент в родительском поле, и он станет относительным для этого элемента.
    Если вы используете поле 'именованный url', метод get_url сначала будет использовать его для генерации url.
    И только тогда поле 'url'.
    """

    name = models.CharField("Название пункта меню", max_length=50, unique=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_items", null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name="Link", blank=True)
    named_url = models.CharField(
        max_length=255,
        verbose_name="Named URL",
        blank=True,
        help_text="Именованный url из файла urls.py",
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ("order",)

    def __str__(self):
        get_list = self.path_to_menu_item()[::-1]
        get_list[-1] = get_list[-1].upper()
        return " > ".join(get_list)

    def path_to_menu_item(self) -> list:
        list_names = []
        node = self
        while node is not None:
            list_names.append(node.name)
            node = node.parent
        return list_names

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            return "/"

        if url[0] != "/":
            url = f"/{url}"
        if url[-1] != "/":
            url = f"{url}/"
        return url
