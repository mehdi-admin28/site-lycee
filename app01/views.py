from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms01 import Form01, Form02
from .models import Matiere, Message, Groupe, contact01, Filiere01, classe01, changement_nom_prernom, posts, pub0, emplous_temps, certificat
import ast
import random
from urllib.parse import unquote
import json
from datetime import date
from django.core.paginator import Paginator
from django.core.cache import cache
import time
'''from django.db.models import Prefetch'''
from django.http import HttpResponse
from django.core.files.storage import default_storage



# Variables globales supprimées - elles seront chargées via le cache ou des requêtes optimisées

limite = False
contact_chance = 0
redx = "bloque"
redy = "bloque"
dm_pub312 = 0


def test_storage(request):
    
    return HttpResponse(str(default_storage.__class__))


def get_cached_data(key, queryset, timeout=300):
    """Helper function to get cached data or set it if not exists"""
    data = cache.get(key)
    if data is None:
        data = list(queryset)
        cache.set(key, data, timeout)
    return data


def langue_fonction(request):
    langue = "en"
    form = request.POST.get('quelform')
    '''
        if form == "languefr":
            langue ="fr"
        if form == "languear":
            langue ="ar"
        if form == "languean":
            langue = "en"
    '''
    if request.user.is_authenticated:
        z = request.user.profile.dm
        t = list(z)
        for i in t:
            if i == "A":
                langue = "ar"
                break
            elif i == "E":
                langue = "en"
                break
            elif i == "F":
                langue = "fr"
                break

    if form == "languefr":
        if request.user.is_authenticated:
            x = request.user.username
            y = User.objects.get(username=x)
            z = y.profile.dm
            t = list(z)
            for i in t:
                if i == "A" or i == "E":
                    t.remove(i)
                else:
                    continue
            t.append("F")
            t = "".join(t)
            y.profile.dm = t
            y.profile.save()
            langue = "fr"
        else:
            langue = "fr"
        
    elif form == "languear":
        if request.user.is_authenticated:
            x = request.user.username
            y = User.objects.get(username=x)
            z = y.profile.dm
            t = list(z)
            for i in t:
                if i == "E" or i == "F":
                    t.remove(i)
                else:
                    continue
            t.append("A")
            t = "".join(t)
            y.profile.dm = t
            y.profile.save()
            langue = "ar"
        else:
            langue = "ar"
        
    elif form == "languean":
        if request.user.is_authenticated:
            x = request.user.username
            y = User.objects.get(username=x)
            z = y.profile.dm
            t = list(z)
            for i in t:
                if i == "A" or i == "F":
                    t.remove(i)
                else:
                    continue
            t.append("E")
            t = "".join(t)
            y.profile.dm = t
            y.profile.save()
            langue = "en"
        else:
            langue = "en"
    
    return langue


def home(request):
    # Utilisation du cache pour les données fréquemment accédées
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    e15 = get_cached_data('prof_users', User.objects.filter(profile__badge="prof").select_related('profile'))
    
    langue = langue_fonction(request)
    u17 = ""
    titreu17 = ""
    a = ""
    b = ""
    c = ""
    d = ""
    e = ""
    f = ""
    g = ""
    
    # Chargement optimisé des posts avec prefetch
    p03 = get_cached_data('all_posts', posts.objects.all()[:50])
    
    nomjjj = ""
    
    if request.user.is_authenticated:
        a = request.user.first_name + " " + request.user.last_name
        b = request.user.profile.classe
        c = request.user.profile.badge
        d = request.user.profile.matiere
        e = request.user.profile.heure_de_reception
        f = request.user.profile.badge
        g = request.user.first_name
        
        classe = request.user.profile.classe
        
        # Remplacement du next() par une requête directe
        try:
            post_trouve = posts.objects.filter(titre=classe).first()
            if post_trouve:
                u17 = post_trouve.text
                titreu17 = post_trouve.titre
        except:
            u17 = ""
            titreu17 = ""
            
        if request.user.is_superuser or request.user.username == "Mehdi_Admin":
            nomjjj = "oui"
    
    return render(request, 'home.html', {
        'name': a,
        'classe': b,
        'badge': c,
        'matiere': d,
        'heures_de_reception': e,
        'posts': p03,
        'titre_emplois': titreu17,
        'mon_emplois': u17,
        'pubs': pubs,
        'profs': e15,
        'is_auth': request.user.is_authenticated,
        'is_admin': f,
        'langue': langue,
        'name2': g,
        'nomjjj': nomjjj,
    })


def vue01login(request):
    if request.method == 'POST':
        username0 = request.POST.get('username')
        password0 = request.POST.get('password')
        user = authenticate(request, username=username0, password=password0)
        if user:
            login(request, user)
            return redirect('home_name')
    
    return render(request, 'login.html')
   

def table_users(request):
    langue = langue_fonction(request)
    liste404 = []
    resultat = ""
    eleve_est_la = ""
    prof_est_la = ""
    admin_est_la = ""
    a = ""
    b = ""
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
        b = request.user.username
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form == "form_recuper_id_selected":
            resultat = request.POST.get('resultat01')
            resultat = resultat.split('-')
            resultat.pop(0)
            
            for i in resultat:
                user_suppr = User.objects.filter(id=i).first()
                if user_suppr:
                    liste404.append(f"{user_suppr.first_name} {user_suppr.last_name}")
                    user_suppr.delete()
            
            resultat = "liste 404 n est pas vide"
            
        elif form == "form_ajou_eleve":
            abc = ""
            ln = request.POST.get('last_name01')
            fn = request.POST.get('first_name01')
            cl = request.POST.get('slct_classe03')
            mdp_eleve = str(random.randint(1000, 1000000))
            username_eleve = f"{ln} {fn}"
            username_eleve = username_eleve.split(" ")
            
            for i in username_eleve:
                if i.isalpha():
                    continue
                else:
                    abc = "pasabc"
                    break
                
            if abc != "pasabc":
                username_eleve = "_".join(username_eleve)
                user0 = User.objects.filter(last_name=ln, first_name=fn).exists()
                if not user0:
                    user = User.objects.create_user(username=username_eleve, password=mdp_eleve, last_name=ln, first_name=fn)
                    user.profile.classe = cl
                    user.profile.badge = "eleve"
                    user.profile.password = mdp_eleve
                    user.profile.save()
                    # Invalider le cache après modification
                    cache.delete('all_users')
                else:
                    eleve_est_la = "y"
            else:
                eleve_est_la = "n"
                                
        elif form == "form_ajou_prof":
            ab = ""
            ln = request.POST.get('last_name_prof')
            fn = request.POST.get('first_name_prof')
            mtr_selected = request.POST.get('slct_mtr03')
            mdp_prof = str(random.randint(1000, 1000000))
            username_prof = f"{ln} {fn}"
            username_prof = username_prof.split(" ")
            
            for i in username_prof:
                if i.isalpha():
                    continue
                else:
                    ab = "ab"
                    break
            
            if ab != "ab":
                username_prof = "_".join(username_prof)
                
                user0 = User.objects.filter(last_name=ln, first_name=fn).exists()
                if not user0:
                    user = User.objects.create_user(username=username_prof, password=mdp_prof, last_name=ln, first_name=fn)
                    user.profile.badge = "prof"
                    user.profile.password = mdp_prof
                    user.profile.matiere = mtr_selected
                    user.profile.save()
                    cache.delete('all_users')
                    cache.delete('prof_users')
                else:
                    prof_est_la = "y"
            else:
                prof_est_la = "n"

        elif form == "form_ajou_administration":
            abd = ""
            ln = request.POST.get('last_name_adm')
            fn = request.POST.get('first_name_adm')
            mdp_adm = request.POST.get('mdp_adm')
            username_adm = f"{ln} {fn}"
            username_adm = username_adm.split(" ")
            
            for i in username_adm:
                if i.isalpha():
                    continue
                else:
                    abd = "abd"
            
            if abd != "abd":
                username_adm = "_".join(username_adm)
            
                user0 = User.objects.filter(first_name=fn, last_name=ln).exists()
                if not user0:
                    user = User.objects.create_user(username=username_adm, password=mdp_adm, first_name=fn, last_name=ln)
                    user.profile.badge = "admin"
                    user.profile.password = mdp_adm
                    user.profile.save()
                    cache.delete('all_users')
                else:
                    admin_est_la = "y"
            else:
                admin_est_la = "n"
        
        elif form == "form_suppr_tout_eleve":
            User.objects.filter(profile__badge="eleve").delete()
            User.objects.filter(profile__badge="pas de badge !").delete()
            cache.delete('all_users')
            
        elif form == "securiser admin":
            for i in User.objects.filter(profile__badge="admin"):
                i.profile.password = "security"
                i.profile.save()
                
        elif form == "securiser":
            for i in User.objects.all():
                i.profile.password = "security"
                i.profile.save()
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement optimisé avec pagination et cache
    tous_les_utilisateurs = get_cached_data('all_users', 
        User.objects.all().select_related('profile').order_by('id'))
    
    '''
    paginateur = Paginator(tous_les_utilisateurs, 50)
    numero_page = request.GET.get('page')
    page_utilisateurs = paginateur.get_page(numero_page)
    '''
    page_utilisateurs = User.objects.all()
    
    # Chargement des données avec cache
    matieres = get_cached_data('all_matieres', Matiere.objects.all())
    classes = get_cached_data('all_classes', classe01.objects.all())
    
    return render(request, 'table_users.html', {
        'resultat_id': resultat,
        'liste404': liste404,
        'error_eleve': eleve_est_la,
        'error_prof': prof_est_la,
        'error_admin': admin_est_la,
        'User': page_utilisateurs,
        'Matiere': matieres,
        'classe01': classes,
        'username': b,  
        'is_auth': request.user.is_authenticated,
        'is_admin': a, 
        'langue': langue, 
        'nomjjj': nomjjj,                                    
    })
   
   
def settings_admin(request):
    langue = langue_fonction(request)
    pr = ""
    er_flr = ""
    er_mtr = ""
    a = ""
    tgpg = ""
    global redy, redx
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        if form == "form_supprimer_matiere":
            mtr_suppr = request.POST.get('matierename')
            liste_mtr_suppr = mtr_suppr.split('-')
            liste_mtr_suppr.pop(0)
            for i in liste_mtr_suppr:
                mtr = Matiere.objects.filter(id=int(i)).first()
                if mtr:
                    mtr.delete()
            cache.delete('all_matieres')
                
        elif form == "form_ajouter_matiere":
            matiere_ajou = request.POST.get('matierename01')
            if matiere_ajou.isalpha():
                matiere0 = Matiere.objects.filter(matiere=matiere_ajou).exists()
                if not matiere0:
                    Matiere.objects.create(matiere=matiere_ajou)
                    cache.delete('all_matieres')
                else:
                    er_mtr = "y"
            else:
                er_mtr = "n"
                
        elif form == "form_suppr_flr":
            liste_flr_suppr = request.POST.get('inp_suppr_flr')
            liste_flr_suppr = liste_flr_suppr.split('-')
            liste_flr_suppr.pop(0)
            for i in liste_flr_suppr:
                flr = Filiere01.objects.filter(id=int(i)).first()
                if flr:
                    flr.delete()
            cache.delete('all_filieres')
                
        elif form == "form_ajou_flr":
            flr_ajou = request.POST.get('inp_ajou_flr')
            if flr_ajou.isalpha():
                flr0 = Filiere01.objects.filter(filiere=flr_ajou).exists()
                if not flr0:
                    Filiere01.objects.create(filiere=flr_ajou)
                    cache.delete('all_filieres')
                else:
                    er_flr = "y"
            else:
                er_flr = "n"
                
        elif form == "suppr_classe":
            liste_suppr_classe = request.POST.get('inp_suppr_classe')
            liste_suppr_classe = liste_suppr_classe.split('-')
            liste_suppr_classe.pop(0)
            for i in liste_suppr_classe:
                classe = classe01.objects.filter(id=int(i)).first()
                if classe:
                    classe.delete()
            cache.delete('all_classes')     
                    
        elif form == "ajou_classe":
            slct_flr = request.POST.get('slct_flr')
            slct_annee = request.POST.get('slct_annee')
            inp_number_classe = request.POST.get('inp_number_classe')
            
            classe_ajou = slct_annee + " " + slct_flr + " 0" + inp_number_classe
            classe = classe01.objects.filter(classe=classe_ajou).exists()
            if not classe:
                classe01.objects.create(classe=classe_ajou)
                cache.delete('all_classes')
            else:
                pr = "y"
                
        elif form == "debloquerpub":
            redx = "bloque"
            
        elif form == "debloquecertif":
            redy = "bloque"
            
        elif form == "bloquepub":
            redx = "debloque"
            
        elif form == "bloquecertf":
            redy = "debloque"
            
        elif form == "recevoir_pdf":
            liste_classe = []
            liste_matiere = []
            sur = False
            num = 0
            
            for i in classe01.objects.all():
                r = str(i.classe)
                liste_classe.append(r)
                
            for i in Matiere.objects.all():
                r = str(i.matiere)
                liste_matiere.append(r)
           
            for mtr in liste_matiere:
                tgpg += f"============<( 💎 PROF - {mtr} 💎 )>================\n\n"
                for i_un in User.objects.filter(profile__badge="prof",profile__matiere=mtr):
                    x = i_un.profile.password
                    y = i_un.username
                    
                    if sur == False:
                        tgpg += f" {y} 🎓 {x}       /       "
                        sur = True
                    else:
                        num += 1
                        tgpg += f" {y} 🎓 {x} \n--------------------------------------------------------------<({num} 💡)>\n\n"
                        sur = False
                        
            sur = False
            
            for mtr in liste_classe:
                tgpg += f"===========<( 💎 ELEVE - {mtr} 💎 )>===========\n\n"
                for i_deux in User.objects.filter(profile__badge="eleve",profile__classe=mtr):
                    x = i_deux.profile.password
                    y = i_deux.username
                    
                    if sur == False:
                        tgpg += f" {y} 🎓 {x}       /       "
                        sur = True
                    else:
                        num += 1
                        tgpg += f" {y} 🎓 {x} \n--------------------------------------------------------------<({num} 💡)>\n\n"
                        sur = False
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement avec cache
    matieres = get_cached_data('all_matieres', Matiere.objects.all())
    classes = get_cached_data('all_classes', classe01.objects.all())
    filieres = get_cached_data('all_filieres', Filiere01.objects.all())
    
    return render(request, 'settings_admin.html', {
        'error_flr': er_flr,
        'error_mtr': er_mtr,
        'error_classe': pr,
        'Matiere': matieres,
        'classe01': classes,
        'Filiere01': filieres,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
        'redx': redx,
        'redy': redy,
        'tout_infos':tgpg,
    })
    

def sign_in_many(request):
    langue = langue_fonction(request)
    dct_eleve_good = ""
    dct_prof_good = ""
    a = ""
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form == "form_tout_eleve":
            dct_eleve = unquote(request.POST.get('inp_dct_eleve'))
            slct_classe = request.POST.get('slct_classe0010')
            try:
                dct_eleve = ast.literal_eval(dct_eleve)
                dct_eleve_good = True
                
                if isinstance(dct_eleve, list):
                    for i in dct_eleve:
                        if not isinstance(i, dict):
                            dct_eleve_good = False
                            break
                    for i in dct_eleve:
                        if not ("nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip()):
                            dct_eleve_good = "err_n_p"
                            break
                    
                    if dct_eleve_good == True:
                        for i in dct_eleve:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_classe
                            p = str(random.randint(1000, 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t, first_name=y, last_name=x, password=p)
                            user0.profile.badge = "eleve"
                            user0.profile.classe = z
                            user0.profile.password = p
                            user0.profile.save()
                        cache.delete('all_users')
            except:
                dct_eleve_good = "pas liste"
            
        elif form == "form_tout_prof":
            dct_prof = unquote(request.POST.get('inp_dct_prof'))
            slct_mtr = request.POST.get('slct_mtr_0010')
            try:
                dct_prof = ast.literal_eval(dct_prof)
                dct_prof_good = True
                
                if isinstance(dct_prof, list):
                    for i in dct_prof:
                        if not isinstance(i, dict):
                            dct_prof_good = False
                            break
                    for i in dct_prof:
                        if not ("nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip()):
                            dct_prof_good = "err_n_p"
                            break
                    
                    if dct_prof_good == True:
                        for i in dct_prof:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_mtr
                            p = str(random.randint(1000, 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t, first_name=y, last_name=x, password=p)
                            user0.profile.badge = "prof"
                            user0.profile.matiere = z
                            user0.profile.password = p
                            user0.profile.save()
                        cache.delete('all_users')
                        cache.delete('prof_users')
            except:
                dct_prof_good = "pas liste"
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement avec cache
    matieres = get_cached_data('all_matieres', Matiere.objects.all())
    classes = get_cached_data('all_classes', classe01.objects.all())
    
    return render(request, 'sign_in_many.html', {
        'dct_eleve_good': dct_eleve_good,
        'dct_prof_good': dct_prof_good,
        'Matiere': matieres,
        'classe01': classes,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
    })
    
    
def name_change(request):
    langue = langue_fonction(request)
    a = ""
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form == "accepter_changement":
            h = request.POST.get('quelchoix')
            changement = changement_nom_prernom.objects.filter(id=int(h)).first()
            if changement:
                x = changement.nom_avant
                y = changement.prenom_avant
                z = changement.nom_apr
                o = changement.prenom_apr
                
                user0 = User.objects.get(first_name=y, last_name=x)
                user0.first_name = o
                user0.last_name = z
                user0.save()
                changement.delete()
                cache.delete('all_changements')
                                
        elif form == "refuser_changement":
            h = request.POST.get('quelchoix')
            changement = changement_nom_prernom.objects.filter(id=int(h)).first()
            if changement:
                changement.delete()
                cache.delete('all_changements')
            
        elif form == "toutrefusernoms":
            changement_nom_prernom.objects.all().delete()
            cache.delete('all_changements')
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement avec cache
    all_changements = get_cached_data('all_changements', 
        changement_nom_prernom.objects.all())  # Limite pour éviter trop de données
    
    return render(request, 'name_change.html', {
        'changement_nom_prernom': all_changements,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
    })
    
    
def posting_news(request):
    langue = langue_fonction(request)
    a = ""
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    date0001 = date.today()
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form == "poster_info":
            titre = request.POST.get('titre')
            date_info = date0001
            text = request.POST.get('text')
            
            post_exists = posts.objects.filter(titre=titre, text=text, date=date_info).exists()
            
            if not post_exists:
                posts.objects.create(titre=titre, text=text, date=date_info)
                cache.delete('all_posts')
                
        elif form == "supprimertoutposts":
            posts.objects.all().delete()
            cache.delete('all_posts')
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    return render(request, 'posts.html', {
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
    })


def table_time(request):
    langue = langue_fonction(request)
    o_emplois = ""
    date0001 = date.today()
    a = ""
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form == "save_emplois":
            code_html_emplois = request.POST.get('code_html_emplois')
            titre_emplois = request.POST.get('titre_emplois')
            emploi_exists = emplous_temps.objects.filter(
                titre=titre_emplois, 
                emplois=code_html_emplois
            ).exists()
            
            if not emploi_exists:
                emplous_temps.objects.create(titre=titre_emplois, emplois=code_html_emplois)
                cache.delete('all_emplois')
                return redirect('table_time_name')
            
        elif form == "suprimer_lemplois":
            idk = request.POST.get('id_emplois')
            emploi = emplous_temps.objects.filter(id=int(idk)).first()
            
            if emploi:
                x = "<table>" + emploi.emplois + "</table>"
                z = "emplois"
                i = emploi.titre
                
                post = posts.objects.filter(text=x, titre=i, type=z).first()
                if post:
                    post.delete()
                    cache.delete('all_posts')
                
                emploi.delete()
                cache.delete('all_emplois')
            
        elif form == "poster_emplois":
            titre0 = request.POST.get('titre_emplois')
            date_post = date0001
            emplois = "<table>" + request.POST.get('emplois') + "</table>"
            type0 = "emplois"
            
            post_exists = posts.objects.filter(
                titre=titre0, 
                date=date_post, 
                text=emplois, 
                type=type0
            ).exists()
            
            if not post_exists:
                posts.objects.create(titre=titre0, date=date_post, text=emplois, type=type0)
                cache.delete('all_posts')
            else:
                o_emplois = "emplois_deja_la" 
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement avec cache
    all_emplois = get_cached_data('all_emplois', emplous_temps.objects.all()[:50])
    classes = get_cached_data('all_classes', classe01.objects.all())

    return render(request, 'table_time.html', {
        'o_emplois': o_emplois,
        'emplois_temps': all_emplois,
        'classe01': classes,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
    })
   
   
def profile(request):
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    att = ""
    c_d = 0
    a = ""
    b = ""
    c = ""
    d = ""
    e = ""
    f = ""
    g = ""
    h = ""
    i = ""
    
    if request.user.is_authenticated:
        a = request.user.first_name
        b = request.user.last_name
        c = request.user.username
        d = request.user.profile.classe
        e = request.user.profile.badge
        f = request.user.profile.matiere
        g = request.user.profile.heure_de_reception
        h = request.user.profile.dm
        i = request.user.profile.badge
    
        if form == "demande_changement":
            x = request.POST.get('nom_voulu')
            y = request.POST.get('prenom_voulu')
            z = request.user.last_name
            o = request.user.first_name
            
            c_d += 1
            changement_exists = changement_nom_prernom.objects.filter(
                nom_avant=z, 
                prenom_avant=o, 
                nom_apr=x, 
                prenom_apr=y
            ).exists()
            
            if not changement_exists:
                changement_nom_prernom.objects.create(
                    nom_avant=z, 
                    prenom_avant=o, 
                    nom_apr=x, 
                    prenom_apr=y
                )
                cache.delete('all_changements')
                request.user.profile.dm += "M"
                request.user.profile.save()
                
            else:
                att = "deja_la"
                
                
        elif form == "log-out_user":
            logout(request)
            return redirect('home_name')

        elif form == "changer_reception":
            db = request.POST.get('db_reception') 
            fn = request.POST.get('fn_reception') 
            jr = request.POST.get('slct_jour')
            
            x = jr + " : " + db + " - " + fn
            
            request.user.profile.heure_de_reception = x
            request.user.profile.save()
            return redirect('profile_name')
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    return render(request, 'profile.html', {
        'first_name': a,
        'last_name': b,
        'username': c,
        'classe': d,
        'badge': e,
        'matiere': f,
        'heures_de_reception': g,
        'c_d': c_d,
        'att': att,
        'chance': h,
        'pubs': pubs,
        'is_auth': request.user.is_authenticated,
        'is_admin': i,
        'langue': langue,
        'nomjjj': nomjjj,
    })
    
    
def news(request):
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a = ""
    b = "."
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
        b = request.user.profile.badge
    
    if form == "suppr_post":
        id = request.POST.get('id_post')
        if request.user.profile.badge == "admin":
            post_to_delete = posts.objects.filter(id=int(id)).first()
            if post_to_delete:
                post_to_delete.delete()
                cache.delete('all_posts')
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    # Chargement avec cache et optimisation
    all_posts = get_cached_data('all_posts', 
         posts.objects.all()[:100])
    
    return render(request, 'news.html', {
        'posts': reversed(all_posts),
        'posts0': all_posts,
        'pubs': pubs,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'badge': b,
        'langue': langue,
        'nomjjj': nomjjj,
    })
    
    
def log_in(request):
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    mdp_faux = "vrai"    
    a = ""
    fautemdp = 0
    
    
    
    if request.user.is_authenticated:
        a = request.user.profile.badge 
    
    if form == "log-in_user":
        x = request.POST.get('nom')
        y = request.POST.get('prenom')
        z = request.POST.get('password')
        
        
        e1 = x + "_" + y
        e1 = e1.split(" ")
        e1 = "_".join(e1)
        e2 = authenticate(request,username=e1,password=z)
        if e2:
            login(request, e2)
            return redirect('home_name')
        else:
            e1 = y + "_" + x
            e1 = e1.split(" ")
            e1 = "_".join(e1)
            e2 = authenticate(request,username=e1,password=z)
            if e2:
                login(request, e2)
                return redirect('home_name')
            else:
                mdp_faux = "faux"
                
                    
                
    '''
    user1 = User.objects.filter(first_name=y, last_name=x).first()
        if user1:
            user1 = User.objects.get(first_name=y, last_name=x)
            if str(user1.profile.password) == z:
                u_1 = user1.username
                u = authenticate(request, username=u_1, password=z)
                if u:
                    login(request, u)
                    mdp_faux = "vrai"
                    return redirect('home_name')
                else:
                    mdp_faux = "faux"
            else:
                
        else:
            
    ''' 
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
           
    return render(request, 'log_in.html', {
        'mdp_faux': mdp_faux,
        'pubs': pubs,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
        'fautemdp':fautemdp,
    })
    
    
def certificat_admin0(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a = ""
    x0x = ""
    
    if request.user.is_authenticated:
        x0x = request.user.profile.badge
    
    # Chargement avec cache
    all_certificats = certificat.objects.all()
    
    if not all_certificats:
        a = "oui"
    
    if form == "accepter certificat":
        nom = request.POST.get('n')
        certif = certificat.objects.filter(id=int(nom)).first()
        if certif:
            certif.dcr = "oui"
            certif.save()
            cache.delete('all_certificats')
        
        return redirect('certificat_admin_name')
        
    elif form == "refuser certificat":
        nom = request.POST.get('n')
        certif = certificat.objects.filter(id=int(nom)).first()
        if certif:
            certif.dcr = "non"
            certif.save()
            cache.delete('all_certificats')
        
        return redirect('certificat_admin_name')
        
    elif form == "suppr tout les certificats":
        certificat.objects.all().delete()
        cache.delete('all_certificats')
        return redirect('certificat_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    return render(request, 'certificat_admin.html', {
        'certificat': certificat.objects.all(),
        'vide': a,
        'is_auth': request.user.is_authenticated,
        'is_admin': x0x,
        'langue': langue,
        'nomjjj': nomjjj,
    })


def certificat0(request):
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    z = ""
    y01 = []
    a = ""
    global redy
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
        # Requête directe au lieu de filter sur liste
        y01 = certificat.objects.filter(
            nom=request.user.last_name, 
            prenom=request.user.first_name
        )[:20]  # Limite pour éviter trop de données
        
    if form == "suppr_certif":
        idc = request.POST.get('idcertif')
        certif_to_delete = certificat.objects.filter(id=int(idc)).first()
        if certif_to_delete:
            certif_to_delete.delete()
            cache.delete('all_certificats')
        
    if form == "certificat_envoie":
        slct_jour = request.POST.get('slct_jour')
        av_abs = request.POST.get('av_abs')
        ap_abs = request.POST.get('ap_abs')
        motif = request.POST.get('motif')
        
        x = f"{slct_jour} de {av_abs} a {ap_abs}"
        
        certif_exists = certificat.objects.filter(
            nom= f"{request.user.last_name}",
            prenom= f"{request.user.first_name}",
            heure=x,
            motif=motif
        ).exists()
        
        if not certif_exists:
            certificat.objects.create(
                nom= f"{request.user.last_name}",
                prenom= f"{request.user.first_name}",
                heure=x,
                motif=motif
            )
            z = "envoyer"
            
        else:
            z = "certif deja la"
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    return render(request, 'certificat.html', {
        'z': z,
        'mescertif': y01,
        'pubs': pubs,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
        'redy': redy,
    })
    
    
def pub_admin(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a = ""
    global dm_pub312
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
    
    # Chargement avec cache
    all_pubs = get_cached_data('all_pubs', pub0.objects.all())
    
    if form == "accepter_pub":
        idg = request.POST.get('idg')
        pub = pub0.objects.filter(id=int(idg)).first()
        if pub:
            pub.dcr = "oui"
            pub.save()
            cache.delete('all_pubs')
            cache.delete('pub0_dcr_oui')
        return redirect('pub_admin_name')
    
    elif form == "toutrefuserpub":
        dm_pub312 = 0
        pubs_to_delete = pub0.objects.all()
        for pub in pubs_to_delete:
            k = pub.nom_complet.split(" ")
            l = k[0]
            f = k[-1]
            user = User.objects.filter(first_name=f, last_name=l).first()
            if user:
                rr = user.profile.dm
                rr = list(rr)
                if "P" in rr:
                    rr.remove("P")
                user.profile.dm = "".join(rr)
                user.profile.save()
        
        pub0.objects.all().delete()
        cache.delete('all_pubs')
        cache.delete('pub0_dcr_oui')
        
    elif form == "refuser_pub":
        
        dm_pub312 -= 1
        idg = request.POST.get('idg')
        pub = pub0.objects.filter(id=int(idg)).first()
        if pub:
            x = pub.nom_complet.split(" ")
            l = x[0]
            f = x[-1]
            user = User.objects.filter(first_name=f, last_name=l).first()
            if user:
                rr = user.profile.dm
                rr = list(rr)
                if "P" in rr:
                    rr.remove("P")
                user.profile.dm = "".join(rr)
                user.profile.save()
            pub.delete()
            cache.delete('all_pubs')
            cache.delete('pub0_dcr_oui')
        return redirect('pub_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    return render(request, 'pub_admin.html', {
        'pub': all_pubs,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
    })


def pub1(request):
    pubs = get_cached_data('pub0_dcr_oui', pub0.objects.filter(dcr="oui"))
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a = ""
    b = ""
    c = ""
    nomjjj = ""
    error_pub =""
    global redx
    global dm_pub312
    
    if form == "demander une pub inviter":
            pub_file = request.FILES.get('img') 
            nom = "INVITé 💎"
            message = request.POST.get('message') 
            
            pub_exists = pub0.objects.filter(
                pub=pub_file.name if pub_file else None,
                nom_complet=nom,
                message=message
            ).exists()
            
            if not pub_exists and pub_file:
                if dm_pub312 < 50:
                    pub0.objects.create(pub=pub_file, nom_complet=nom, message=message)
                    cache.delete('all_pubs')
                    
                    dm_pub312 += 1
                else:
                    error_pub = "oui"
                    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
    
    if request.user.is_authenticated:
        a = request.user.profile.badge
        b = request.user.profile.dm
        c = request.user.profile.badge
    
        if form == "demander une pub":
            pub_file = request.FILES.get('img') 
            nom = request.user.last_name + " " + request.user.first_name
            message = request.POST.get('message') 
            
            pub_exists = pub0.objects.filter(
                pub=pub_file.name if pub_file else None,
                nom_complet=nom,
                message=message
            ).exists()
            
            if not pub_exists and pub_file:
                pub0.objects.create(pub=pub_file, nom_complet=nom, message=message)
                cache.delete('all_pubs')
                request.user.profile.dm += "P"
                b = request.user.profile.dm
                request.user.profile.save()
        
                
                    
    
    return render(request, 'pub1.html', {
        'error_pub':error_pub,
        'chance': b,
        'pubs': pubs,
        'badge': c,
        'is_auth': request.user.is_authenticated,
        'is_admin': a,
        'langue': langue,
        'nomjjj': nomjjj,
        'redx': redx,
    })


def contact_us(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    is_auth = False
    is_admin = False
    global limite
    error0 = False
    u_limite = 3
    
    global contact_chance
    if contact_chance >= 50:
        limite = "max"
    else:
        limite = False

    if request.user.is_authenticated:
        is_auth = True
        if request.user.profile.badge == "admin":
            is_admin = "admin"

    if form == "mehdi":
        if contact_chance < u_limite:
            
            x = request.POST.get('nom') + request.POST.get('prenom')
            y = request.POST.get('numero')
            z = request.POST.get('message')
            t = "mehdi"
            if x.isalpha() and y.isdigit():
                x = request.POST.get('nom') + " " + request.POST.get('prenom')
                contact_chance += 1
                contact01.objects.create(nom_complet=x,numero=y,message=z,qui=t)
                error0 = "cbon"
            else:
                error0= "error"
        else:
            limite = "max"
        
    elif form == "samy":
        if contact_chance < u_limite:        
        
            x = request.POST.get('nom') + request.POST.get('prenom')
            y = request.POST.get('numero')
            z = request.POST.get('message')
            t = "samy"
            if x.isalpha() and y.isdigit():
                x = request.POST.get('nom') + " " + request.POST.get('prenom')
                contact_chance += 1
                contact01.objects.create(nom_complet=x,numero=y,message=z,qui=t)
                error0 = "cbon"
            else:
                error0= "error"
        else:
            limite = "max"
        
    elif form == "directeur":
        if contact_chance < u_limite:        
        
            x = request.POST.get('nom') + request.POST.get('prenom')
            y = request.POST.get('numero')
            z = request.POST.get('message')
            t = "directeur"
            if x.isalpha() and y.isdigit():
                x = request.POST.get('nom') + " " + request.POST.get('prenom')
                contact_chance += 1
                contact01.objects.create(nom_complet=x,numero=y,message=z,qui=t)
                error0 = "cbon"
            else:
                error0= "error"
        else:
            limite = "max"
    
    return render(request,'contact_us.html',{
        'langue':langue,
        'is_auth':is_auth,
        'is_admin':is_admin,
        'limite':limite,
        'error':error0,
        })


def contact_admin(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    is_auth = False
    is_admin = False
    g =  False
    global contact_chance

    if request.user.is_authenticated:
        g = request.user.username
        is_auth = True
        if request.user.profile.badge == "admin":
            is_admin = "admin"

    if form == "supprimer_contact":
        id2 = request.POST.get('id1')
        contact01.objects.get(id=id2).delete()
        contact_chance -= 1
        
    elif form == "supprimer_mes_contact":
        qui = request.POST.get('qui')
        for i in contact01.objects.all():
            if i.qui == qui:
                i.delete()
    elif form == "supprime_stp":
        for i in contact01.objects.all():
            if i.qui == "samy" or i.qui == "directeur":
                i.delete()
    
    return render(request,'contact_admin.html',{
        'langue':langue,
        'is_auth':is_auth,
        'is_admin':is_admin,
        'contact':contact01.objects.all(),
        'username':g,
        })


def documentation(request):
    langue = langue_fonction(request)
    return render(request,'documentation.html',{'langue':langue,})


def messagerie(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    requestuser = None
    is_auth = False
    is_admin=None
    error_groupe=None
    username=None
    badge=None
    
    if request.user.is_authenticated:
        requestuser = request.user
        username = request.user.username
        badge = request.user.profile.badge
        
        if request.user.profile.badge == "admin":
            is_admin = "admin"
            
        is_auth = True
        
        if form == "créer un groupe":
            opt = request.POST.get('opt')
            sp = request.POST.get('titre du groupe de chat')
            
            if opt == "tout le monde":
                rf = request.user
                n = User.objects.all()
                
            elif opt == "eleve":
                xv = request.POST.getlist('jsp')
                if xv:
                    rf = request.user
                    n = User.objects.filter(username=request.user.username)
                    n = n | User.objects.filter(profile__classe=f"{xv[0]}")
                    for i in xv[1:]:
                        try:
                            n = n | User.objects.filter(profile__classe=f"{i}")
                        except:
                            error_groupe = "pas choisir prof+eleve"
                    
                    f = Groupe.objects.create(nom=sp,created_by=rf)
                    f.membres.set(n)
                            
                else:
                    error_groupe ='classe'
            elif opt == "prof":
                xv = request.POST.getlist('jsp')
                if xv:
                    rf = request.user
                    n = User.objects.filter(username=request.user.username)
                    n = n | User.objects.filter(profile__matiere=f"{xv[0]}")
                    for i in xv[1:]:
                        try:
                            n = n | User.objects.filter(profile__matiere=f"{i}")
                        except:
                            error_groupe = "pas choisir prof+eleve"
                    sp = request.POST.get('titre du groupe de chat')
                    f = Groupe.objects.create(nom=sp,created_by=rf)
                    f.membres.set(n)
                            
                else:
                    error_groupe ="mtr"
            else:
               xv = request.POST.getlist('jsp')
               if not xv:
                   error_groupe = "required"
        elif form == "supprimer groupe chat":
            idg = request.POST.get('id_groupe')
            Groupe.objects.get(id=idg).delete()
        
        elif form == "modifier le titre":
            titre =  request.POST.get('titre')
            idg = request.POST.get('id_groupe')
            h_ih = Groupe.objects.get(id=idg)
            h_ih.nom = titre
            h_ih.save()
            
        elif form == "envoyer message":
            idg = request.POST.get('id_groupe')
            grp = Groupe.objects.get(id=idg)
            text = request.POST.get('text')
            img = request.FILES.get('img45')
            sndr = request.user
            Message.objects.create(groupe=grp, text=text, image=img, sender=sndr)
            
        elif form == "supprimer message":
            idg = request.POST.get('id_message')
            Message.objects.get(id=idg).delete()
            
        elif form == "signaler message":
            idg = request.POST.get('id_message')
            uh = Message.objects.get(id=idg)
            s = str(request.user.username)
            uh.signale = s
            uh.save()
        
        elif form == "designaler":
            idg = request.POST.get('id_message')
            uh = Message.objects.get(id=idg)
            uh.signale = "."
            uh.save()
               
    else:
        is_auth=False
        
    return render(request,'messagerie.html',{
        'langue':langue,
        'classe':classe01.objects.all(),
        'matiere':Matiere.objects.all(),
        'error_groupe':error_groupe,
        'is_admin':is_admin,
        'is_auth':is_auth,
        'username':username,
        'badge':badge,
        'groupe':Groupe.objects.all(),
        'requestuser':requestuser,
        })



def messages_du_groupe(request, group_id):          
    groupe = get_object_or_404(Groupe, id=group_id)
    messages = groupe.messages.all().order_by("date_creation")
    form = request.POST.get('quelform')
    ryt = None
    
    if request.user.is_authenticated:
        ryt = request.user
        
    if form == "supprimer message":
            idg = request.POST.get('id_message')
            Message.objects.get(id=idg).delete()
            
    elif form == "signaler message":
        idg = request.POST.get('id_message')
        uh = Message.objects.get(id=idg)
        s = str(request.user.username)
        uh.signale = s
        uh.save()
    
    elif form == "designaler":
        idg = request.POST.get('id_message')
        uh = Message.objects.get(id=idg)
        uh.signale = "."
        uh.save()
    
    return render(request, "partials/messages_list.html", {"messages": messages,'requestuser':ryt,})

'''from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms01 import Form01 , Form02
from .models import Matiere , Filiere01 , classe01 , changement_nom_prernom , posts , pub0 , emplous_temps , certificat
import ast
import random
from urllib.parse import unquote
import json
from datetime import date
from django.core.paginator import Paginator

# Variables globales préchargées
e14 = pub0.objects.all().filter(dcr="oui")
e15 = User.objects.filter(profile__badge="prof")
matieres = Matiere.objects.all()
filieres = Filiere01.objects.all()
classes = classe01.objects.all()
all_posts = posts.objects.all()
all_certificats = certificat.objects.all()
all_changements = changement_nom_prernom.objects.all()
all_emplois = emplous_temps.objects.all()
all_pubs = pub0.objects.all()

redx="bloque"
redy="bloque"

def langue_fonction(request):
    langue="fr"
    form = request.POST.get('quelform')
    
    if request.user.is_authenticated:
        z=request.user.profile.dm
        t=list(z)
        for i in t:
            if i == "A":
                langue="ar"
                break
            elif i == "E":
                langue="en"
                break
            elif i == "F":
                langue="fr"
                break

    if form == "languefr":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "A" or i =="E":
                    t.remove(i)
                else:
                    continue
            t.append("F")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="fr"

        else:
            langue="fr"
        
    elif form == "languear":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "E" or i =="F":
                    t.remove(i)
                else:
                    continue
            t.append("A")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="ar"

        else:
            langue="ar"
        
    elif form == "languean":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "A" or i =="F":
                    t.remove(i)
                else:
                    continue
            t.append("E")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="en"

        else:
            langue="en"
    return langue

# Create your views here.
def home(request):
    pubs = e14
    langue = langue_fonction(request)
    u17=""
    titreu17=""
    a=""
    b=""
    c=""
    d=""
    e=""
    f=""
    g=""
    p03=all_posts
    nomjjj = ""
    
    if request.user.is_authenticated:
        a=request.user.first_name+" "+request.user.last_name
        b=request.user.profile.classe
        c=request.user.profile.badge
        d=request.user.profile.matiere
        e=request.user.profile.heure_de_reception
        f=request.user.profile.badge
        g=request.user.first_name
        
        classe = request.user.profile.classe
        
        try:
            post_trouve = next((post for post in all_posts if post.titre == classe), None)
            if post_trouve:
                u17 = post_trouve.text
                titreu17 = post_trouve.titre
        except:
            u17 = ""
            titreu17 = ""
            
        if request.user.is_superuser:
            nomjjj = "oui"
    
    return render(request,'home.html',{'name':a,
                                       'classe':b,
                                       'badge':c,
                                       'matiere':d,
                                       'heures_de_reception':e,
                                       'posts':p03,
                                       
                                       'titre_emplois':titreu17,
                                       'mon_emplois':u17,
                                       
                                       'pubs':pubs,
                                       'profs':e15,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':f,
                                       
                                       'langue':langue,
                                       
                                       'name2':g,
                                       
                                       'nomjjj':nomjjj,
                                       })

def vue01login(request):
    if request.method=='POST':
        username0=request.POST.get('username')
        password0=request.POST.get('password')
        user=authenticate(request,username=username0,password=password0)
        if user:
            login(request,user)
            return redirect('home_name')
    
    return render(request,'login.html')
   
    
def table_users(request):
    langue = langue_fonction(request)
    liste404=[]
    resultat=""
    eleve_est_la=""
    prof_est_la=""
    admin_est_la=""
    a=""
    b=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.username
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form=="form_recuper_id_selected":
                    resultat = request.POST.get('resultat01')
                    resultat = resultat.split('-')
                    resultat.pop(0)
                    
                    for i in resultat:
                        global User
                        user_suppr = User.objects.filter(id=i)
                        
                        if user_suppr:
                            user_suppr = User.objects.get(id=i)
                            liste404.append(f"{user_suppr.first_name} {user_suppr.last_name}")
                            user_suppr.delete()
                    
                    resultat = "liste 404 n est pas vide"
                    
        elif form=="form_ajou_eleve":
            abc=""
            ln = request.POST.get('last_name01')
            fn = request.POST.get('first_name01')
            cl = request.POST.get('slct_classe03')
            mdp_eleve = str(random.randint(1000,1000000))
            username_eleve = f"{ln} {fn}"
            username_eleve = username_eleve.split(" ")
            
            for i in username_eleve:
                if i.isalpha():
                    continue
                else:
                    abc ="pasabc"
                    break
                
            if abc !="pasabc":
                username_eleve = "_".join(username_eleve)
                user0 = User.objects.filter(last_name=ln,first_name=fn)
                if not user0:
                    user = User.objects.create_user(username=username_eleve,password=mdp_eleve,last_name=ln,first_name=fn)
                    user.profile.classe = cl
                    user.profile.badge = "eleve"
                    user.profile.password = mdp_eleve
                    user.profile.save()
                else:
                    eleve_est_la = "y"
            else:
                eleve_est_la = "n"
                                
        elif form=="form_ajou_prof":
            ab=""
            ln = request.POST.get('last_name_prof')
            fn = request.POST.get('first_name_prof')
            mtr_selected = request.POST.get('slct_mtr03')
            mdp_prof = str(random.randint(1000,1000000))
            username_prof = f"{ln} {fn}"
            username_prof = username_prof.split(" ")
            
            tous_les_utilisateurs = User.objects.all()
            paginateur = Paginator(tous_les_utilisateurs, 50)
            numero_page = request.GET.get('page')
            page_utilisateurs = paginateur.get_page(numero_page)
            
            for i in username_prof:
                if i.isalpha():
                    continue
                else:
                    ab="ab"
                    break
            
            if ab != "ab":
                username_prof = "_".join(username_prof)
                
                user0 = User.objects.filter(last_name=ln,first_name=fn)
                if not user0:
                    user = User.objects.create_user(username=username_prof,password=mdp_prof,last_name=ln,first_name=fn)
                    user.profile.badge = "prof"
                    user.profile.password = mdp_prof
                    user.profile.matiere = mtr_selected
                    user.profile.save()
                else:
                    prof_est_la="y"
            else:
                prof_est_la="n"

        elif form=="form_ajou_administration":
            abd=""
            ln = request.POST.get('last_name_adm')
            fn = request.POST.get('first_name_adm')
            mdp_adm = request.POST.get('mdp_adm')
            username_adm = f"{ln} {fn}"
            username_adm = username_adm.split(" ")
            
            for i in username_adm:
                if i.isalpha():
                    continue
                else:
                    abd="abd"
            
            if abd!="abd":
                username_adm = "_".join(username_adm)
            
                user0 = User.objects.filter(first_name=fn,last_name=ln,)
                if not user0:
                    user = User.objects.create_user(username=username_adm,password=mdp_adm,first_name=fn,last_name=ln,)
                    user.profile.badge = "admin"
                    user.profile.password = mdp_adm
                    user.profile.save()
                else:
                    admin_est_la = "y"
            else:
                admin_est_la = "n"
        
        elif form=="form_suppr_tout_eleve":
            User.objects.filter(profile__badge="eleve").delete()
            User.objects.filter(profile__badge="pas de badge !").delete()
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'table_users.html',{
                                            'resultat_id':resultat,
                                            'liste404':liste404,
                                            'error_eleve':eleve_est_la,
                                            'error_prof':prof_est_la,
                                            'error_admin':admin_est_la,
                                            'User': page_utilisateurs,
                                            'Matiere':matieres,
                                            'classe01':classes,
                                            
                                            'username':b,  
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a, 
                                            
                                            'langue':langue, 
                                            
                                            'nomjjj':nomjjj,                                    
                                            })
   
    
def settings_admin(request):
    langue = langue_fonction(request)
    pr = ""
    er_flr=""
    er_mtr=""
    a=""
    global redy,redx
    
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        if form=="form_supprimer_matiere":
            mtr_suppr = request.POST.get('matierename')
            liste_mtr_suppr = mtr_suppr.split('-')
            liste_mtr_suppr.pop(0)
            for i in liste_mtr_suppr:
                mtr = next((m for m in matieres if m.id == int(i)), None)
                if mtr:
                    mtr.delete()
                
        elif form=="form_ajouter_matiere":
            matiere_ajou = request.POST.get('matierename01')
            if matiere_ajou.isalpha():
                matiere0 = next((m for m in matieres if m.matiere == matiere_ajou), None)
                if not matiere0:
                    new_matiere = Matiere.objects.create(matiere=matiere_ajou)
                    matieres = Matiere.objects.all()
                else:
                    er_mtr="y"
            else:
                er_mtr="n"
                
        elif form=="form_suppr_flr":
            liste_flr_suppr = request.POST.get('inp_suppr_flr')
            liste_flr_suppr = liste_flr_suppr.split('-')
            liste_flr_suppr.pop(0)
            for i in liste_flr_suppr:
                flr = next((f for f in filieres if f.id == int(i)), None)
                if flr:
                    flr.delete()
                
        elif form=="form_ajou_flr":
            flr_ajou = request.POST.get('inp_ajou_flr')
            if flr_ajou.isalpha():
                flr0 = next((f for f in filieres if f.filiere == flr_ajou), None)
                if not flr0:
                    new_filiere = Filiere01.objects.create(filiere=flr_ajou)
                    filieres = Filiere01.objects.all()
                else:
                    er_flr="y"
            else:
                er_flr="n"
                
        elif form=="suppr_classe":
            liste_suppr_classe = request.POST.get('inp_suppr_classe')
            liste_suppr_classe = liste_suppr_classe.split('-')
            liste_suppr_classe.pop(0)
            for i in liste_suppr_classe:
                classe = next((c for c in classes if c.id == int(i)), None)
                if classe:
                    classe.delete()     
                    
        elif form=="ajou_classe":
            slct_flr = request.POST.get('slct_flr')
            slct_annee = request.POST.get('slct_annee')
            inp_number_classe = request.POST.get('inp_number_classe')
            
            classe_ajou = slct_annee + " " + slct_flr + " 0" + inp_number_classe
            classe = next((c for c in classes if c.classe == classe_ajou), None)
            if not classe:
                new_classe = classe01.objects.create(classe=classe_ajou)
                classes = classe01.objects.all()
            else:
                pr="y"
                
        
                
        elif form =="debloquerpub":
            redx="bloque"
            
        elif form == "debloquecertif":
            redy="bloque"
            
        elif form == "bloquepub":
            redx="debloque"
            
        elif form == "bloquecertf":
            redy="debloque"
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
           
    
    return render(request,'settings_admin.html',{
                                                 'error_flr':er_flr,
                                                 'error_mtr':er_mtr,
                                                 'error_classe':pr,
                                                 'Matiere':matieres,
                                                 'classe01':classes,
                                                 'Filiere01':filieres,
                                                 
                                                 'is_auth':request.user.is_authenticated,
                                                 'is_admin':a,
                                                 
                                                 'langue':langue,
                                                 
                                                 'nomjjj':nomjjj,
                                                 'redx':redx,
                                                 'redy':redy,
                                                })
    

def sign_in_many(request):
    langue = langue_fonction(request)
    dct_eleve_good = ""
    dct_prof_good = ""
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form=="form_tout_eleve":
            dct_eleve = unquote(request.POST.get('inp_dct_eleve'))
            slct_classe = request.POST.get('slct_classe0010')
            try:
                dct_eleve = ast.literal_eval(dct_eleve)
                dct_eleve_good = True
                
                if isinstance(dct_eleve,list):

                    for i in dct_eleve :
                        if not isinstance(i ,dict):
                            dct_eleve_good=False
                            break
                    for i in dct_eleve :
                        if not( "nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip() ):
                            dct_eleve_good="err_n_p"
                            break
                    
                    if dct_eleve_good==True:
                        for i in dct_eleve:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_classe
                            p = str(random.randint(1000 , 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t,first_name=y,last_name=x,password=p)
                            user0.profile.badge="eleve"
                            user0.profile.classe=z
                            user0.profile.password=p
                            user0.profile.save()         
            except:
                dct_eleve_good="pas liste"
            
        elif form=="form_tout_prof":
            dct_prof = unquote(request.POST.get('inp_dct_prof'))
            slct_mtr = request.POST.get('slct_mtr_0010')
            try:
                dct_prof = ast.literal_eval(dct_prof)
                dct_prof_good = True
                
                if isinstance(dct_prof,list):

                    for i in dct_prof :
                        if not isinstance(i ,dict):
                            dct_prof_good=False
                            break
                    for i in dct_prof :
                        if not( "nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip() ):
                            dct_prof_good="err_n_p"
                            break
                    
                    if dct_prof_good==True:
                        for i in dct_prof:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_mtr
                            p = str(random.randint(1000 , 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t,first_name=y,last_name=x,password=p)
                            user0.profile.badge="prof"
                            user0.profile.matiere=z
                            user0.profile.password=p
                            user0.profile.save()
            except:
                dct_prof_good="pas liste"
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'sign_in_many.html',{'dct_eleve_good':dct_eleve_good,
                                               'dct_prof_good':dct_prof_good,
                                               'Matiere':matieres,
                                               'classe01':classes,
                                               
                                               'is_auth':request.user.is_authenticated,
                                               'is_admin':a,
                                               
                                               'langue':langue,
                                               
                                               'nomjjj':nomjjj,
                                               })
    
    
def name_change(request):
    langue = langue_fonction(request)
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form=="accepter_changement":
            h = request.POST.get('quelchoix')
            h = next((c for c in all_changements if c.id == int(h)), None)
            if h:
                x = h.nom_avant
                y = h.prenom_avant
                z = h.nom_apr
                o = h.prenom_apr
                
                user0 = User.objects.get(first_name=y,last_name=x)
                user0.first_name=o
                user0.last_name=z
                user0.save()
                h.delete()
                                
        elif form=="refuser_changement":
            h = request.POST.get('quelchoix')
            h = next((c for c in all_changements if c.id == int(h)), None)
            if h:
                h.delete()
            
        elif form=="toutrefusernoms":
            for i in all_changements:
                i.delete()
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'name_change.html',{
                                            'changement_nom_prernom':all_changements,
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a,
                                            
                                            'langue':langue,
                                            
                                            'nomjjj':nomjjj,
                                            })
    
    
def posting_news(request):
    langue = langue_fonction(request)
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    date0001=date.today()
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form =="poster_info":
            titre = request.POST.get('titre')
            date_info = date0001
            text = request.POST.get('text')
            
            x = next((p for p in all_posts if p.titre == titre and p.text == text and p.date == date_info), None)
            
            if not x:
                new_post = posts.objects.create(titre=titre,text=text,date=date_info)
                all_posts = posts.objects.all()
                
        elif form == "supprimertoutposts":
            for i in all_posts:
                i.delete()
            all_posts = posts.objects.all()
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'posts.html',{'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })


def table_time(request):
    langue = langue_fonction(request)
    o_emplois=""
    date0001=date.today()
    a=""
    
    
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form =="save_emplois":
            code_html_emplois = request.POST.get('code_html_emplois')
            titre_emplois = request.POST.get('titre_emplois')
            o = next((e for e in all_emplois if e.titre == titre_emplois and e.emplois == code_html_emplois), None)
            if not o:
                new_emploi = emplous_temps.objects.create(titre=titre_emplois,emplois=code_html_emplois)
                all_emplois = emplous_temps.objects.all()
                return redirect('table_time_name')
            
        elif form=="suprimer_lemplois":
            idk = request.POST.get('id_emplois')
            u = next((e for e in all_emplois if e.id == int(idk)), None)
            
            if u:
                x="<table>"+u.emplois+"</table>"
                z="emplois"
                i=u.titre
                
                tit = next((p for p in all_posts if p.text == x and p.titre == i and p.type == z), None)
                if tit:
                    tit.delete()
                    all_posts = posts.objects.all()
                
                u.delete()
                all_emplois = emplous_temps.objects.all()
            
            
            
        elif form=="poster_emplois":
            titre0 = request.POST.get('titre_emplois')
            date_post = date0001
            emplois = "<table>"+request.POST.get('emplois')+"</table>"
            type0="emplois"
            u = next((p for p in all_posts if p.titre == titre0 and p.date == date_post and p.text == emplois and p.type == type0), None)
            if not u:
                new_post = posts.objects.create(titre=titre0,date=date_post,text=emplois,type=type0)
                all_posts = posts.objects.all()
            else:
                o_emplois="emplois_deja_la" 
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        

    return render(request,'table_time.html',{'o_emplois':o_emplois,
                                               'emplois_temps':all_emplois,
                                               'classe01':classes,
                                               
                                               'is_auth':request.user.is_authenticated,
                                               'is_admin':a,
                                               
                                               'langue':langue,
                                               
                                               'nomjjj':nomjjj,
                                               })
   

 
def profile(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    att=""
    c_d = 0
    a=""
    b=""
    c=""
    d=""
    e=""
    f=""
    g=""
    h=""
    i=""
    if request.user.is_authenticated:
        a=request.user.first_name
        b=request.user.last_name
        c=request.user.username
        d=request.user.profile.classe
        e=request.user.profile.badge
        f=request.user.profile.matiere
        g=request.user.profile.heure_de_reception
        h=request.user.profile.dm
        i=request.user.profile.badge
    
        if form == "demande_changement":
            x = request.POST.get('nom_voulu')
            y = request.POST.get('prenom_voulu')
            z = request.user.last_name
            o = request.user.first_name
            
            c_d += 1
            att = next((c for c in all_changements if c.nom_avant == z and c.prenom_avant == o and c.nom_apr == x and c.prenom_apr == y), None)
            if not att :
                new_change = changement_nom_prernom.objects.create(nom_avant=z,prenom_avant=o,nom_apr=x,prenom_apr=y)
                all_changements = changement_nom_prernom.objects.all()
                request.user.profile.dm += "M"
                request.user.profile.save()
            else:
                att = "deja_la"
                
        elif form == "log-out_user":
            logout(request)
            return redirect('home_name')
            
        elif form == "changer_reception":
            db = request.POST.get('db_reception') 
            fn = request.POST.get('fn_reception') 
            jr = request.POST.get('slct_jour')
            
            x = jr +" : "+ db +" - "+ fn
            
            request.user.profile.heure_de_reception = x
            request.user.profile.save()
            return redirect('profile_name')
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
          
    return render(request,'profile.html',{'first_name':a,
                                       'last_name':b,
                                       'username':c,
                                       'classe':d,
                                       'badge':e,
                                       'matiere':f,
                                       'heures_de_reception':g,
                                       
                                       'c_d':c_d,
                                       'att':att,
                                       'chance':h,
                                       'pubs':pubs,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':i,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })
    
    
def news(request):
    pubs = e14
    langue = langue_fonction(request)
    form=request.POST.get('quelform')
    a=""
    b="."
    all_posts = False
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.profile.badge
    
    if form == "suppr_post":
        id = request.POST.get('id_post')
        if request.user.profile.badge=="admin":
            post_to_delete = next((p for p in all_posts if p.id == int(id)), None)
            if post_to_delete:
                post_to_delete.delete()
                all_posts = posts.objects.all()
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
            
    return render(request,'news.html',{'posts':reversed(all_posts),
                                       'posts0':all_posts,
                                       'pubs':pubs,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'badge':b,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })
    
    
def log_in(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    mdp_faux = "vrai"    
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge 
    
    if form=="log-in_user":
        x = request.POST.get('nom')
        y = request.POST.get('prenom')
        z = request.POST.get('password')
        
        user1 = User.objects.filter(first_name=y,last_name=x,)
        if user1:
            user1 = User.objects.get(first_name=y,last_name=x,)
            if str(user1.profile.password) == z:
                u = user1.username
                u = authenticate(request,username=u,password=z)
                login(request,u)
                mdp_faux = "vrai"
                return redirect('home_name')
            else:
                mdp_faux = "faux"
        else:
            mdp_faux="jsp"
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
           
    return render(request,'log_in.html',{'mdp_faux':mdp_faux,
                                         'pubs':pubs,
                                         
                                         'is_auth':request.user.is_authenticated,
                                         'is_admin':a,
                                         
                                         'langue':langue,
        
                                         'nomjjj':nomjjj,
                                         })
    
    
def certificat_admin0(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    x0x=""
    if request.user.is_authenticated:
        x0x=request.user.profile.badge
    
    if not all_certificats:
        a = "oui"
    
    if form == "accepter certificat":
        nom = request.POST.get('n')

        abs = next((c for c in all_certificats if c.id == int(nom)), None)
        if abs:
            abs.dcr = "oui"
            abs.save()
        
        return redirect('certificat_admin_name')
        
    elif form == "refuser certificat":
        nom = request.POST.get('n')

        abs = next((c for c in all_certificats if c.id == int(nom)), None)
        if abs:
            abs.dcr = "non"
            abs.save()
        
        return redirect('certificat_admin_name')
        
    elif form == "suppr tout les certificats":
        for i in all_certificats:
            i.delete()
        all_certificats = certificat.objects.all()
        return redirect('certificat_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    
    
    return render(request,'certificat_admin.html',{'certificat':all_certificats,
                                                   'vide':a,
                                                   
                                                   'is_auth':request.user.is_authenticated,
                                                   'is_admin':x0x,
                                                   
                                                   'langue':langue,
                                                   
                                                   'nomjjj':nomjjj,
                                                   })


def certificat0(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    z=""
    y01=""
    a=""
    global redy
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        y01 = [c for c in all_certificats if c.nom == request.user.last_name and c.prenom == request.user.first_name]
        
    if form =="suppr_certif":
        idc= request.POST.get('idcertif')
        certif_to_delete = next((c for c in all_certificats if c.id == int(idc)), None)
        if certif_to_delete:
            certif_to_delete.delete()
            all_certificats = certificat.objects.all()
        
    if form == "certificat_envoie":
        slct_jour = request.POST.get('slct_jour')
        av_abs = request.POST.get('av_abs')
        ap_abs = request.POST.get('ap_abs')
        motif = request.POST.get('motif')
        
        x = slct_jour + " : de " + av_abs+" a " + ap_abs
        
        y = next((c for c in all_certificats if c.nom == request.user.last_name and c.prenom == request.user.first_name and c.heure == x and c.motif == motif), None)
        if not y:
            new_certif = certificat.objects.create(nom=request.user.last_name,prenom=request.user.first_name,heure=x,motif=motif)
            all_certificats = certificat.objects.all()
            z ="envoyer"
            redirect('certificat_name')
        else:
            z ="certif deja la"
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
        
    return render(request,'certificat.html',{'z':z,
                                             'mescertif':y01,
                                             'pubs':pubs,
                                             
                                             'is_auth':request.user.is_authenticated,
                                             'is_admin':a,
                                             
                                             'langue':langue,
                                             
                                             'nomjjj':nomjjj,
                                             
                                             'redy':redy,
                                             })
    
    
def pub_admin(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if form == "accepter_pub":
        idg = request.POST.get('idg')
        x = next((p for p in all_pubs if p.id == int(idg)), None)
        if x:
            x.dcr="oui"
            x.save()
        return redirect('pub_admin_name')
    
    
    elif form == "toutrefuserpub":
        for i in all_pubs:
          k=i.nom_complet.split(" ")
          l=k[0]
          f=k[-1]
          i.delete()
          us = User.objects.filter(first_name=f,last_name=l)
          if us:
            us = User.objects.get(first_name=f,last_name=l)
            rr = us.profile.dm
            rr = list(rr)
            for i in rr:
                if i == "P":
                    rr.remove(i)
            us.profile.dm=rr
            us.profile.save()
          
        all_pubs = pub0.objects.all()
        
    elif form == "refuser_pub":
        idg = request.POST.get('idg')
        z = next((p for p in all_pubs if p.id == int(idg)), None)
        if z:
            x = z.nom_complet.split(" ")
            l=x[0]
            f=x[-1]
            us = User.objects.filter(first_name=f,last_name=l)
            if us:
                us = User.objects.get(first_name=f,last_name=l)
                rr = us.profile.dm
                rr = list(rr)
                for i in rr:
                    if i == "P":
                        rr.remove(i)
                us.profile.dm=rr
                us.profile.save()
            z.delete()
            all_pubs = pub0.objects.all()
        return redirect('pub_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
        
    return render(request,'pub_admin.html',{'pub':all_pubs,
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a,
                                            
                                            'langue':langue,
                                            'nomjjj':nomjjj,
                                            })


def pub1(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    b=""
    c=""
    nomjjj = ""
    global redx
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.profile.dm
        c=request.user.profile.badge
    
        if form == "demander une pub":
            pub = request.FILES.get('img') 
            nom = request.user.last_name +" "+request.user.first_name
            message = request.POST.get('message') 
            
            x = next((p for p in all_pubs if str(p.pub) == str(pub) and p.nom_complet == nom and p.message == message), None)
            
            if not x:
                new_pub = pub0.objects.create(pub=pub,nom_complet=nom,message=message)
                all_pubs = pub0.objects.all()
                request.user.profile.dm += "P"
                b = request.user.profile.dm
                request.user.profile.save()
        
    
    return render(request,'pub1.html',{'chance':b,
                                       'pubs':pubs,
                                       'badge':c,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'langue':langue,
                                       'nomjjj':nomjjj,
                                       'redx':redx,
                                       })
    
    
def base01(request):
    return render(request,'base01.html',{})

'''

#AVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAV  

'''from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms01 import Form01 , Form02
from .models import Matiere , Filiere01 , classe01 , changement_nom_prernom , posts , pub0 , emplous_temps , certificat
import ast
import random
from urllib.parse import unquote
import json
from datetime import date
from django.core.paginator import Paginator

e14 = pub0.objects.all().filter(dcr="oui")
e15 = User.objects.filter(profile__badge="prof")

redx="bloque"
redy="bloque"

def langue_fonction(request):
    langue="fr"
    form = request.POST.get('quelform')
    
    if request.user.is_authenticated:
        z=request.user.profile.dm
        t=list(z)
        for i in t:
            if i == "A":
                langue="ar"
                break
            elif i == "E":
                langue="en"
                break
            elif i == "F":
                langue="fr"
                break

    if form == "languefr":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "A" or i =="E":
                    t.remove(i)
                else:
                    continue
            t.append("F")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="fr"

        else:
            langue="fr"
        
    elif form == "languear":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "E" or i =="F":
                    t.remove(i)
                else:
                    continue
            t.append("A")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="ar"

        else:
            langue="ar"
        
    elif form == "languean":
        if request.user.is_authenticated:
            x=request.user.username
            y=User.objects.get(username=x)
            z=y.profile.dm
            t=list(z)
            for i in t:
                if i == "A" or i =="F":
                    t.remove(i)
                else:
                    continue
            t.append("E")
            t="".join(t)
            y.profile.dm=t
            y.profile.save()
            langue="en"

        else:
            langue="en"
    return langue

# Create your views here.
def home(request):
    pubs = e14
    langue = langue_fonction(request)
    u17=""
    titreu17=""
    a=""
    b=""
    c=""
    d=""
    e=""
    f=""
    g=""
    p03=""
    nomjjj = ""
    if request.user.is_authenticated:
        a=request.user.first_name+" "+request.user.last_name
        b=request.user.profile.classe
        c=request.user.profile.badge
        d=request.user.profile.matiere
        e=request.user.profile.heure_de_reception
        f=request.user.profile.badge
        g=request.user.first_name
        
        classe = request.user.profile.classe
        
        p03 = posts.objects.all()
    
        try:
            post_trouve = posts.objects.get(titre=classe)
            u17 = post_trouve.text
            titreu17 = post_trouve.titre
        except posts.DoesNotExist:
            u17 = ""
            titreu17 = ""
            
        if request.user.is_superuser:
            nomjjj = "oui"
    
    return render(request,'home.html',{'name':a,
                                       'classe':b,
                                       'badge':c,
                                       'matiere':d,
                                       'heures_de_reception':e,
                                       'posts':p03,
                                       
                                       'titre_emplois':titreu17,
                                       'mon_emplois':u17,
                                       
                                       'pubs':pubs,
                                       'profs':e15,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':f,
                                       
                                       'langue':langue,
                                       
                                       'name2':g,
                                       
                                       'nomjjj':nomjjj,
                                       })

def vue01login(request):
    if request.method=='POST':
        username0=request.POST.get('username')
        password0=request.POST.get('password')
        user=authenticate(request,username=username0,password=password0)
        if user:
            login(request,user)
            return redirect('home_name')
    
    return render(request,'login.html')
   
    
def table_users(request):
    langue = langue_fonction(request)
    liste404=[]
    resultat=""
    eleve_est_la=""
    prof_est_la=""
    admin_est_la=""
    a=""
    b=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.username
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form=="form_recuper_id_selected":
                    resultat = request.POST.get('resultat01')
                    resultat = resultat.split('-')
                    resultat.pop(0)
                    
                    for i in resultat:
                        global User
                        user_suppr = User.objects.filter(id=i)
                        
                        if user_suppr:
                            user_suppr = User.objects.get(id=i)
                            liste404.append(f"{user_suppr.first_name} {user_suppr.last_name}")
                            user_suppr.delete()
                    
                    resultat = "liste 404 n est pas vide"
                    
        elif form=="form_ajou_eleve":
            abc=""
            ln = request.POST.get('last_name01')
            fn = request.POST.get('first_name01')
            cl = request.POST.get('slct_classe03')
            mdp_eleve = str(random.randint(1000,1000000))
            username_eleve = f"{ln} {fn}"
            username_eleve = username_eleve.split(" ")
            
            for i in username_eleve:
                if i.isalpha():
                    continue
                else:
                    abc ="pasabc"
                    break
                
            if abc !="pasabc":
                username_eleve = "_".join(username_eleve)
                user0 = User.objects.filter(last_name=ln,first_name=fn)
                if not user0:
                    user = User.objects.create_user(username=username_eleve,password=mdp_eleve,last_name=ln,first_name=fn)
                    user.profile.classe = cl
                    user.profile.badge = "eleve"
                    user.profile.password = mdp_eleve
                    user.profile.save()
                else:
                    eleve_est_la = "y"
            else:
                eleve_est_la = "n"
                                
        elif form=="form_ajou_prof":
            ab=""
            ln = request.POST.get('last_name_prof')
            fn = request.POST.get('first_name_prof')
            mtr_selected = request.POST.get('slct_mtr03')
            mdp_prof = str(random.randint(1000,1000000))
            username_prof = f"{ln} {fn}"
            username_prof = username_prof.split(" ")
            
            tous_les_utilisateurs = User.objects.all()
            paginateur = Paginator(tous_les_utilisateurs, 50)  # 50 par page
            numero_page = request.GET.get('page')
            page_utilisateurs = paginateur.get_page(numero_page)
            
            for i in username_prof:
                if i.isalpha():
                    continue
                else:
                    ab="ab"
                    break
            
            if ab != "ab":
                username_prof = "_".join(username_prof)
                
                user0 = User.objects.filter(last_name=ln,first_name=fn)
                if not user0:
                    user = User.objects.create_user(username=username_prof,password=mdp_prof,last_name=ln,first_name=fn)
                    user.profile.badge = "prof"
                    user.profile.password = mdp_prof
                    user.profile.matiere = mtr_selected
                    user.profile.save()
                else:
                    prof_est_la="y"
            else:
                prof_est_la="n"

        elif form=="form_ajou_administration":
            abd=""
            ln = request.POST.get('last_name_adm')
            fn = request.POST.get('first_name_adm')
            mdp_adm = request.POST.get('mdp_adm')
            username_adm = f"{ln} {fn}"
            username_adm = username_adm.split(" ")
            
            for i in username_adm:
                if i.isalpha():
                    continue
                else:
                    abd="abd"
            
            if abd!="abd":
                username_adm = "_".join(username_adm)
            
                user0 = User.objects.filter(first_name=fn,last_name=ln,)
                if not user0:
                    user = User.objects.create_user(username=username_adm,password=mdp_adm,first_name=fn,last_name=ln,)
                    user.profile.badge = "admin"
                    user.profile.password = mdp_adm
                    user.profile.save()
                else:
                    admin_est_la = "y"
            else:
                admin_est_la = "n"
        
        elif form=="form_suppr_tout_eleve":
            User.objects.filter(profile__badge="eleve").delete()
            User.objects.filter(profile__badge="pas de badge !").delete()
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'table_users.html',{
                                            'resultat_id':resultat,
                                            'liste404':liste404,
                                            'error_eleve':eleve_est_la,
                                            'error_prof':prof_est_la,
                                            'error_admin':admin_est_la,
                                            'User': page_utilisateurs,
                                            'Matiere':Matiere.objects.all(),
                                            'classe01':classe01.objects.all(),
                                            
                                            'username':b,  
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a, 
                                            
                                            'langue':langue, 
                                            
                                            'nomjjj':nomjjj,                                    
                                            })
   
    
def settings_admin(request):
    langue = langue_fonction(request)
    pr = ""
    er_flr=""
    er_mtr=""
    a=""
    global redy,redx
    
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        if form=="form_supprimer_matiere":
            mtr_suppr = request.POST.get('matierename')
            liste_mtr_suppr = mtr_suppr.split('-')
            liste_mtr_suppr.pop(0)
            for i in liste_mtr_suppr:
                mtr = Matiere.objects.get(id=i)
                mtr.delete()
                
        elif form=="form_ajouter_matiere":
            matiere_ajou = request.POST.get('matierename01')
            if matiere_ajou.isalpha():
                matiere0 = Matiere.objects.filter(matiere= matiere_ajou)
                if not matiere0:
                    Matiere.objects.create(matiere= matiere_ajou)
                else:
                    er_mtr="y"
            else:
                er_mtr="n"
                
        elif form=="form_suppr_flr":
            liste_flr_suppr = request.POST.get('inp_suppr_flr')
            liste_flr_suppr = liste_flr_suppr.split('-')
            liste_flr_suppr.pop(0)
            for i in liste_flr_suppr:
                flr = Filiere01.objects.get(id=i)
                flr.delete()
                
        elif form=="form_ajou_flr":
            flr_ajou = request.POST.get('inp_ajou_flr')
            if flr_ajou.isalpha():
                flr0 = Filiere01.objects.filter(filiere=flr_ajou)
                if not flr0:
                    Filiere01.objects.create(filiere=flr_ajou)
                else:
                    er_flr="y"
            else:
                er_flr="n"
                
        elif form=="suppr_classe":
            liste_suppr_classe = request.POST.get('inp_suppr_classe')
            liste_suppr_classe = liste_suppr_classe.split('-')
            liste_suppr_classe.pop(0)
            for i in liste_suppr_classe:
                classe = classe01.objects.get(id=i)
                classe.delete()     
                    
        elif form=="ajou_classe":
            slct_flr = request.POST.get('slct_flr')
            slct_annee = request.POST.get('slct_annee')
            inp_number_classe = request.POST.get('inp_number_classe')
            
            classe_ajou = slct_annee + " " + slct_flr + " 0" + inp_number_classe
            classe = classe01.objects.filter(classe=classe_ajou)
            if not classe:
                classe01.objects.create(classe=classe_ajou)
            else:
                pr="y"
                
        
                
        elif form =="debloquerpub":
            redx="bloque"
            
        elif form == "debloquecertif":
            redy="bloque"
            
        elif form == "bloquepub":
            redx="debloque"
            
        elif form == "bloquecertf":
            redy="debloque"
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
           
    
    return render(request,'settings_admin.html',{
                                                 'error_flr':er_flr,
                                                 'error_mtr':er_mtr,
                                                 'error_classe':pr,
                                                 'Matiere':Matiere.objects.all(),
                                                 'classe01':classe01.objects.all(),
                                                 'Filiere01':Filiere01.objects.all(),
                                                 
                                                 'is_auth':request.user.is_authenticated,
                                                 'is_admin':a,
                                                 
                                                 'langue':langue,
                                                 
                                                 'nomjjj':nomjjj,
                                                 'redx':redx,
                                                 'redy':redy,
                                                })
    

def sign_in_many(request):
    langue = langue_fonction(request)
    dct_eleve_good = ""
    dct_prof_good = ""
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form=="form_tout_eleve":
            dct_eleve = unquote(request.POST.get('inp_dct_eleve'))
            slct_classe = request.POST.get('slct_classe0010')
            try:
                dct_eleve = ast.literal_eval(dct_eleve)
                dct_eleve_good = True
                
                if isinstance(dct_eleve,list):

                    for i in dct_eleve :
                        if not isinstance(i ,dict):
                            dct_eleve_good=False
                            break
                    for i in dct_eleve :
                        if not( "nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip() ):
                            dct_eleve_good="err_n_p"
                            break
                    
                    if dct_eleve_good==True:
                        for i in dct_eleve:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_classe
                            p = str(random.randint(1000 , 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t,first_name=y,last_name=x,password=p)
                            user0.profile.badge="eleve"
                            user0.profile.classe=z
                            user0.profile.password=p
                            user0.profile.save()         
            except:
                dct_eleve_good="pas liste"
            
        elif form=="form_tout_prof":
            dct_prof = unquote(request.POST.get('inp_dct_prof'))
            slct_mtr = request.POST.get('slct_mtr_0010')
            try:
                dct_prof = ast.literal_eval(dct_prof)
                dct_prof_good = True
                
                if isinstance(dct_prof,list):

                    for i in dct_prof :
                        if not isinstance(i ,dict):
                            dct_prof_good=False
                            break
                    for i in dct_prof :
                        if not( "nom" in i and "prenom" in i and i['nom'].strip() and i['prenom'].strip() ):
                            dct_prof_good="err_n_p"
                            break
                    
                    if dct_prof_good==True:
                        for i in dct_prof:
                            x = i['nom']
                            y = i["prenom"]
                            z = slct_mtr
                            p = str(random.randint(1000 , 1000000))
                            u = f"{x} {y}"
                            u = u.split(" ")
                            t = "_".join(u)
                            user0 = User.objects.create_user(username=t,first_name=y,last_name=x,password=p)
                            user0.profile.badge="prof"
                            user0.profile.matiere=z
                            user0.profile.password=p
                            user0.profile.save()
            except:
                dct_prof_good="pas liste"
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'sign_in_many.html',{'dct_eleve_good':dct_eleve_good,
                                               'dct_prof_good':dct_prof_good,
                                               'Matiere':Matiere.objects.all(),
                                               'classe01':classe01.objects.all(),
                                               
                                               'is_auth':request.user.is_authenticated,
                                               'is_admin':a,
                                               
                                               'langue':langue,
                                               
                                               'nomjjj':nomjjj,
                                               })
    
    
def name_change(request):
    langue = langue_fonction(request)
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form=="accepter_changement":
            h = request.POST.get('quelchoix')
            h = changement_nom_prernom.objects.get(id=h)
            x = h.nom_avant
            y = h.prenom_avant
            z = h.nom_apr
            o = h.prenom_apr
            
            user0 = User.objects.get(first_name=y,last_name=x)
            user0.first_name=o
            user0.last_name=z
            user0.save()
            h.delete()
                                
        elif form=="refuser_changement":
            h = request.POST.get('quelchoix')
            h = changement_nom_prernom.objects.get(id=h)
            h.delete()
            
        elif form=="toutrefusernoms":
            uy= changement_nom_prernom.objects.all()
            for i in uy:
                i.delete()
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'name_change.html',{
                                            'changement_nom_prernom':changement_nom_prernom.objects.all(),
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a,
                                            
                                            'langue':langue,
                                            
                                            'nomjjj':nomjjj,
                                            })
    
    
def posting_news(request):
    langue = langue_fonction(request)
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    date0001=date.today()
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
        
        if form =="poster_info":
            titre = request.POST.get('titre')
            date_info = date0001
            text = request.POST.get('text')
            
            x = posts.objects.filter(titre=titre,text=text,date=date_info)
            
            if not x:
                posts.objects.create(titre=titre,text=text,date=date_info)
                
        elif form == "supprimertoutposts":
            ih = posts.objects.all()
            for i in ih:
                i.delete()
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    return render(request,'posts.html',{'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })


def table_time(request):
    langue = langue_fonction(request)
    o_emplois=""
    date0001=date.today()
    a=""
    
    
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if request.method == 'POST':
        form = request.POST.get('quelform')
    
        if form =="save_emplois":
            code_html_emplois = request.POST.get('code_html_emplois')
            titre_emplois = request.POST.get('titre_emplois')
            o = emplous_temps.objects.filter(titre=titre_emplois,emplois=code_html_emplois)
            if not o:
                emplous_temps.objects.create(titre=titre_emplois,emplois=code_html_emplois)
                return redirect('table_time_name')
            
        elif form=="suprimer_lemplois":
            idk = request.POST.get('id_emplois')
            u = emplous_temps.objects.get(id=idk)
            
            x="<table>"+u.emplois+"</table>"
            z="emplois"
            i=u.titre
            
            tit=posts.objects.filter(text=x,titre=i,type=z)
            if tit:
                posts.objects.get(text=x,titre=i,type=z).delete()
            
            u.delete()
            
            
            
        elif form=="poster_emplois":
            titre0 = request.POST.get('titre_emplois')
            date_post = date0001
            emplois = "<table>"+request.POST.get('emplois')+"</table>"
            type0="emplois"
            u = posts.objects.filter(titre=titre0,date=date_post,text=emplois,type=type0)
            if not u:
                posts.objects.create(titre=titre0,date=date_post,text=emplois,type=type0)
            else:
                o_emplois="emplois_deja_la" 
                
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        

    return render(request,'table_time.html',{'o_emplois':o_emplois,
                                               'emplois_temps':emplous_temps.objects.all(),
                                               'classe01':classe01.objects.all(),
                                               
                                               'is_auth':request.user.is_authenticated,
                                               'is_admin':a,
                                               
                                               'langue':langue,
                                               
                                               'nomjjj':nomjjj,
                                               })
   
#AVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAVAV  

 
def profile(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    att=""
    c_d = 0
    a=""
    b=""
    c=""
    d=""
    e=""
    f=""
    g=""
    h=""
    i=""
    if request.user.is_authenticated:
        a=request.user.first_name
        b=request.user.last_name
        c=request.user.username
        d=request.user.profile.classe
        e=request.user.profile.badge
        f=request.user.profile.matiere
        g=request.user.profile.heure_de_reception
        h=request.user.profile.dm
        i=request.user.profile.badge
    
        if form == "demande_changement":
            x = request.POST.get('nom_voulu')
            y = request.POST.get('prenom_voulu')
            z = request.user.last_name
            o = request.user.first_name
            
            c_d += 1
            att = changement_nom_prernom.objects.filter(nom_avant=z,prenom_avant=o,nom_apr=x,prenom_apr=y)
            if not att :
                changement_nom_prernom.objects.create(nom_avant=z,prenom_avant=o,nom_apr=x,prenom_apr=y)
                request.user.profile.dm += "M"
                request.user.profile.save()
            else:
                att = "deja_la"
                
        elif form == "log-out_user":
            logout(request)
            return redirect('home_name')
            
        elif form == "changer_reception":
            db = request.POST.get('db_reception') 
            fn = request.POST.get('fn_reception') 
            jr = request.POST.get('slct_jour')
            
            x = jr +" : "+ db +" - "+ fn
            
            request.user.profile.heure_de_reception = x
            request.user.profile.save()
            return redirect('profile_name')
        
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
          
    return render(request,'profile.html',{'first_name':a,
                                       'last_name':b,
                                       'username':c,
                                       'classe':d,
                                       'badge':e,
                                       'matiere':f,
                                       'heures_de_reception':g,
                                       
                                       'c_d':c_d,
                                       'att':att,
                                       'chance':h,
                                       'pubs':pubs,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':i,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })
    
    
def news(request):
    pubs = e14
    langue = langue_fonction(request)
    form=request.POST.get('quelform')
    a=""
    b="."
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.profile.badge
    
    if form == "suppr_post":
        id = request.POST.get('id_post')
        if request.user.profile.badge=="admin":
            posts.objects.get(id=id).delete()
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
            
    return render(request,'news.html',{'posts':reversed(posts.objects.all()),
                                       'posts0':posts.objects.all(),
                                       'pubs':pubs,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'badge':b,
                                       
                                       'langue':langue,
                                       
                                       'nomjjj':nomjjj,
                                       })
    
    
def log_in(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    mdp_faux = "vrai"    
    a=""
    
    if request.user.is_authenticated:
        a=request.user.profile.badge 
    
    if form=="log-in_user":
        x = request.POST.get('nom')
        y = request.POST.get('prenom')
        z = request.POST.get('password')
        
        user1 = User.objects.filter(first_name=y,last_name=x,)
        if user1:
            user1 = User.objects.get(first_name=y,last_name=x,)
            if str(user1.profile.password) == z:
                u = user1.username
                u = authenticate(request,username=u,password=z)
                login(request,u)
                mdp_faux = "vrai"
                return redirect('home_name')
            else:
                mdp_faux = "faux"
        else:
            mdp_faux="jsp"
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
           
    return render(request,'log_in.html',{'mdp_faux':mdp_faux,
                                         'pubs':pubs,
                                         
                                         'is_auth':request.user.is_authenticated,
                                         'is_admin':a,
                                         
                                         'langue':langue,
        
                                         'nomjjj':nomjjj,
                                         })
    
    
def certificat_admin0(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    x0x=""
    if request.user.is_authenticated:
        x0x=request.user.profile.badge
    
    if not certificat.objects.exists():
        a = "oui"
    
    if form == "accepter certificat":
        nom = request.POST.get('n')

        abs = certificat.objects.get(id=nom)
        abs.dcr = "oui"
        abs.save()
        
        return redirect('certificat_admin_name')
        
    elif form == "refuser certificat":
        nom = request.POST.get('n')

        abs = certificat.objects.get(id=nom)
        abs.dcr = "non"
        abs.save()
        
        return redirect('certificat_admin_name')
        
    elif form == "suppr tout les certificats":
        for i in certificat.objects.all():
            i.delete()
        return redirect('certificat_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    
    
    return render(request,'certificat_admin.html',{'certificat':certificat.objects.all(),
                                                   'vide':a,
                                                   
                                                   'is_auth':request.user.is_authenticated,
                                                   'is_admin':x0x,
                                                   
                                                   'langue':langue,
                                                   
                                                   'nomjjj':nomjjj,
                                                   })


def certificat0(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    z=""
    y01=""
    a=""
    global redy
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        y01 = certificat.objects.filter(nom=request.user.last_name,prenom=request.user.first_name)
    if form =="suppr_certif":
        idc= request.POST.get('idcertif')
        certificat.objects.get(id=idc).delete()
        
    if form == "certificat_envoie":
        slct_jour = request.POST.get('slct_jour')
        av_abs = request.POST.get('av_abs')
        ap_abs = request.POST.get('ap_abs')
        motif = request.POST.get('motif')
        
        x = slct_jour + " : de " + av_abs+" a " + ap_abs
        
        y = certificat.objects.filter(nom=request.user.last_name,prenom=request.user.first_name,heure=x,motif=motif)
        if not y:
            certificat.objects.create(nom=request.user.last_name,prenom=request.user.first_name,heure=x,motif=motif)
            z ="envoyer"
            redirect('certificat_name')
        else:
            z ="certif deja la"
            
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
        
    return render(request,'certificat.html',{'z':z,
                                             'mescertif':y01,
                                             'pubs':pubs,
                                             
                                             'is_auth':request.user.is_authenticated,
                                             'is_admin':a,
                                             
                                             'langue':langue,
                                             
                                             'nomjjj':nomjjj,
                                             
                                             'redy':redy,
                                             })
    
    
def pub_admin(request):
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    if request.user.is_authenticated:
        a=request.user.profile.badge
    
    if form == "accepter_pub":
        idg = request.POST.get('idg')
        x = pub0.objects.get(id=idg)
        x.dcr="oui"
        x.save()
        return redirect('pub_admin_name')
    
    
    elif form == "toutrefuserpub":
        uhff = pub0.objects.all()
        for i in uhff:
          k=i.nom_complet.split(" ")
          l=k[0]
          f=k[-1]
          i.delete()
          us = User.objects.filter(first_name=f,last_name=l)
          if us:
            us = User.objects.get(first_name=f,last_name=l)
            rr = us.profile.dm
            rr = list(rr)
            for i in rr:
                if i == "P":
                    rr.remove(i)
            us.profile.dm=rr
            us.profile.save()
          
        
    elif form == "refuser_pub":
        idg = request.POST.get('idg')
        z=pub0.objects.get(id=idg)
        x = z.nom_complet.split(" ")
        l=x[0]
        f=x[-1]
        us = User.objects.filter(first_name=f,last_name=l)
        if us:
            us = User.objects.get(first_name=f,last_name=l)
            rr = us.profile.dm
            rr = list(rr)
            for i in rr:
                if i == "P":
                    rr.remove(i)
            us.profile.dm=rr
            us.profile.save()
        z.delete()
        return redirect('pub_admin_name')
    
    nomjjj = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
        
    return render(request,'pub_admin.html',{'pub':pub0.objects.all(),
                                            
                                            'is_auth':request.user.is_authenticated,
                                            'is_admin':a,
                                            
                                            'langue':langue,
                                            'nomjjj':nomjjj,
                                            })


def pub1(request):
    pubs = e14
    langue = langue_fonction(request)
    form = request.POST.get('quelform')
    a=""
    b=""
    c=""
    nomjjj = ""
    global redx
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            nomjjj = "oui"
        
    
    if request.user.is_authenticated:
        a=request.user.profile.badge
        b=request.user.profile.dm
        c=request.user.profile.badge
    
        if form == "demander une pub":
            pub = request.FILES.get('img') 
            nom = request.user.last_name +" "+request.user.first_name
            message = request.POST.get('message') 
            
            x = pub0.objects.filter(pub=pub,nom_complet=nom,message=message)
            
            if not x:
                pub0.objects.create(pub=pub,nom_complet=nom,message=message)
                request.user.profile.dm += "P"
                b = request.user.profile.dm
                request.user.profile.save()
        
    
    return render(request,'pub1.html',{'chance':b,
                                       'pubs':pubs,
                                       'badge':c,
                                       
                                       'is_auth':request.user.is_authenticated,
                                       'is_admin':a,
                                       
                                       'langue':langue,
                                       'nomjjj':nomjjj,
                                       'redx':redx,
                                       })
    
    
def base01(request):
    return render(request,'base01.html',{})'''