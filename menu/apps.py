from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "menu"

    def ready(self):
        from django.db import OperationalError
        from django.contrib.auth.models import User
        try:
            from menu.models import Menu, MenuItem
            obj1 = Menu.objects.filter(name="group")
            if not obj1.count():
                obj1 = Menu(name="group", slug="main")
                obj1.save()
            else:
                obj1 = Menu.objects.get(name='group')

            obj2 = Menu.objects.filter(name="group2")
            if not obj2.count():
                obj2 = Menu(name="group2", slug="main")
                obj2.save()
            else:
                obj2 = Menu.objects.get(name='group2')
            
            for i in range(1, 6):
                if not MenuItem.objects.filter(name=f"item{i}").count():
                    if i < 7:
                        l1_obj = MenuItem(name=f"item{i}", menu=obj1, url="/" if i == 1 else f"item{i}")
                        l1_obj.save()
                    else:
                        slug = f"item{i}"
                        l1_obj = MenuItem(name=f"item{i}", menu=obj2, url=slug)
                        l1_obj.save()
                else:
                    l1_obj = MenuItem.objects.filter(name=f"item{i}")
                
                for j in range(1, 3):
                    if not MenuItem.objects.filter(name=f"item{i}.{j}").count():
                        if i < 7:
                            l2_obj = MenuItem(name=f"item{i}.{j}", parent=l1_obj, url=f"item{i}.{j}")
                            l2_obj.save()
                        else:
                            l2_obj = MenuItem(name=f"item{i}.{j}", parent=l2_obj, url=f"item{i}.{j}")
                            l2_obj.save()

            if not User.objects.filter(is_superuser=True).count():
                user=User.objects.create_user('admin', password='admin')
                user.is_superuser=True
                user.is_staff=True
                user.save()
        except OperationalError:
            from django.core import management
            management.call_command('migrate')
            self.ready()
