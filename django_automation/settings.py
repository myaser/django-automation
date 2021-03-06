import os


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Settings(object):

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.path.pardir))
    REQUIREMENTS_ROOT = os.path.join(PROJECT_ROOT, 'requirements/')

    LOCAL = 1
    DEPLOYMENT = 0

    virtual_env_path = ''
    environment = ''

    def set_virtual_env_path(self, path):
        self.virtual_env_path = path

    def get_virtual_env_path(self):
        return self.virtual_env_path

    def set_environment(self, env, virtual_env='/var/venv/kotob/'):
        if env == self.LOCAL:
            self.set_virtual_env_path(virtual_env)

        elif env == self.DEPLOYMENT:
            self.set_virtual_env_path(virtual_env)

        else:
            raise ValueError('please use the constants Settings.LOCAL or Settings.DEPLOYMENT')

        self.environment = env

    def get_environment(self):
        return self.environment

    @property
    def is_local(self):
        if not self.environment:
            return
        if self.environment == self.LOCAL:
            return True
        else:
            return False


s = Settings()