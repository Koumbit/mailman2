# $URL$
# $Id$
#
# At 8AM every day, mail reminders to admins as to pending requests.
# They are less likely to ignore these reminders if they're mailed
# early in the morning, but of course, this is local time... ;)
0 8 * * * list /var/lib/mailman/cron/checkdbs
#
# At 9AM, send notifications to disabled members that are due to be
# reminded to re-enable their accounts.
0 9 * * * list /var/lib/mailman/cron/disabled
#
# Noon, mail digests for lists that do periodic as well as threshhold delivery.
0 12 * * * list /var/lib/mailman/cron/senddigests
#
# 5 AM on the first of each month, mail out password reminders.
0 5 1 * * list /var/lib/mailman/cron/mailpasswds
#
# Every 5 mins, try to gate news to mail.  You can comment this one out
# if you don't want to allow gating, or don't have any going on right now,
# or want to exclusively use a callback strategy instead of polling.
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * list /var/lib/mailman/cron/gate_news
#
# At 3:27am every night, regenerate the gzip'd archive file.  Only
# turn this on if the internal archiver is used and
# GZIP_ARCHIVE_TXT_FILES is false in mm_cfg.py
27 3 * * * list /var/lib/mailman/cron/nightly_gzip
