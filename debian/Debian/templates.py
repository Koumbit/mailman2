# -*- python -*-
# $URL$
# $Id$
mm_cfg_defaults = '''\
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
are in /var/lib/mailman/Mailman/Defaults.py.  In mm_cfg, override only
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

'''

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
# If you change these, you have to configure your http server
# accordingly (Alias and ScriptAlias directives in most httpds)
DEFAULT_URL_PATTERN = %(DEFAULT_URL_PATTERN)r
# For logos on MM web pages, add this to your httpd config:
#   Alias %(IMAGE_LOGOS)s /usr/share/images/mailman/
IMAGE_LOGOS         = %(IMAGE_LOGOS)r

#-------------------------------------------------------------
# Default host for web interface of newly created MLs
DEFAULT_URL_HOST   = %(DEFAULT_URL_HOST)r
#-------------------------------------------------------------
# Default domain for email addresses of newly created MLs
DEFAULT_EMAIL_HOST = %(DEFAULT_EMAIL_HOST)r
#-------------------------------------------------------------
# Required when setting any of its arguments.
add_virtualhost(DEFAULT_URL_HOST, DEFAULT_EMAIL_HOST)

#-------------------------------------------------------------
# The default language for this server (may be changed to a
# supported language when mailman-i18n is installed).
DEFAULT_SERVER_LANGUAGE = %(DEFAULT_SERVER_LANGUAGE)r

#-------------------------------------------------------------
# Don't use address from envelope instead of from headers when
# determining if a message comes from a list member.
USE_ENVELOPE_SENDER    = %(USE_ENVELOPE_SENDER)r

#-------------------------------------------------------------
# By default don't send monthly password reminders for newly
# created lists.
DEFAULT_SEND_REMINDERS = %(DEFAULT_SEND_REMINDERS)r

#-------------------------------------------------------------
# Uncomment this if you configured your MTA such that it
# automatically recognizes newly created lists.
# (see /usr/share/doc/mailman/README.{EXIM,...})
# MTA=None   # Misnomer, suppresses alias output on newlist

#-------------------------------------------------------------
# Uncomment if you use Postfix virtual domains, but be sure to
# read /usr/share/doc/mailman/README.POSTFIX first.
# MTA='Postfix'

# Note - if you're looking for something that is imported from mm_cfg, but you
# didn't find it above, it's probably in /usr/lib/mailman/Mailman/Defaults.py.

#-------------------------------------------------------------
# Local settings not managed by Debian maintainer scripts. 
# only variables not mentioned above are preserved on package
# upgrade. If you define variables mentioned above here,
# the last setting here will be used above and occurrences
# below are removed.
'''
