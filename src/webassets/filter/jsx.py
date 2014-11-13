from __future__ import print_function
import os
import subprocess

from webassets.filter import Filter
from webassets.exceptions import FilterError


__all__ = ('JSXScript',)


class JSXScript(Filter):
    """Converts JSX (from Facebook's React) to real JavaScript."""

    name = 'jsx'
    options = {
        'binary': 'JSX_BIN',
        'extra_args': 'JSX_EXTRA_ARGS',
    }

    def output(self, _in, out, **kw):
        binary = self.binary or 'jsx'
        args = [binary]
        if self.extra_args:
            args.extend(self.extra_args)

        try:
            proc = subprocess.Popen(args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=(os.name == 'nt'))
        except OSError as e:
            if e.errno == 2:
                raise Exception("jsx not installed or in system path for webassets")
            raise
        stdout, stderr = proc.communicate(_in.read().encode('utf-8'))
        if proc.returncode != 0:
            raise FilterError(('jsx: subprocess had error: stderr=%s, '
                               'stdout=%s, returncode=%s') % (
                stderr, stdout, proc.returncode))
        elif stderr:
            print("jsx filter has warnings:", stderr)
        out.write(stdout.decode('utf-8'))
