# Importation de Flask et de render_template
from flask import Flask, render_template, session, redirect
from questions import questions
from resultats import resultats
import os 

# Création de l'instance de l'app Flask
app = Flask("Quizz de personnalité")
app.secret_key = os.urandom(24)

# Route principal "/"-> notre page d'accueil qui est donc à la racine du site
@app.route("/")
def index():
    # On crée un cookie pour stocker le numero de la question
    session["numero_question"] = 0
    # On crée un cookie pour stocker le numero de la question
    session["score"] = {"Enderman":0, "Creeper":0, "Cochon":0, "Zombied":0}
    return render_template("index.html")

# Route question -> dédier à l'affichage des questions
@app.route("/question")
def question():
    global questions
    numero_question = session["numero_question"]

    # On affiche la question et les réponses correcspondantes de notre question actuelle = numero_question
    if numero_question < len(questions):
        question_texte = questions[numero_question]["question"]
        dictionnaire = questions[numero_question].copy()
        dictionnaire.pop("question")
        clefs = list(dictionnaire.keys())
        reponses = list(dictionnaire.values())
        session["clefs"] = clefs
        return render_template("question.html", question = question_texte, reponses = reponses, clefs = clefs)
    else :
        global score # On accède au score
        global resultats
        score_ordonne = sorted(session["score"], key = session["score"].get , reverse = True)
        vainqueur = score_ordonne[0]

        description = resultats[vainqueur]
        return render_template("resultat.html", nom = vainqueur)

# route pour les réponses sélectionnées : on incrémente les cookies de session "score" et "numero_question"
@app.route("/reponse/<numero>")
def reponse(numero):
    # On incrémente notre numero de question
    session["numero_question"] += 1
    # On récupère le choix de l'utilisateur sous forme de clef
    print(numero)
    choix = session["clefs"][int(numero)]
    # On incrémente selon la clef notre personnage choisi
    session["score"][choix] += 1
    return redirect("/question")

# Exécution de l'application
# 0.0.0.0 -> accessible sur le réseau local
# 81 -> port sur lequel l'application sera disponible
app.run(host="0.0.0.0", port = 81)