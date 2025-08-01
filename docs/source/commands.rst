Commands
========

🔧 General Commands
-------------------

.. code:: slash

   /help

🆘 Displays all available commands with a short explanation.

.. code:: slash

   /presentation

🤖 Introduces the bot in the server and allows users to suggest a name via DM. Suggestions are saved in a file.

.. code:: slash

   /rules

📏 Shows the bot usage rules.

.. code:: slash

   /next_event

📅 Displays the date and name of the next F1 event.

🎯 Prediction Commands
----------------------

.. code:: slash

   /pronos statue: str premier: str deuxieme: str troisieme: str best_lap: str

📋 Submit or modify your prediction. Only one edit is allowed while the session is open.

.. code:: slash

   /visualisation

🔍 Displays your current predictions.

.. code:: slash

   /leaderboard

🏆 Shows the general ranking of all users based on their predictions.

🛡️ Admin Commands
------------------

.. code:: slash

   /admin_help

🆘 Displays all available admins commands with a short explanation.

.. code:: slash

   /admin_clear nombre: int

🧹 Deletes the specified number of messages from the current channel.

.. code:: slash

   /admin_ban member: @member reason: str article: str

🚫 Bans a member with a reason and the rule(s) violated.

.. code:: slash

   /admin_open duration: float statue: str

🟢 Opens a prediction session for a set amount of time (in hours).

.. code:: slash

   /admin_close

🔴 Closes the current prediction session.

.. code:: slash

   /admin_status

📊 Shows the bot's current mode (manual or automatic).

.. code:: slash

   /admin_stop

⛔ Disables automatic mode and switches back to manual.

.. code:: slash

   /admin_launch

🚀 Starts automatic mode: sessions open/close according to the F1 calendar.

.. code:: slash

   /admin_getresult

🔄 Manually fetches session results from the FastF1 API and updates the leaderboard.

.. code:: slash

   /session saison: int location: str type: str

⚙️ Manually configures a session and updates the leaderboard.

💰 Economy Commands
--------------------

.. code:: slash

   /salaire

💵 Collect your daily salary.

.. code:: slash

   /solde

💳 Displays your current balance.

.. code:: slash

   /solde_proteger

🛡️ Displays your secure bank balance.

.. code:: slash

   /virement somme_a_retirer: float member: @member

💸 Transfer money to another user.

.. code:: slash

   /admin_retrait somme_a_retirer: float member: @member

🏦 Withdraw money from a user's account.

.. code:: slash

   /deposit somme_a_verser: float

📥 Transfer money from your wallet to your bank.

.. code:: slash

   /withdraw somme_a_verser: float

📤 Transfer money from your bank to your wallet.

.. code:: slash

   /top

👑 Shows the top 10 richest users on the server.

.. code:: slash

   /boutique

🛍️ Opens the shop.

🎵 Music Command
----------------

.. code:: slash

   /play_song title: str

🎶 Plays a requested song.