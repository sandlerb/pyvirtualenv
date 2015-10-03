import os
import shutil
import platform
import tempfile
import subprocess

__version__ = '0.1.0'


class Virtualenv(object):

    def __init__(self, name=None, runner=None):
        if runner is None:
            runner = subprocess.check_output
        self._runner = runner

        if name is None:
            name = tempfile.mkdtemp()

        if not Virtualenv._is_virtualenv(name):
            Virtualenv._create_virtualenv(name)

        self.name = name

    @property
    def _bin_path(self):
        return os.path.join(
            self.name,
            'Scripts' if platform.system() == 'Windows' else 'bin')

    @property
    def _activate_string(self):
        activate_path = os.path.join(self._bin_path, 'activate')
        if platform.system() == 'Windows':
            return os.path.join('.', activate_path)
        else:
            return 'source {0}'.format(activate_path)

    def activate(self):
        """Activates the virtualenv in the current interpreter"""
        # TODO check if already activated
        activate_this = os.path.join(self._bin_path, 'activate_this.py')
        execfile(activate_this, dict(__file__=activate_this))

    def deactivate(self):
        # could just remove all paths with self.virtualenv from path, etc
        if os.path.abspath(self._bin_path) in os.environ['PATH']:
            print "in path"
        raise NotImplementedError()

    def run(self, command, *args, **kwargs):
        """
        Run a command in the virtualenv represented by this object

        command -- A string reprsenting the command to be run
        """
        # if the user has called activate(), we probably don't want all of this
        activate = "{activate} && {command}".format(
            activate=self._activate_string, command=command)
        # TODO other runners will break from the **kwargs (i.e. os.system)
        return self._runner(activate, *args, **kwargs)

    @staticmethod
    def _is_virtualenv(path):
        if platform.system() == 'Windows':
            contents = ['Scripts', 'include', 'Lib']
        else:
            contents = ['bin', 'include', 'lib']
        if not set(contents).issubset(set(os.listdir(path))):
            return False

        bin_path = os.path.join(
            path, 'Scripts' if platform.system() == 'Windows' else 'bin')
        if not os.path.isdir(path) or 'activate' not in os.listdir(bin_path):
            return False

        return True

    @staticmethod
    def in_virtualenv():
        """Returns True/False if a virtualenv is activated in the shell"""
        return 'VIRTUAL_ENV' in os.environ

    @staticmethod
    def _create_virtualenv(name):
        """Create a new virtualenv"""
        # TODO add support for CLI switches and args
        os.system("virtualenv {name}".format(name=name))

    @staticmethod
    def _destroy_virtualenv(name):
        """Remove a virtualenv from the filesystem"""
        shutil.rmtree(name)

    def destroy(self):
        """Remove the virtualenv represented by this object from the
        file system"""
        # TODO call deactivate()
        Virtualenv._destroy_virtualenv(self.name)
        self.name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        self.destroy()
