TWITTER Service
===============

Periodically retrieve recent tweets and record them to database.

Provides a simple web interface at :5001 (by default) for status.

Note:
FLASK has a nice "reload" feature that restarts the server if you change
source code.  However, it doesn't kill the process, so the "cron" events
are duplicated resulting in duplicate tweets written to the db.
