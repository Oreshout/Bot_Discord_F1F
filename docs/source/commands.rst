Commands
========

🔧 General Commands
-------------------

.. code:: slash

   /help

📖 Displays a complete list of available commands with explanations for each.

.. code:: slash

   /presentation

🤖 Introduces the bot in the server and invites users to suggest a name via DM.  
All suggestions are saved to a file.

.. code:: slash

   /rules

📏 Displays the bot usage rules.

🎯 Prediction Commands
----------------------

.. code:: slash

   /pronos_course premier: str deuxieme: str troisieme: str best_lap: str

🏁 Submit or update your **race predictions** (top 3 + fastest lap).  
➡️ Can only be changed **once**, and **only while the session is open**.

.. code:: slash

   /pronos_qualif premier: str deuxieme: str troisieme: str

⏱️ Submit or update your **qualifying predictions** (top 3 only).  
➡️ Can only be changed **once**, and **only while the session is open**.

.. code:: slash

   /visualisation

🔍 Displays your current predictions (race and qualifying if available).

.. code:: slash

   /leaderboard

🏆 Displays the **overall leaderboard** based on prediction accuracy.

🛡️ Admin Commands
------------------

.. code:: slash

   /clear nombre: int

🧹 Deletes a specific number of messages in the current channel.  
🔒 **Admins only.**

.. code:: slash

   /admin_ban member: @member reason: str article: str

🔨 Bans a member, specifying the reason and rule/article violated.  
🔒 **Admins only.**

.. code:: slash

   /admin_open duration: float

🟢 Manually opens a prediction session for a given duration (in hours).  
⚠️ Available in **manual mode only**.

.. code:: slash

   /admin_close

🔴 Manually closes the current prediction session.  
⚠️ Available in **manual mode only**.

.. code:: slash

   /admin_status

📊 Displays the current bot mode: **manual** or **automatic**.

.. code:: slash

   /admin_stop

⛔ Stops automatic mode and switches to **manual mode**.  
🔒 **Admins only.**

.. code:: slash

   /admin_launch

🚀 Starts the bot in **automatic mode**: sessions will open and close based on the F1 calendar.

.. code:: slash

   /admin_getresult

🔄 Manually fetches results from the FastF1 API and updates the leaderboard.

.. code:: slash

   /session saison: int location: str type: str

🗂️ Manually configures a prediction session (`type = Q` for qualifying or `R` for race) and updates the leaderboard.

🛠️ Developer / System Commands
------------------------------

.. code:: text

   !sync

🧩 **Non-slash command** reserved for developers (`owners_id`).  
Synchronizes all slash commands with Discord.

📌 Notes
--------

- 🔐 **Admin commands require appropriate permissions** (e.g., administrator, ban members...).
- ⏱️ The prediction system works in both **manual** and **automatic** modes.
- 🕒 Sessions are time-limited depending on the selected mode.
- ⚙️ Errors are handled using `try/except`, and logs are generated accordingly.
