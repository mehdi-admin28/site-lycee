import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet01.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("Mehdi_Admin", "mehdi.chek6514@gmail.com", "impossible0")
    print("✅ Superuser créé avec succès !")
else:
    print("⚠️ Le superuser existe déjà.")
