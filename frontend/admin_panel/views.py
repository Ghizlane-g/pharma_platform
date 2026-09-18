import requests

from django.shortcuts import render, redirect
from django.contrib.auth import logout

BACKEND_URL = "http://backend:8001"



def login_page(request):
    if request.session.get("access_token"):
        role = request.session.get("role")
        if role == "ADMIN":
            return redirect("dashboard")
        elif role == "CLIENT":
            return redirect("client_dashboard")
        elif role == "ACHETEUR":
            return redirect("acheteur_stock")
        else:
            request.session.flush()

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            response = requests.post(
                f"{BACKEND_URL}/api/token/",
                json={
                    "username": username,
                    "password": password,
                },
                timeout=5,
            )

        except requests.exceptions.RequestException:
            return render(
                request,
                "admin_panel/login.html",
                {
                    "error": "Impossible de joindre le serveur d'authentification."
                },
            )

        if response.status_code == 200:

            data = response.json()

            access_token = data.get("access")
            refresh_token = data.get("refresh")

            request.session["access_token"] = access_token
            request.session["refresh_token"] = refresh_token
            request.session["username"] = username

            # Récupérer l'utilisateur connecté
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            user_response = requests.get(
                f"{BACKEND_URL}/api/users/me/",
                headers=headers,
                timeout=5,
            )

            if user_response.status_code == 200:

                user_data = user_response.json()

                role = user_data.get("role")

                request.session["role"] = role

                if role == "ADMIN":
                    return redirect("dashboard")

                elif role == "CLIENT":
                    return redirect("client_dashboard")

                elif role == "ACHETEUR":
                    return redirect("acheteur_stock")

                else:
                    return render(
                        request,
                        "admin_panel/login.html",
                        {
                            "error": "Rôle utilisateur inconnu."
                        },
                    )

            return render(
                request,
                "admin_panel/login.html",
                {
                    "error": "Impossible de récupérer les informations de l'utilisateur."
                },
            )

        return render(
            request,
            "admin_panel/login.html",
            {
                "error": "Nom d'utilisateur ou mot de passe incorrect.",
                "username": username,
            },
        )

    # GET → afficher simplement la page de login
    return render(
        request,
        "admin_panel/login.html"
    )
def dashboard(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/statistics/",
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.RequestException:
        response = None

    if response and response.status_code == 200:
        statistics = response.json()
    else:
        statistics = {
            "total_comptes": 0,
            "acheteurs": 0,
            "clients": 0,
            "commandes": 0,
            "medicaments": 0,
        }

    return render(
        request,
        "admin_panel/dashboard.html",
        {
            "statistics": statistics,
            "username": request.session.get("username", "Administrateur"),
        },
    )


def acheteurs(request):
    token = request.session.get("access_token")
    if not token:
        return redirect("login")

    response = requests.get(
        f"{BACKEND_URL}/api/admin/acheteurs/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )

    acheteurs = response.json() if response.status_code == 200 else []

    return render(request, "admin_panel/acheteurs.html", {"acheteurs": acheteurs})


def comptes(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BACKEND_URL}/api/accounts/",
        headers=headers,
        timeout=5,
    )

    if response.status_code == 200:
        comptes = response.json()
    else:
        comptes = []

    return render(
        request,
        "admin_panel/comptes.html",
        {
            "comptes": comptes
        }
    )

def clients(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BACKEND_URL}/api/admin/clients/",
        headers=headers,
        timeout=5,
    )

    if response.status_code == 200:
        clients = response.json()
    else:
        clients = []

    return render(
        request,
        "admin_panel/clients.html",
        {
            "clients": clients
        }
    )


def commandes(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BACKEND_URL}/api/admin/commandes/",
        headers=headers,
        timeout=5,
    )

    if response.status_code == 200:
        commandes = response.json()
    else:
        commandes = []

    return render(
        request,
        "admin_panel/commandes.html",
        {
            "commandes": commandes
        }
    )


def medicaments(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BACKEND_URL}/api/admin/medicaments/",
        headers=headers,
        timeout=5,
    )

    error = None
    if response.status_code == 200:
        medicaments = response.json()
    else:
        medicaments = []
        try:
            error = response.json().get(
                "detail",
                "Impossible de charger les médicaments."
            )
        except Exception:
            error = "Impossible de charger les médicaments."

    return render(
        request,
        "admin_panel/medicaments.html",
        {
            "medicaments": medicaments,
            "error": error,
        }
    ) 

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("login")


def Ajouter_Acheteur(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
}

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Temporary debug logs to capture request/response
        print('--- Ajouter_Acheteur DEBUG ---')
        print('access_token present:', bool(token))
        print('Sending to backend:', f'{BACKEND_URL}/api/admin/acheteurs/create/')
        print('Payload:', data)
        print('Headers:', headers)

        response = requests.post(
            f"{BACKEND_URL}/api/admin/acheteurs/create/",
            json=data,
            headers=headers,
            timeout=5,
        )

        print('Response status:', getattr(response, 'status_code', None))
        try:
            print('Response body:', response.text)
        except Exception as e:
            print('Response body read error:', e)

        if response.status_code == 201:
            return redirect("acheteurs")

        error = response.json().get(
            "detail",
            "Erreur lors de la création."
        )

        return render(
            request,
            "admin_panel/ajouter_acheteur.html",
            {"error": error}
        )

    return render(
        request,
        "admin_panel/ajouter_acheteur.html"
    )


def modifier_acheteur(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    api_url = f"{BACKEND_URL}/api/admin/acheteurs/{id}/"

    # Récupérer les informations actuelles
    if request.method == "GET":

        response = requests.get(
            api_url,
            headers=headers
        )

        if response.status_code != 200:
            return redirect("acheteurs")

        acheteur = response.json()

        return render(
            request,
            "admin_panel/modifier_acheteur.html",
            {"acheteur": acheteur}
        )

    # Modifier
    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
        }

        response = requests.patch(
            api_url,
            json=data,
            headers=headers
        )

        if response.status_code in [200, 202]:
            return redirect("acheteurs")

        error = response.json().get(
            "detail",
            "Erreur lors de la modification."
        )

        return render(
            request,
            "admin_panel/modifier_acheteur.html",
            {
                "acheteur": data,
                "error": error
            }
        )

def desactiver_acheteur(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.patch(
        f"{BACKEND_URL}/api/admin/acheteurs/{id}/desactiver/",
        headers=headers
    )

    return redirect("acheteurs")  

def activer_acheteur(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.patch(
        f"{BACKEND_URL}/api/admin/acheteurs/{id}/activer/",
        headers=headers
    )

    return redirect("acheteurs")


def Ajouter_Client(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(
            f"{BACKEND_URL}/api/admin/clients/create/",
            json=data,
            headers=headers
        )

        if response.status_code == 201:
            return redirect("clients")

        error = response.json().get(
            "detail",
            "Erreur lors de la création."
        )

        return render(
            request,
            "admin_panel/Ajouter_Client.html",
            {"error": error}
        )

    return render(
        request,
        "admin_panel/Ajouter_Client.html"
    )

def modifier_client(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    api_url = f"{BACKEND_URL}/api/admin/clients/{id}/"

    # Récupérer les informations actuelles
    if request.method == "GET":

        response = requests.get(
            api_url,
            headers=headers
        )

        if response.status_code != 200:
            return redirect("clients")

        client = response.json()

        return render(
            request,
            "admin_panel/modifier_client.html",
            {"client": client}
        )

    # Modifier
    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
        }

        response = requests.patch(
            api_url,
            json=data,
            headers=headers
        )

        if response.status_code in [200, 202]:
            return redirect("clients")

        error = response.json().get(
            "detail",
            "Erreur lors de la modification."
        )

        return render(
            request,
            "admin_panel/modifier_client.html",
            {
                "client": data,
                "error": error
            }
        )
    
def desactiver_client(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.patch(
        f"{BACKEND_URL}/api/admin/clients/{id}/desactiver/",
        headers=headers
    )

    return redirect("clients")  

def activer_client(request, id):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.patch(
        f"{BACKEND_URL}/api/admin/clients/{id}/activer/",
        headers=headers
    )

    return redirect("clients")



def ajouter_medicament(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.method == "POST":

        data = {
            "nom": request.POST.get("nom"),
            "classe": request.POST.get("classe"),
            "prix": request.POST.get("prix"),
            "statut": request.POST.get("statut"),
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(
            f"{BACKEND_URL}/api/admin/medicaments/create/",
            json=data,
            headers=headers
        )

        if response.status_code == 201:
            return redirect("medicaments")

        try:
            error = response.json().get(
                "detail",
                "Erreur lors de la création du médicament."
            )
        except:
            error = "Erreur lors de la création du médicament."

        return render(
            request,
            "admin_panel/ajouter_medicament.html",
            {"error": error}
        )

    return render(
        request,
        "admin_panel/ajouter_medicament.html"
    )


def desactiver_medicament(request, id):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.patch(
        f"{BACKEND_URL}/api/admin/medicaments/{id}/desactiver/",
        headers=headers
    )

    return redirect("medicaments")

def activer_medicament(request, id):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.patch(
        f"{BACKEND_URL}/api/admin/medicaments/{id}/activer/",
        headers=headers
    )

    return redirect("medicaments")
def modifier_medicament(request, id):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Récupérer le médicament
    response = requests.get(
        f"{BACKEND_URL}/api/admin/medicaments/{id}/",
        headers=headers
    )

    if response.status_code != 200:
        return redirect("medicaments")

    medicament = response.json()

    if request.method == "POST":

        data = {
            "nom": request.POST.get("nom"),
            "classe": request.POST.get("classe"),
            "prix": request.POST.get("prix"),
            "statut": request.POST.get("statut"),
        }

        response = requests.patch(
            f"{BACKEND_URL}/api/admin/medicaments/{id}/",
            json=data,
            headers=headers
        )

        # 👇 IMPORTANT : voir l'erreur réelle
        print("STATUS UPDATE :", response.status_code)
        print("REPONSE UPDATE :", response.text)

        if response.status_code in [200, 204]:
            return redirect("medicaments")

        try:
            error = response.json().get(
                "detail",
                response.text
            )
        except:
            error = response.text

        return render(
            request,
            "admin_panel/modifier_medicament.html",
            {
                "medicament": medicament,
                "error": error
            }
        )

    return render(
        request,
        "admin_panel/modifier_medicament.html",
        {
            "medicament": medicament
        }
    )


def modifier_statut_commande(request, id):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.method == "POST":

        statut = request.POST.get("statut")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.patch(
            f"{BACKEND_URL}/api/admin/commandes/{id}/changer_statut/",
            json={
                "statut": statut
            },
            headers=headers
        )

        if response.status_code == 200:
            return redirect("commandes")

        try:
            error = response.json().get(
                "detail",
                "Erreur lors de la modification."
            )
        except:
            error = "Erreur lors de la modification."

        return redirect("commandes")

    return redirect("commandes")

#Client 

def client_dashboard(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            f"{BACKEND_URL}/api/client/medicaments/",
            headers=headers,
            timeout=5,
        )

    except requests.exceptions.RequestException:

        return render(
            request,
            "client/dashboard.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code == 200:

        medicaments = response.json()

        # ==============================
        # RECHERCHE
        # ==============================

        recherche = request.GET.get("recherche", "").strip()

        if recherche:

            medicaments = [
                medicament
                for medicament in medicaments
                if recherche.lower()
                in medicament.get("nom", "").lower()
            ]


        # ==============================
        # FILTRE PAR CLASSE
        # ==============================

        classe = request.GET.get("classe")

        if classe:

            medicaments = [
                medicament
                for medicament in medicaments
                if medicament.get("classe") == classe
            ]


        # ==============================
        # NOM DE LA CLASSE
        # ==============================

        classes_noms = {

            "ANTALGIQUES": "Antalgiques",

            "ANTIBIOTIQUES": "Antibiotiques",

            "ANTI_INFLAMMATOIRES":"Anti-inflammatoires",

            "VITAMINES": "Vitamines",

            "DIGESTIFS": "Digestifs",

            "CARDIOLOGIE": "Cardiologie",

            "AUTRES": "Autres",
        }

        classe_selectionnee = (
            classes_noms.get(classe)
            if classe
            else None
        )


        return render(
            request,
            "client/dashboard.html",
            {
                "medicaments": medicaments,

                "classe_selectionnee":
                    classe_selectionnee,

                "recherche":
                    recherche,
            }
        )


    return render(
        request,
        "client/dashboard.html",
        {
            "error":
                "Impossible de récupérer les médicaments."
        }
    )
def ajouter_panier(request):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    if request.method != "POST":
        return redirect("client_dashboard")

    medicament_id = request.POST.get("medicament_id")
    quantite = request.POST.get("quantite", 1)

    try:
        medicament_id = int(medicament_id)
        quantite = int(quantite)

        if quantite < 1:
            raise ValueError

    except (ValueError, TypeError):
        return redirect("client_dashboard")

    panier = request.session.get("panier", {})

    medicament_id = str(medicament_id)

    if medicament_id in panier:
        panier[medicament_id] += quantite
    else:
        panier[medicament_id] = quantite

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("client_dashboard")

def panier(request):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    token = request.session.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    panier_session = request.session.get("panier", {})

    if not panier_session:
        return render(
            request,
            "client/panier.html",
            {
                "panier": [],
                "total": 0
            }
        )

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/client/medicaments/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:

        return render(
            request,
            "client/panier.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code != 200:

        return render(
            request,
            "client/panier.html",
            {
                "error": "Impossible de récupérer les médicaments."
            }
        )

    medicaments = response.json()

    panier = []
    total = 0

    for medicament in medicaments:

        medicament_id = str(medicament["id"])

        if medicament_id in panier_session:

            quantite = panier_session[medicament_id]

            prix = float(medicament["prix"])

            sous_total = prix * quantite

            panier.append({
                "id": medicament["id"],
                "nom": medicament["nom"],
                "prix": prix,
                "quantite": quantite,
                "sous_total": sous_total,
                "image": medicament.get("image")
            })

            total += sous_total

    return render(
        request,
        "client/panier.html",
        {
            "panier": panier,
            "total": total
        }
    )

def retirer_panier(request, medicament_id):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    panier = request.session.get("panier", {})

    medicament_id = str(medicament_id)

    if medicament_id in panier:
        del panier[medicament_id]

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")

def modifier_quantite_panier(request, medicament_id):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    if request.method != "POST":
        return redirect("panier")

    panier = request.session.get("panier", {})

    medicament_id = str(medicament_id)

    try:
        quantite = int(request.POST.get("quantite", 1))
    except (ValueError, TypeError):
        return redirect("panier")

    if quantite <= 0:

        if medicament_id in panier:
            del panier[medicament_id]

    else:

        if medicament_id in panier:
            panier[medicament_id] = quantite

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")

def vider_panier(request):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    request.session["panier"] = {}
    request.session.modified = True

    return redirect("panier")

def client_commandes(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/admin/mes-commandes/",
            headers=headers,
            timeout=5,
        )

    except requests.exceptions.RequestException:
        return render(
            request,
            "client/commandes.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code == 200:
        commandes = response.json()

        return render(
            request,
            "client/commandes.html",
            {
                "commandes": commandes
            }
        )

    return render(
        request,
        "client/commandes.html",
        {
            "error": "Impossible de récupérer vos commandes."
        }
    )

def modifier_quantite_panier(request, medicament_id):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    if request.method != "POST":
        return redirect("panier")

    panier = request.session.get("panier", {})

    medicament_id = str(medicament_id)

    try:
        quantite = int(request.POST.get("quantite", 1))
    except (ValueError, TypeError):
        return redirect("panier")

    if quantite <= 0:

        if medicament_id in panier:
            del panier[medicament_id]

    else:

        if medicament_id in panier:
            panier[medicament_id] = quantite

    request.session["panier"] = panier
    request.session.modified = True

    return redirect("panier")

def valider_commande(request):

    if not request.session.get("access_token"):
        return redirect("login")

    if request.session.get("role") != "CLIENT":
        return redirect("login")

    if request.method != "POST":
        return redirect("panier")

    panier = request.session.get("panier", {})

    if not panier:
        return redirect("panier")

    medicaments = []

    for medicament_id, quantite in panier.items():

        medicaments.append({
            "medicament_id": int(medicament_id),
            "quantite": int(quantite)
        })

    data = {
        "medicaments": medicaments
    }

    token = request.session.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/api/admin/creer/",
            json=data,
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:

        return render(
            request,
            "client/panier.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code == 201:

        request.session["panier"] = {}
        request.session.modified = True

        return redirect("client_commandes")

    try:
        error = response.json().get(
            "detail",
            "Impossible de valider la commande."
        )
    except ValueError:
        error = "Impossible de valider la commande."

    return render(
        request,
        "client/panier.html",
        {
            "error": error
        }
    )

#register



def register_view(request):

    if request.method == "POST":

        data = {
            "nom": request.POST.get("nom"),
            "prenom": request.POST.get("prenom"),
            "email": request.POST.get("email"),
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "role": "CLIENT",
        }

        try:
            response = requests.post(
                f"{BACKEND_URL}/api/inscription/",
                json=data,
                timeout=5
            )

        except requests.exceptions.RequestException:
            return render(
                request,
                "registration/register.html",
                {
                    "error": "Impossible de contacter le serveur."
                }
            )

        if response.status_code == 201:
            return render(
                request,
                "registration/register.html",
                {
                    "success": (
                        "Votre demande a été envoyée à "
                        "l'administrateur."
                    )
                }
            )

        try:
            errors = response.json()
        except ValueError:
            errors = "Une erreur est survenue."

        return render(
            request,
            "registration/register.html",
            {
                "error": errors
            }
        )

    return render(
        request,
        "registration/register.html"
    )

def demandes_inscription(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ADMIN" and request.session.get("role") != "ACHETEUR":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/admin/demandes/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:
        return render(
            request,
            "admin_panel/demandes_inscription.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code == 200:

        demandes = response.json()

        return render(
            request,
            "admin_panel/demandes_inscription.html",
            {
                "demandes": demandes
            }
        )

    return render(
        request,
        "admin_panel/demandes_inscription.html",
        {
            "error": "Impossible de récupérer les demandes."
        }
    )

def accepter_demande_frontend(request, pk):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ADMIN" and request.session.get("role") != "ACHETEUR":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/admin/demandes/{pk}/accepter/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:
        return redirect("demandes_inscription")

    return redirect("demandes_inscription")

def refuser_demande_frontend(request, pk):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ADMIN" and request.session.get("role") != "ACHETEUR":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        requests.post(
            f"{BACKEND_URL}/api/admin/demandes/{pk}/refuser/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:
        pass

    return redirect("demandes_inscription")

#acheteur
def acheteur_stock(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ACHETEUR":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        stock_response = requests.get(
            f"{BACKEND_URL}/api/acheteur/mon-stock/",
            headers=headers,
            timeout=5
        )

        medicaments_response = requests.get(
            f"{BACKEND_URL}/api/acheteur/medicaments/",
            headers=headers,
            timeout=5
        ) 

    except requests.exceptions.RequestException:
        return render(
            request,
            "acheteur/stock.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if (
        stock_response.status_code == 200
        and medicaments_response.status_code == 200
    ):
        return render(
            request,
            "acheteur/stock.html",
            {
                "stocks": stock_response.json(),
                "medicaments": medicaments_response.json()
            }
        )

    return render(
        request,
        "acheteur/stock.html",
        {
            "error": "Impossible de récupérer les données."
        }
    )

def ajouter_stock_frontend(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ACHETEUR":
        return redirect("login")

    if request.method != "POST":
        return redirect("acheteur_stock")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "medicament": request.POST.get("medicament"),
        "quantite": request.POST.get("quantite"),
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/api/acheteur/mon-stock/ajouter/",
            json=data,
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:

        return render(
            request,
            "acheteur/stock.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    # ✅ Succès
    if response.status_code == 201:
        return redirect("acheteur_stock")

    # ✅ Essayer de récupérer le JSON seulement s'il est valide
    try:
        erreur = response.json()

        if isinstance(erreur, dict):
            message = erreur.get(
                "detail",
                "Impossible d'ajouter le médicament."
            )
        else:
            message = "Impossible d'ajouter le médicament."

    except ValueError:
        message = (
            f"Erreur serveur ({response.status_code}). "
            "Le serveur n'a pas retourné une réponse JSON."
        )

    return render(
        request,
        "acheteur/stock.html",
        {
            "error": message
        }
    )

def modifier_stock_frontend(request, pk):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ACHETEUR":
        return redirect("login")

    if request.method != "POST":
        return redirect("acheteur_stock")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "quantite": request.POST.get("quantite")
    }

    try:
        response = requests.patch(
            f"{BACKEND_URL}/api/acheteur/mon-stock/{pk}/",
            json=data,
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:
        return redirect("acheteur_stock")

    if response.status_code == 200:
        return redirect("acheteur_stock")

    return redirect("acheteur_stock")

def supprimer_stock_frontend(request, pk):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ACHETEUR":
        return redirect("login")

    if request.method != "POST":
        return redirect("acheteur_stock")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(
            f"{BACKEND_URL}/api/acheteur/mon-stock/{pk}/supprimer/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:
        return redirect("acheteur_stock")

    return redirect("acheteur_stock")

def stock_acheteurs(request):

    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    if request.session.get("role") != "ADMIN":
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            f"{BACKEND_URL}/api/admin/stock-acheteurs/",
            headers=headers,
            timeout=5
        )

    except requests.exceptions.RequestException:

        return render(
            request,
            "admin_panel/stock_acheteurs.html",
            {
                "error": "Impossible de contacter le serveur."
            }
        )

    if response.status_code == 200:

        stocks = response.json()

        return render(
            request,
            "admin_panel/stock_acheteurs.html",
            {
                "stocks": stocks
            }
        )

    return render(
        request,
        "admin_panel/stock_acheteurs.html",
        {
            "error": "Impossible de récupérer le stock des acheteurs."
        }
    )



