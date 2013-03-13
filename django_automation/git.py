from deployment import tasks_runner_factory


def pull():
    runner = tasks_runner_factory.get_fabric_method()
    runner.execute('git pull')