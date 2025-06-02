# 🚨 FBI Information Assistant Chatbot

Un chatbot alimenté par l'IA qui vous permet d'accéder aux informations officielles de la base de données des personnes recherchées par le FBI.

## 🎯 Objectifs du Projet

Ce chatbot vous permet de :
- Accéder à la liste des personnes les plus recherchées par le FBI
- Rechercher des personnes spécifiques par nom
- Filtrer les recherches par critères (sexe, âge, etc.)
- Obtenir des informations détaillées sur les personnes recherchées
- Consulter la liste des terroristes les plus recherchés
- Interagir avec les données FBI via une interface conversationnelle naturelle

## 📋 Prérequis

- Python 3.9+ installé sur votre système
- Éditeur de texte ou IDE (VS Code recommandé)
- Connexion Internet pour l'accès à l'API FBI
- Clé API Google AI Studio (niveau gratuit disponible)

## 🏗️ Architecture du Projet

```
FBI Information Assistant
├── frontend.py          # Interface utilisateur Streamlit
├── backend.py           # Logique IA et orchestration des agents
├── tools.py             # Outils personnalisés pour l'API FBI
├── prompts.py           # Prompts système et modèles de conversation
├── utils.py             # Fonctions utilitaires
├── requirements.txt     # Dépendances Python
└── config.env          # Variables d'environnement (clés API)
```

### 🧠 Comment ça fonctionne

1. **Frontend (`frontend.py`)**: Interface web créée avec [Streamlit](https://docs.streamlit.io/)
2. **Backend (`backend.py`)**: Orchestre la conversation IA en utilisant LangChain
3. **Outils (`tools.py`)**: Étend les capacités de l'IA avec l'accès à l'API FBI
4. **Système de mémoire**: Se souvient du contexte de conversation pour un dialogue naturel
5. **Monitoring**: Suit l'utilisation de l'IA avec Langfuse

## 🚀 Guide de Démarrage Rapide

### Étape 1: Installation des Dépendances

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer les packages requis
pip install -r requirements.txt
```

### Étape 2: Configuration des Variables d'Environnement

Créez un fichier `config.env` et ajoutez vos clés API :

```env
# Clé API Google AI Studio (niveau gratuit disponible)
GOOGLE_AI_STUDIO_API_KEY=votre_cle_google_ai_ici

# Clés Langfuse pour le monitoring (optionnel)
LANGFUSE_PUBLIC_KEY=votre_cle_publique
LANGFUSE_SECRET_KEY=votre_cle_secrete
```

**Obtenir les clés API :**
- Google AI Studio : Visitez [ai.google.dev](https://ai.google.dev) pour créer une clé API gratuite
- Langfuse : Visitez [langfuse.com](https://langfuse.com) pour le monitoring (optionnel)

### Étape 3: Lancer l'Application

```bash
streamlit run frontend.py
```

Votre chatbot s'ouvrira dans votre navigateur à `http://localhost:8501`! 🎉

## 🔍 Fonctionnalités Disponibles

### Outils FBI Intégrés (Basés sur les Données Réelles de l'API)

1. **Liste des Plus Recherchés (`get_fbi_most_wanted`)**
   - Récupère les 8 personnes les plus recherchées par le FBI
   - Affiche statut (ACTIF/CAPTURÉ), récompenses, avertissements
   - Informations détaillées : bureau FBI, date de publication, ID unique

2. **Recherche par Nom (`search_fbi_person_by_name`)**
   - Recherche complète avec description physique détaillée
   - Informations personnelles : dates de naissance, nationalité, alias
   - Données physiques : taille, poids, couleur des yeux/cheveux
   - Cicatrices, marques distinctives, professions

3. **Recherche par Bureau FBI (`search_fbi_by_field_office`)**
   - Filtre par bureau FBI spécifique (ex: "newyork", "losangeles")
   - Affiche les cas gérés par région géographique
   - Informations sur les récompenses et statuts par bureau

4. **Recherche par Statut (`search_fbi_by_status`)**
   - Filtre par statut officiel : "captured" (capturés), "na" (actifs)
   - Suivi de l'évolution des affaires
   - Dates de publication et mise à jour

5. **Recherche par Classification Personne (`search_fbi_by_classification`)**
   - `main` : Liste principale des plus recherchés
   - `vicap` : Programme d'appréhension de criminels violents
   - `ecap` : Programme d'alerte pour enfants en danger
   - `seeking-information` : Cas recherchant des informations

6. **Recherche par Classification Poster (`get_fbi_by_poster_classification`)**
   - `default` : Personnes recherchées standard
   - `law-enforcement-assistance` : Assistance aux forces de l'ordre
   - `missing` : Personnes disparues
   - `information` : Recherche d'informations

7. **Détails Complets (`get_fbi_person_details`)**
   - Informations exhaustives par ID de personne
   - Description physique complète, informations criminelles
   - Avertissements de sécurité, détails d'enquête
   - Ressources disponibles (images, fichiers)

8. **Liste Terrorisme (`get_fbi_terrorism_list`)**
   - Cases liées au terrorisme et à la sécurité nationale
   - Informations sur la nationalité et les professions
   - Avertissements spéciaux de sécurité

9. **Recherche Avancée (`get_fbi_advanced_search`)**
   - Recherche avec options de tri personnalisées
   - Tri par : publication, titre, sujets
   - Filtrage par titre avec pagination

### Données Réelles Exploitées

**Informations Personnelles Complètes :**
- Nom complet, alias, dates de naissance multiples
- Nationalité, lieu de naissance, langues parlées
- Professions, liens géographiques

**Description Physique Détaillée :**
- Taille (pieds/pouces), poids, corpulence
- Couleur des yeux/cheveux (données brutes et formatées)
- Cicatrices, tatouages, marques distinctives
- Teint, couleur de peau

**Informations Criminelles :**
- Charges spécifiques, sujets d'enquête
- Numéros NCIC, mandats d'arrêt
- Avertissements de sécurité spécialisés
- Détails des affaires avec contexte

**Données d'Enquête :**
- Bureaux FBI responsables, dates de publication
- Statut actuel (actif, capturé)
- Pays et états possibles de localisation
- Récompenses et montants spécifiques

### Paramètres de Filtrage Officiels

L'API FBI supporte les critères suivants :
- **`title`** : Nom ou partie du nom de la personne
- **`field_offices`** : Bureau FBI (ex: "newyork", "chicago", "miami")
- **`status`** : Statut de l'affaire ("captured", "na")
- **`person_classification`** : Type de classification ("main", "vicap", "ecap")
- **`sort_on`** : Critère de tri ("publication", "title", "subjects")
- **`sort_order`** : Ordre de tri ("asc", "desc")
- **`page`** et **`pageSize`** : Pagination des résultats

### Exemples d'Utilisation (Données Réelles)

**Recherches de base :**
```
"Montre-moi la liste des personnes les plus recherchées par le FBI"
"Recherche John Smith avec toutes ses informations"
"Affiche la liste des cas de terrorisme"
```

**Filtrage par bureau FBI :**
```
"Recherche dans le bureau FBI de Cincinnati"
"Montre-moi les cas du bureau de Miami"
"Trouve les personnes recherchées à Little Rock"
```

**Filtrage par statut officiel :**
```
"Trouve les suspects récemment capturés"
"Montre-moi toutes les affaires actives"
"Recherche les personnes avec statut 'captured'"
```

**Filtrage par classification :**
```
"Affiche les cas de la liste principale (main)"
"Montre-moi les cas VICAP de crimes violents"
"Trouve les alertes enfants en danger (ECAP)"
"Recherche les cas seeking-information"
```

**Classifications de poster :**
```
"Montre les cas d'assistance aux forces de l'ordre"
"Affiche les personnes disparues (missing)"
"Trouve les cas de recherche d'informations"
"Montre les personnes recherchées standard"
```

**Recherches avancées avec données réelles :**
```
"Recherche avancée triée par date de publication récente"
"Trouve 'Dixon' avec toutes ses informations physiques"
"Montre les résultats triés par titre alphabétique"
```

**Informations exhaustives :**
```
"Donne-moi tous les détails pour la personne ID d79f8572987541d2b4c9e4119b8dd444"
"Affiche la description physique complète de cette personne"
"Montre les avertissements de sécurité et détails d'enquête"
```

**Types de données récupérées :**
- **Statut en temps réel** : 🔴 ACTIF / 🟢 CAPTURÉ
- **Informations physiques** : Taille (5'11"), poids (215 lbs), cicatrices
- **Données biographiques** : Naissance, nationalité, alias
- **Détails criminels** : Charges spécifiques, avertissements de sécurité
- **Contexte d'enquête** : Bureau responsable, dates, récompenses

## 🛠️ Comprendre le Code

### Architecture Frontend (`frontend.py`)

Le frontend utilise **Streamlit** pour l'interface web :

```python
# Composants Streamlit clés :
st.chat_message()      # Bulles de conversation
st.chat_input()        # Champ de saisie utilisateur
st.sidebar.button()    # Fonctionnalité de réinitialisation
st.session_state       # Stockage de données persistantes
```

### Architecture Backend (`backend.py`)

Le backend orchestre les conversations IA :

```python
class ChatBackend:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI()     # Modèle IA
        self.tools = [get_fbi_tools]            # Outils disponibles
        self.memory = ConversationBufferMemory() # Mémoire de contexte
```

### Système d'Outils (`tools.py`)

Les outils étendent les capacités de l'IA :

```python
@tool
def get_fbi_most_wanted() -> str:
    """Obtient la liste des personnes les plus recherchées par le FBI"""
    # Votre implémentation d'outil ici
```

## ⚠️ Considérations Importantes

### Sécurité et Responsabilité

- **Source Officielle**: Les données proviennent de l'API officielle du FBI
- **Utilisation Responsable**: Ne pas utiliser pour harceler ou diffamer
- **Signalement**: Si vous avez des informations sur une personne recherchée, contactez les autorités

### Contacts d'Urgence

- **FBI**: 1-800-CALL-FBI (1-800-225-5324)
- **Conseils en ligne**: [tips.fbi.gov](https://tips.fbi.gov)
- **Urgence locale**: Contactez votre police locale

### Bureaux FBI Disponibles

**Bureaux principaux :**
- `newyork` - New York
- `losangeles` - Los Angeles
- `chicago` - Chicago
- `miami` - Miami
- `philadelphia` - Philadelphie
- `boston` - Boston
- `detroit` - Detroit
- `houston` - Houston
- `atlanta` - Atlanta
- `phoenix` - Phoenix
- `baltimore` - Baltimore
- `cleveland` - Cleveland

**Classifications Spéciales :**
- `main` - Liste principale des plus recherchés
- `vicap` - Programme d'appréhension de criminels violents
- `ecap` - Programme d'alerte pour enfants en danger
- `seeking-information` - Cas recherchant des informations du public

**Statuts Disponibles :**
- `captured` - Personnes capturées
- `na` - Non applicable / Affaires actives

## 📊 **Structure des Données FBI Exploitées**

Le chatbot exploite pleinement la richesse de l'API officielle du FBI avec **1053+ personnes** dans la base de données.

### 🔍 **Données Personnelles Complètes**

**Exemple de données réelles extraites :**
```json
{
  "title": "DAVEONTE JAMES DIXON",
  "status": "captured",  // 🟢 CAPTURÉ ou 🔴 ACTIF
  "reward_text": "Reward of up to $25,000",
  "height_min": 73,     // 6'1"
  "weight": "215 pounds",
  "eyes_raw": "Brown",
  "hair_raw": "Black",
  "race_raw": "Black",
  "warning_message": "SHOULD BE CONSIDERED ARMED AND DANGEROUS",
  "field_offices": ["cincinnati"],
  "scars_and_marks": "Dixon has a tattoo on his left forearm"
}
```

### 📋 **Types de Classifications Réelles**

**Poster Classifications :**
- `law-enforcement-assistance` : Assistance aux forces de l'ordre (Dixon, Hardin)
- `missing` : Personnes disparues (Fleming, Hatfield) 
- `default` : Personnes recherchées standard (Martinez, Astorga)
- `information` : Recherche d'informations (Pike, Panjaki)

**Person Classifications :**
- `Main` : Liste principale des plus recherchés
- `Victim` : Victimes dans des affaires (Morgan)

### 🏢 **Bureaux FBI Actifs**

Bureaux avec des affaires en cours :
- `cincinnati`, `littlerock`, `neworleans`
- `miami`, `birmingham`, `sacramento`
- `charlotte`, `indianapolis`, `phoenix`

### ⚠️ **Avertissements de Sécurité Réels**

Messages d'avertissement officiels :
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS"
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS WITH VIOLENT TENDENCIES"
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS AND AN ESCAPE RISK"

### 💰 **Récompenses Actuelles**

Montants réels offerts par le FBI :
- **$75,000** : Emily Pike (meurtre)
- **$50,000** : Asha Jaquilla Degree (disparition)
- **$25,000** : Daveonte James Dixon (tentative de meurtre)
- **$20,000** : Grant Matthew Hardin (évasion)

### 📅 **Données Temporelles**

- **Publication** : Dates de mise en ligne des avis
- **Modification** : Dernières mises à jour des dossiers
- **Chronologie** : Affaires de 1986 à 2025

### 🌍 **Données Géographiques**

- **Possible Countries** : MEX, USA (Martinez)
- **Possible States** : US-AL, US-FL, US-TX (affaires multi-états)
- **Coordinates** : Localisation précise quand disponible

## 💡 **Avantages de l'Intégration Complète**

✅ **Données 100% Officielles** - Source directe FBI API
✅ **Informations Temps Réel** - Statuts mis à jour (capturé/actif)
✅ **Descriptions Physiques Précises** - Taille, poids, signes distinctifs
✅ **Avertissements de Sécurité** - Messages officiels du FBI
✅ **Géolocalisation** - Bureaux responsables, états possibles
✅ **Classification Professionnelle** - Types d'affaires et priorités
✅ **Historique Complet** - De 1986 à aujourd'hui
✅ **Multilinguisme** - Fiches en plusieurs langues disponibles

## 🔧 Personnalisation

### Ajouter de Nouveaux Outils

Pour créer un nouvel outil FBI :

```python
@tool
def votre_outil_personnalise(parametre: str) -> str:
    """Décrit ce que fait votre outil.
    
    Args:
        parametre: Décrit le paramètre d'entrée
        
    Returns:
        Une chaîne avec la réponse de l'outil
    """
    try:
        # Votre appel API ici
        response = requests.get(f"https://api.fbi.gov/wanted/v1/{parametre}")
        data = response.json()
        
        # Formater et retourner les résultats
        return f"Votre réponse formatée: {data}"
        
    except Exception as e:
        return f"Erreur: {str(e)}"
```

**N'oubliez pas de :**
1. Importer votre outil dans `backend.py`
2. L'ajouter à la liste des outils dans `_setup_tools()`
3. Le tester dans l'interface de chat !

### Modifier la Personnalité de l'IA

Éditez `prompts.py` pour changer le comportement de votre IA :

```python
SYSTEM_PROMPT = """
Vous êtes un assistant spécialisé dans les informations FBI...
[Votre personnalité personnalisée ici]
"""
```

## 🌐 Ressources Utiles

- **[Documentation Streamlit](https://docs.streamlit.io/)**: Guide complet pour créer des applications web
- **[API FBI](https://www.fbi.gov/wanted/api)**: Documentation officielle de l'API FBI
- **[Documentation LangChain](https://python.langchain.com/)**: Framework pour applications IA
- **[Google AI Studio](https://ai.google.dev)**: Accès gratuit aux modèles IA

## 🐛 Dépannage

### Problèmes Courants

**Erreurs "Module non trouvé" :**
```bash
# Assurez-vous que l'environnement virtuel est activé
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Réinstaller les dépendances
pip install -r requirements.txt
```

**Erreurs de clé API :**
- Vérifiez que votre fichier `config.env` existe
- Vérifiez que les clés API sont correctes
- Assurez-vous qu'il n'y a pas d'espaces supplémentaires dans le fichier

**Streamlit ne démarre pas :**
```bash
# Vérifiez si le port est disponible
streamlit run frontend.py
```

**Erreurs API FBI :**
- L'API FBI est publique mais peut avoir des limites de débit
- Vérifiez votre connexion Internet
- Certaines requêtes peuvent prendre du temps

## 📝 Utilisation Éthique

Ce chatbot est conçu pour :
- ✅ Accéder aux informations publiques du FBI
- ✅ Éduquer sur les personnes recherchées
- ✅ Faciliter le signalement d'informations aux autorités

Ne l'utilisez pas pour :
- ❌ Harceler ou diffamer des individus
- ❌ Activités illégales ou non éthiques
- ❌ Diffuser de fausses informations

---

**Note légale**: Ce projet utilise l'API publique du FBI et est destiné à des fins éducatives et informatives. Les utilisateurs sont responsables de l'utilisation éthique et légale des informations obtenues.