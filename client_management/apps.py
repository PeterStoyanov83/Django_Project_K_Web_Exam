from django.apps import AppConfig
from django.db.models.signals import post_migrate



class ClientManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_management'

    @staticmethod
    def create_default_site_profile(sender, **kwargs):
        """creating a default superuser after migrations"""
        from client_management.models import CustomUser

        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@admin.ad',
                password='admin123'
            )


    def ready(self):
        result=super().ready()

        post_migrate.connect(self.create_default_site_profile, sender=self)

        return result
