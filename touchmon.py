#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, print_function

import sys
import os
import time
import subprocess

try:
    import ujson as json
except ImportError:
    import json

import pyinotify

MASK = pyinotify.IN_CLOSE_WRITE


class TouchHandler(pyinotify.ProcessEvent):
    def __init__(self, actions):
        super(TouchHandler, self).__init__()

        self._actions = actions
        now = time.time()
        self._mtimes = {k: now for k in actions.iterkeys()}

    def process_IN_CLOSE_WRITE(self, event):
        #print event
        #print event.pathname
        fname = event.pathname
        s = os.stat(fname)
        if s.st_mtime > self._mtimes[fname]:
            # mtime newer than previous examination
            self._mtimes[fname] = s.st_mtime
            # print fname
            chld = subprocess.Popen(self._actions[fname], env={})
            chld.communicate()


def main(argv):
    # read in action files
    if len(argv) < 2:
        print(
                'usage: %s <list of action files>' % (
                    argv[0],
                    ),
                file=sys.stderr,
                )
        return 127

    actions = {}
    for path in argv[1:]:
        with open(path, 'rb') as fp:
            action_content = fp.read()
        actions.update(json.loads(action_content))

    wm = pyinotify.WatchManager()
    handler = TouchHandler(actions)
    notifier = pyinotify.Notifier(wm, handler)

    wdd = {}
    for fname in actions.iterkeys():
        wdd.update(wm.add_watch(fname, MASK))

    notifier.loop()

    #wm.rm_watch(wdd.values())
    #notifier.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
