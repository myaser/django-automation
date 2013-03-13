import os
from fabric.api import run, sudo, local
from deployment.settings import s


class FabricMethodFactory():
    def get_fabric_method(self, super=False):
        # use fabric environment variables
        if s.is_local:
            if super:
                return DevelopmentSuperMethod()
            else:
                return DevelopmentMethod()

        else:
            if super:
                return ProductionSuperMethod()
            else:
                return ProductionMethod()


class FabricMethod():
    def execute(self, command, shell=None):
        raise NotImplementedError()


class DevelopmentMethod(FabricMethod):
    def execute(self, command, shell=None, capture=False):
        return local(command, shell=shell, capture=capture)


class DevelopmentSuperMethod(DevelopmentMethod):
    def execute(self, command, shell=None, capture=False):
        command = 'sudo ' + command
        return DevelopmentMethod.execute(self, command, shell=shell, capture=capture)


class ProductionSuperMethod(FabricMethod):
    def execute(self, command, shell=True):
        return sudo(command, shell=shell)


class ProductionMethod(FabricMethod):
    def execute(self, command, shell=True):
        return run(command, shell=shell)

tasks_runner_factory = FabricMethodFactory()