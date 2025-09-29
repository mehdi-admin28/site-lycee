from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home_name'),
    
    path('log-in0/',views.vue01login,name='loginname'),
    
    path('Users/',views.table_users,name='users_name'),
    path('Settings_admin/',views.settings_admin,name='settings_admin_name'),
    path('Sign-in_many/',views.sign_in_many,name='sign_in_many_name'),
    path('Name_change_request/',views.name_change,name='name_change_request'),
    path('Posting_news/',views.posting_news,name="posting_news_name"),
    path('Table_time/',views.table_time,name='table_time_name'),
    
    path('News/',views.news,name='news_name'),
    path('Profile/',views.profile,name='profile_name'), 
    path('Log-in/',views.log_in,name='log_in_name'),
    path('Certificat_admin/',views.certificat_admin0,name='certificat_admin_name'),
    path('Certificat/',views.certificat0,name='certificat_name'),
    
    path('Pub_admin/',views.pub_admin,name='pub_admin_name'),
    path('Pub/',views.pub1,name='pub_name'),
    path("messages/<int:group_id>/", views.messages_du_groupe, name="messages_du_groupe"),
    path('contact_us/',views.contact_us,name='contact_us_name'),
    path('contact_admin/',views.contact_admin,name='contact_admin_name'),
    path('documentation/',views.documentation ,name='documentation_name'),
    path('Messagerie/',views.messagerie,name='messagerie_name'),
    
    path("test-storage/", views.test_storage),
    path("Gallery/", views.galeryj ,name='gallery_name'),
    
    path("condition/", views.condition ,name='condition_name'),
    path("mention/", views.mention ,name='mention_name'),
    path("politique/", views.politique ,name='politique_name'),
]
  