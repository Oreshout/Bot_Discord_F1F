Commands
========

General Commands
----------------

.. code:: slash

   /help

Displays the list of all available commands with explanations.

.. code:: slash

   /presentation

Introduces the bot and lets users suggest a name in DM. These suggestions are saved in a file.

.. code:: slash

   /rules

Displays the bot usage rules.

Prediction Commands
-------------------

.. code:: slash

   /pronos_course premier: str deuxieme: str troisieme: str best_lap: str

Submit or update your race predictions. Can be modified only once and only when a session is open.

.. code:: slash

   /pronos_qualif premier: str deuxieme: str troisieme: str

Submit or update your qualifying predictions. Can be modified only once and only when a session is open.

.. code:: slash

   /visualisation

Displays your current predictions (both race and qualifying if available).

.. code:: slash

   /leaderboard

Displays the general leaderboard based on prediction accuracy.

Admin Commands
--------------

.. code:: slash

   /clear nombre: int

Deletes a specified number of messages in a channel. Admin only.

.. code:: slash

   /admin_ban member: @member reason: str article: str

Bans a member for a specified reason and rule/article. Admin only.

.. code:: slash

   /admin_open duration: float

Opens a prediction session manually for a specified duration (in hours). Manual mode only.

.. code:: slash

   /admin_close

Closes the current prediction session manually. Manual mode only.

.. code:: slash

   /admin_status

Returns the current bot mode (manual or auto).

.. code:: slash

   /admin_stop

Stops automatic mode and reverts to manual mode. Admin only.

.. code:: slash

   /admin_launch

Launches the bot in automatic mode: sessions will be opened and closed based on the F1 calendar.

.. code:: slash

   /admin_getresult

Manually fetches session results from the FastF1 API and updates the leaderboard.

.. code:: slash

   /session saison: int location: str type: str

Manually configures a prediction session and updates the leaderboard (Q = qualifying, R = race).

System Commands (non-slash)
---------------------------

.. code:: text

   !sync

Command reserved to the developers (listed in `owners_id`). Syncs all slash commands with Discord.

Notes
-----

- Admin commands require appropriate permissions (administrator, ban members, etc.).
- The prediction system works in both **manual** and **automatic** mode.
- All sessions are time-limited and controlled based on mode.
- Errors are handled using proper `try/except` blocks, and logs are generated accordingly.
