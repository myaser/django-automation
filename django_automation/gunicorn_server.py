from deployment import tasks_runner_factory


def restart_server():
    runner = tasks_runner_factory.get_fabric_method(super=True)
    # TODO: gunicorn-kotob environment variable should be set
    runner.execute('service gunicorn-kotob restart')