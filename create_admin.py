'''
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet01.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    yo = User.objects.create_superuser("Mehdi_Admin0", "mehdi.chek6514@gmail.com", "impossible0")
    yo.profile.badge = "admin"
    yo.profile.save()
    print("✅ Superuser créé avec succès !")
else:
    print("⚠️ Le superuser existe déjà.")
'''