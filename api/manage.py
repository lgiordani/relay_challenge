#! /usr/bin/env python

import json
import os
import signal
import subprocess

import click


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


setenv("RELAY_API_ENVIRONMENT", "development")


def configure_app(config):
    env_configuration_file = os.path.join("config", f"{config}.json")

    config_data = {}

    if os.path.isfile(env_configuration_file):
        # Read configuration from the relative JSON file
        with open(env_configuration_file) as f:
            config_data = json.load(f)

        # Convert the config into a usable Python dictionary
        config_data = dict((i["name"], i["value"]) for i in config_data)

    for key, value in config_data.items():
        setenv(key, value)


def run_local_commands(commands, arguments_list=[]):
    # Run each command line in a list
    for command in commands:
        cmdline = command.split()
        cmdline.extend(arguments_list)
        subprocess.call(cmdline)


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    configure_app(os.getenv("RELAY_API_ENVIRONMENT"))

    cmdline = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def docker_compose_cmdline(config):
    configure_app(os.getenv("RELAY_API_ENVIRONMENT"))

    docker_compose_file = os.path.join("docker", f"{config}.yml")

    if not os.path.isfile(docker_compose_file):
        raise ValueError(f"The file {docker_compose_file} does not exist")

    return [
        "docker",
        "compose",
        "-p",
        config,
        "-f",
        docker_compose_file,
    ]


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = docker_compose_cmdline(os.getenv("RELAY_API_ENVIRONMENT")) + list(
        subcommand
    )

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
    configure_app("testing")

    file_commands = [
        "pytest -svvl -m unit --cov=src --cov-report=term-missing",
    ]

    global_commands = [
        "mypy src tests",
    ]

    run_local_commands(file_commands, filenames)
    run_local_commands(global_commands)


def _e2e_test(filenames):
    configure_app("development")

    run_local_commands(["pytest -svvl -m e2e"], filenames)


@cli.command()
@click.argument("filenames", nargs=-1)
def e2e_test(filenames):
    cmdline = docker_compose_cmdline("development") + [
        "up",
        "-d",
        "--build",
    ]
    subprocess.call(cmdline)

    _e2e_test(filenames)

    cmdline = docker_compose_cmdline("development") + ["down"]
    subprocess.call(cmdline)


@cli.command()
@click.argument("filenames", nargs=-1)
def e2e_test_nocompose(filenames):
    _e2e_test(filenames)


@cli.command()
def tidy():
    targets = ["src", "tests", "manage.py"]

    commands = ["flake8", "black --check", "isort --check-only"]

    commands = [f"{command} {' '.join(targets)}" for command in commands]

    run_local_commands(commands)


if __name__ == "__main__":
    cli()
