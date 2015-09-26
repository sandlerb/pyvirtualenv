import os
import shutil
import platform
import tempfile


__version__ = '0.1.0'


class Virtualenv(object):

    def __init__(self, virtualenv=None, runner=None):
        super(Virtualenv, self).__init__()
        if runner is None:
            runner = os.system
        self.run = runner

        if virtualenv is None:
            # TODO guarantee that this dir is empty, should be
            virtualenv = tempfile.mkdtemp()
        # TODO only create if doesn't exist
        Virtualenv._create_virtualenv(virtualenv)
        self.virtualenv = virtualenv

    @property
    def _bin_path(self):
        return os.path.join(
            self.virtualenv,
            'Scripts' if platform.system() == 'Windows' else 'bin')

    @property
    def _activate_string(self):
        activate_path = os.path.join(self._bin_path, 'activate')
        if platform.system == 'Windows':
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

    def run(self, command):
        """
        Run a command in the virtualenv represented by this object

        command -- A string reprsenting the command to be run
        """
        # if the user has called activate(), we probably don't want all of this
        os.system("{activate} && {command}".format(
            activate=self._activate_string, command=command))

    @staticmethod
    def _is_virtualenv(path):
        path_bin = os.path.join(
            path, 'Scripts' if platform.system() == 'Windows' else 'bin')
        if not os.path.isdir(path) or 'activate' not in path_bin:
            return False
        return True

    @staticmethod
    def in_virtualenv():
        """Returns True/False is a virtualenv is activated"""
        return 'VIRTUAL_ENV' in os.environ

    @staticmethod
    def _create_virtualenv(name):
        """Create a new virtualenv"""
        # TODO add support for CLI switches and args
        # TODO check if it already exists and is a virtualenv
        os.system("virtualenv {name}".format(name=name))

    @staticmethod
    def _destroy_virtualenv(name):
        """Remove a virtualenv from the filesystem"""
        shutil.rmtree(name)

    def destroy(self):
        """Remove the virtualenv represented by this object from the
        file system"""
        # TODO call deactivate()
        Virtualenv._destroy_virtualenv(self.virtualenv)
        self.virtualenv = None
