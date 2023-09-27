# Pathfinding-Simulator

C'est un projet que j'ai réalisé quand j'étais en terminale. Nous étions trois à travailler sur le projet: Eymeric Chauchat, Baptiste Tajan et moi. Nous avions pour objectif de réaliser une "proof of concept" d'un robot d'entrepôt capable de se repérer dans son environnement et de se déplacer de manière autonome en fonction de ce dernier.

Nous sommes partis de ce robot inital qui nous a généreusement été prêté par notre lycée. Nous avons rajouté des modules de communications, de prises d'informations, d'alimentation et de controle. Pour ça nous avons notamment ajouté une caméra, deux arduino nano. 
![[4wd-60mm-mecanum-wheel-arduino-robot-kit_2_700x.webp]]

Je me suis principalement focalisé sur créer un simulateur de recherche de trajectoire et communiquer les consignes de direction avec le robot par la suite.

Globalement le simulateur est 3D, il intègre un générateur de labyrinthe, il utilise wxpython et OpenGL. L'idée c'est que grace à ce simulateur je pouvais:
- générer des cartes qui représentent mon entrepôt, 
- créer ou éditer à la main une carte
- placer des repères (repère au sol) sur mon modèle qui allait faire écho à des lignes sur le sol réel de l'entrepôt et que le robot allait pouvoir utiliser pour se repérer.
- définir un point de départ et un point d'arrivée
- tester différents algorithme de recherche de trajectoire sur ce simulateur. (Le simulateur étant dynamique on pouvait voir en direct les zones que l'algorithme de trajectoire explorait)

En rouge, ce sont les murs. En bleu des marges de sécurité pour que le robot de s'approche pas trop prêt des murs. Le robot est la boule verte, le carré vert est le point de départ, le carré orange le point d'arrivée. Les traits verts la trajectoire déterminée par l'algorithme. Les cases violettes correspondent à des lignes au sol réellement positionnées dans l'entrepôt réel. Le trait orange correspond au trajet réel du robot.
![[Pasted image 20230126174649.png]]


![[Pasted image 20230126174741.png]]

Le robot se repère dans l'espace en intégrant sa position à partir de sa petite centrale inertielle. Autant vous dire que vu notre budget et les effets de glissement de nos roues, nous n'étions absolument pas précis. Aussi pour contrer ce problème nous effectuions une deuxième localisation à partir de repère sur le sol détecté par la caméra frontale du robot. Ces repères était de simple petite ligne présente sur le sol et sur le modèle du robot qui permettaient au robot de se repositionner.

