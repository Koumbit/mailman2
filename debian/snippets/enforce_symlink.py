#! /usr/bin/env python
# $URL$
# $Id$


import sys, os

VAR_PREFIX   = '/var/lib/mailman'

FHS_LOCK_DIR = '/var/lock'
FHS_LOG_DIR  = '/var/log'
FHS_RUN_DIR  = '/var/run'

# When upgrading from an old MM version, logdir and lockdir may still
# be in the /var/lib/mailman tree.

enforce_symlink(os.path.join(VAR_PREFIX, 'locks'),
                os.path.join(FHS_LOCK_DIR, 'mailman'))
enforce_symlink(os.path.join(VAR_PREFIX, 'logs'),
                os.path.join(FHS_LOG_DIR, 'mailman'))

def enforce_symlink(symlink, tgt_dir):
    """Make sure symlink is a symlink pointing to tgt_dir.

    When the directory is populated, move its contents to the
    new location before converting."""
    if os.isdir(symlink):
        files = os.listdir(symlink)
        if not files:
            os.rmdir(symlink)
        else:
            log('Moving files from directory %(symlink)s'
                ' to new location %(tgt_dir)s.' % locals())
            if os.stat(symlink)[ST_DEV] == os.stat(tgt_dir)[ST_DEV]:
                # same device, just rename
                for fn in os.listdir(symlink):
                    os.rename(os.path.join(symlink,fn),
                              os.path.join(tgt_dir,fn))
                    os.rmdir(symlink)
            else:
                # cross device, use tar pipe
                out, err = os.popen('tar cf - -C %(symlink)s . | '
                                    'tar xf - -C %(tgt_dir)s'
                                    % locals())
                if msgs.close() == 0:
                    os.system('rm -rf %(symlink)s' % locals())
        # TBD: Policy mandates a relative symlink
        log('Symlinking %(symlink)s to %(tgt_dir)s.' % locals())
        os.symlink(tgt_dir, symlink)

