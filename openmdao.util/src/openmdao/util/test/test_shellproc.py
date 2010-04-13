"""
Test ShellProc functions.
"""

import logging
import os.path
import sys
import unittest

from openmdao.util.shellproc import call, check_call, CalledProcessError


class TestCase(unittest.TestCase):
    """ Test ShellProc functions. """

    def test_call(self):
        logging.debug('')
        logging.debug('test_call')

        cmd = 'dir' if sys.platform == 'win32' else 'ls'
        try:
            return_code, error_msg = call(cmd, stdout='stdout', stderr='stderr')
            self.assertEqual(os.path.exists('stdout'), True)
            self.assertEqual(os.path.exists('stderr'), True)
        finally:
            if os.path.exists('stdout'):
                os.remove('stdout')
            if os.path.exists('stderr'):
                os.remove('stderr')
 
    def test_check_call(self):
        logging.debug('')
        logging.debug('test_check_call')

        cmd = 'dir' if sys.platform == 'win32' else 'ls'
        try:
            check_call(cmd, stdout='stdout', stderr='stderr')
            self.assertEqual(os.path.exists('stdout'), True)
            self.assertEqual(os.path.exists('stderr'), True)
        finally:
            if os.path.exists('stdout'):
                os.remove('stdout')
            if os.path.exists('stderr'):
                os.remove('stderr')

        try:
            check_call('no-such-command', stdout='stdout', stderr='stderr')
            self.assertEqual(os.path.exists('stdout'), True)
            self.assertEqual(os.path.exists('stderr'), True)
        except CalledProcessError, exc:
            msg = "Command 'no-such-command' returned non-zero exit status"
            self.assertEqual(str(exc)[:len(msg)], msg)
        else:
            self.fail('Expected CalledProcessError')
        finally:
            if os.path.exists('stdout'):
                os.remove('stdout')
            if os.path.exists('stderr'):
                os.remove('stderr')


if __name__ == '__main__':
    import nose
    sys.argv.append('--cover-package=openmdao')
    sys.argv.append('--cover-erase')
    nose.runmodule()
