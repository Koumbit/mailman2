# -*- python -*-
# $URL$
# $Id$

mm_cfg_defaults = '''\
# Mailman site configuration for Debian automatically generated from
# $URL$
# $Id$
#
# Copyright (C) 1998,1999,2000 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


"""This is the module which takes your site-specific settings.

From a raw distribution it should be copied to mm_cfg.py.  If you
already have an mm_cfg.py, be careful to add in only the new settings
you want.  The complete set of distributed defaults, with annotation,
are in /usr/lib/mailman/Mailman/Defaults.py.  In mm_cfg, override only
those you want to change, after the

  from Defaults import *

line (see below).

Note that these are just default settings - many can be overridden via the
admin and user interfaces on a per-list or per-user basis.

Note also that some of the settings are resolved against the active list
setting by using the value as a format string against the
list-instance-object's dictionary - see the distributed value of
DEFAULT_MSG_FOOTER for an example."""


#######################################################
#    Here's where we get the distributed defaults.    #

from Defaults import *

'''#

mm_cfg_fillin = '''\
##############################################################
# Put YOUR site-specific configuration below, in mm_cfg.py . #
# See Defaults.py for explanations of the values.            #

#-------------------------------------------------------------
# The name of the list Mailman uses to send password reminders
# and similar. Don't change if you want mailman-owner to be
# a valid local part.
MAILMAN_SITE_LIST = %(MAILMAN_SITE_LIST)r

#-------------------------------------------------------------
# Virtual host httpd setup, if you don't use a virtual host
# just copy the ScriptAlias and Alias directives.
#
# <Virtualhost %(DEFAULT_URL_HOST)s>
#   ServerName  %(DEFAULT_URL_HOST)s
#   ScriptAlias %(default_url_path)s /usr/lib/cgi-bin/mailman/
#   Alias       /pipermail/ %(PUBLIC_ARCHIVE_FILE_DIR)s/
#   Alias       %(IMAGE_LOGOS)s /usr/share/images/mailman/
# </VirtualHost>
#-------------------------------------------------------------
DEFAULT_URL_HOST   = %(DEFAULT_URL_HOST)r
DEFAULT_EMAIL_HOST = %(DEFAULT_EMAIL_HOST)r
add_virtualhost(DEFAULT_URL_HOST, DEFAULT_EMAIL_HOST)
DEFAULT_URL_PATTERN = %(DEFAULT_URL_PATTERN)r
IMAGE_LOGOS         = %(IMAGE_LOGOS)r

#-------------------------------------------------------------
# Depending on your MTA setup, the MTA configuration variable
# controls how aliases are generated.
# At the time of this writing legal values are:
# None      - your MTA automatically recognizes new lists
# 'Postfix' - you are using postfix virtual domains
# 'Manual'  - default, meaning you have to manually create the
#             aliases in /etc/aliases or similar.
# In any case, please read the MTA specific README.* in
# /usr/share/doc/mailman before setting this.
MTA=%(MTA)r

#-------------------------------------------------------------
# The USE_ENVELOPE_SENDER variable controls the order in which
# headers are searched when determining if a message originates
# from a subscriber.  When True, the order is Sender:, From:,
# unixfrom, when False it is From:, Sender:, unixfrom.  In both
# cases the first address encountered is used.
# Debian default is not to use the envelope address when
# determining if a message comes from a subscriber.
# This option applies globally to all mailing lists.
USE_ENVELOPE_SENDER    = %(USE_ENVELOPE_SENDER)r

#-------------------------------------------------------------
# Debian default is not to send monthly password reminders
# on newly created lists.  This can be changed per list.
DEFAULT_SEND_REMINDERS = %(DEFAULT_SEND_REMINDERS)r

#-------------------------------------------------------------
# The default language for this server (may be changed to a
# supported language when mailman-i18n is installed).
DEFAULT_SERVER_LANGUAGE = %(DEFAULT_SERVER_LANGUAGE)r

# Note - if you're looking for something that is imported from mm_cfg, but you
# didn't find it above, it's probably in /usr/lib/mailman/Mailman/Defaults.py.
'''#

mm_crontab = '''\
# Mailman crontab for Debian automatically generated from
# $URL$
# $Id$
#
# At 8AM every day, mail reminders to admins as to pending requests.
# They are less likely to ignore these reminders if they're mailed
# early in the morning, but of course, this is local time... ;)
0 8 * * * list /usr/lib/mailman/cron/checkdbs
#
# At 9AM, send notifications to disabled members that are due to be
# reminded to re-enable their accounts.
0 9 * * * list /usr/lib/mailman/cron/disabled
#
# Noon, mail digests for lists that do periodic as well as threshhold delivery.
0 12 * * * list /usr/lib/mailman/cron/senddigests
#
# 5 AM on the first of each month, mail out password reminders.
0 5 1 * * list /usr/lib/mailman/cron/mailpasswds
#
# Every 5 mins, try to gate news to mail.  You can comment this one out
# if you don't want to allow gating, or don't have any going on right now,
# or want to exclusively use a callback strategy instead of polling.
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * list /usr/lib/mailman/cron/gate_news
#
# At 3:27am every night, regenerate the gzip'd archive file.  Only
# turn this on if the internal archiver is used and
# GZIP_ARCHIVE_TXT_FILES is false in mm_cfg.py
27 3 * * * list /usr/lib/mailman/cron/nightly_gzip
'''#
