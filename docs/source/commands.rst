Commands
========

General Commands
----------------

.. code:: slash

   /ping

Replies with "🏓 Pong!". Used to check if the bot is online.

.. code:: slash

   /say message: str

Repeats the provided message. Very useful to make the bot speak.

.. code:: slash

   /salut

Sends a personalized greeting to the user.

.. code:: slash

   /help

Displays the list of available commands with a brief explanation.

Prediction Commands
-------------------

.. code:: slash

   /pronos_course premier: str deuxieme: str troisieme: str best_lap: str

Allows a user to register their predictions for an event. Can be modified only once.

.. code:: slash

   /visualisation

Displays the user’s previously recorded predictions.

.. code:: slash

   /leaderboard

Shows the general leaderboard of users based on their prediction scores.

Administration Commands
-----------------------

.. code:: slash

   /clear nombre: int

Deletes a given number of messages in a channel (admins only).

.. code:: slash

   /admin_ban member: @member reason: str article: str

Bans a member from the server for a specified reason and article (moderators only).

.. code:: slash

   /admin_open duration: float

Opens a prediction session for a set duration (in hours). Works only in manual mode.

.. code:: slash

   /admin_close

Closes the prediction session manually.

.. code:: slash

   /admin_status

Shows the current bot mode (auto or manual).

.. code:: slash

   /admin_stop

Disables automatic mode and switches back to manual.

.. code:: slash

   /admin_launch

Starts automatic mode: the bot automatically opens prediction sessions based on the F1 calendar.

.. code:: slash

   /session saison: int location: str type: str

Manually configures a session (Q for qualifying, R for race). Updates the leaderboard.

Special Commands
----------------

.. code:: slash

   /presentation

Introduces the bot and allows users to propose a name via private message. These proposals are saved in a file.

System Commands (non-slash)
---------------------------

.. code:: text

   !sync

Command available only to administrators listed in `owners_id`. Synchronizes all slash commands with Discord.

Notes
-----

- Administration commands require the corresponding permissions (ban, admin, etc.).
- The prediction system uses both manual and automatic modes.
- All logs and errors are properly handled within `try/except` blocks.
