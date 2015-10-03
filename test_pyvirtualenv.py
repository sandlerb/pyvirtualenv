import os
import platform
import unittest
import tempfile

from pyvirtualenv import Virtualenv


class PyVirtualenvTests(unittest.TestCase):

    def test_construct(self):
        ve = Virtualenv()
        self.assertTrue(ve is not None)
        ve.destroy()

    def test_construct_makes_virtualenv(self):
        temp_env = tempfile.mkdtemp()
        ve = Virtualenv(name=temp_env)
        temp_env_bin = os.path.join(
            temp_env, 'Scripts' if platform.system() == 'Windows' else 'bin')
        try:
            self.assertTrue('activate' in os.listdir(temp_env_bin))
        finally:
            ve.destroy()

    def test_destroy_removes_virtualenv(self):
        ve = Virtualenv()
        temp_env = ve.name
        ve.destroy()
        self.assertFalse(os.path.isdir(temp_env))

    def test_run_runs_in_virtualenv(self):
        ve = Virtualenv()
        try:
            output = ve.run('which python', shell=True)
            self.assertTrue(ve.name in output)
        finally:
            ve.destroy()

    def test_use_existing_virtualenv(self):
        venv = tempfile.mkdtemp()
        os.system('virtualenv %s' % venv)
        ve = Virtualenv(name=venv)
        try:
            output = ve.run('which python', shell=True)
            self.assertTrue(ve.name in output)
        finally:
            ve.destroy()

    def test_run_in_with_statement(self):
        temp_venv = None
        with Virtualenv() as ve:
            temp_venv = ve.name
            output = ve.run('which python', shell=True)
            self.assertTrue(ve.name in output)

        self.assertFalse(os.path.isdir(temp_venv))

    def test_context_manager_removes_virtualenv(self):
        temp_venv = None
        with Virtualenv() as ve:
            temp_venv = ve.name

        self.assertFalse(os.path.isdir(temp_venv))

if __name__ == "__main__":
    unittest.main()
