# TP 0 - Programme en ligne de commande

Nicolas BLANC, Rémi GATTAZ, Quentin GERRY

## Ligne de commande

**1.**
Le programme trace.py, lancé sans argument ne fait aucun retour. De ce fait, la distance sémantique est infini. Il existe tout de même des messages d'erreurs lorsque des paramètres non géré sont donnée au programme.

**2.**
Afin de réduire la distance sémantique, nous avons :
- Géré les exceptions afin de créer des messages d'erreurs plus compréhensible
- Ajouté une option --help qui indique l'utilisation de ce programme
- Ajouté des messages d'erreurs (notamment sur les fonctions hors domaine)

**3.**
Nous avons rajouté :
- --xmin permettant de changer la valeur minimum de x
- --xmax permettant de changer la valeur maximum de x
- --nstep permettant de changer le nombre de valeurs de f(x) calculé entre xmin et xmax


## Langage graphique 2D

**4. 5.**
Nous avons rajouté l'option -o qui appelle la fonction tracePS au lieu de la fonction trace. Ceci permet alors de créer un fichier postscript contenant alors une représentation graphique de la foncion donnée à trace.py.
M
