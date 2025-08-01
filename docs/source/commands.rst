📚 Bot Documentation
====================

🔧 General Commands
-------------------

.. code:: slash

   /help

📖 Affiche la liste complète des commandes disponibles avec une explication pour chacune.

.. code:: slash

   /presentation

🤖 Présente le bot dans le serveur, puis permet à l’utilisateur de suggérer un nom en message privé. Toutes les suggestions sont sauvegardées dans un fichier.

.. code:: slash

   /rules

📏 Affiche les règles d’utilisation du bot.

🎯 Prediction Commands
----------------------

.. code:: slash

   /pronos_course premier: str deuxieme: str troisieme: str best_lap: str

🏁 Envoie ou modifie tes pronostics pour la **course** (top 3 + meilleur tour).  
➡️ Une seule modification possible, **uniquement lorsque la session est ouverte**.

.. code:: slash

   /pronos_qualif premier: str deuxieme: str troisieme: str

⏱️ Envoie ou modifie tes pronostics pour les **qualifications** (top 3 uniquement).  
➡️ Une seule modification possible, **uniquement lorsque la session est ouverte**.

.. code:: slash

   /visualisation

🔍 Affiche tes pronostics actuels, à la fois pour la course et les qualifications si disponibles.

.. code:: slash

   /leaderboard

🏆 Affiche le **classement général** basé sur la précision des pronostics de tous les membres.

🛡️ Admin Commands
------------------

.. code:: slash

   /clear nombre: int

🧹 Supprime un nombre défini de messages dans le salon actuel.  
🔒 **Réservé aux administrateurs.**

.. code:: slash

   /admin_ban member: @membre reason: str article: str

🔨 Bannit un membre en précisant la raison et l’article du règlement violé.  
🔒 **Réservé aux administrateurs.**

.. code:: slash

   /admin_open duration: float

🟢 Ouvre manuellement une session de pronostics pendant une durée définie (en heures).  
⚠️ Disponible uniquement en **mode manuel**.

.. code:: slash

   /admin_close

🔴 Ferme la session de pronostics actuelle.  
⚠️ Disponible uniquement en **mode manuel**.

.. code:: slash

   /admin_status

📊 Affiche le mode actuel du bot : **manuel** ou **automatique**.

.. code:: slash

   /admin_stop

⛔ Interrompt le mode automatique et repasse en **mode manuel**.  
🔒 **Réservé aux administrateurs.**

.. code:: slash

   /admin_launch

🚀 Active le **mode automatique** : les sessions seront ouvertes et fermées selon le calendrier F1.

.. code:: slash

   /admin_getresult

🔄 Récupère manuellement les résultats d’une session via l’API FastF1 et met à jour le leaderboard.

.. code:: slash

   /session saison: int location: str type: str

🗂️ Configure manuellement une session de pronostics (`type = Q` ou `R`) puis met à jour le classement.

🛠️ Developer / System Commands
------------------------------

.. code:: text

   !sync

🧩 Commande **non-slash** réservée aux développeurs (`owners_id`).  
Synchronise toutes les commandes slash avec Discord.

📌 Notes
--------

- 🔐 **Les commandes admin nécessitent les permissions adéquates** (ex. : administrateur, bannir des membres…).
- ⏱️ Le système de pronostics fonctionne en **mode manuel** ou **automatique**.
- 🕒 Les sessions sont limitées dans le temps, selon le mode sélectionné.
- ⚙️ Le bot utilise des `try/except` pour capturer les erreurs et génère des logs pour chaque action importante.
