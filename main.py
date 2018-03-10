import click

from lib.secrets import Secrets


secrets = Secrets()


@click.group()
def main():
    pass


@click.command(help="Generate or re-generate one or more values")
def generate():
    affected_secrets = secrets.generate()
    for secret in affected_secrets:
        print secret + " must be run into k8s"


@click.command("set", help="Set the content of a non-generated value")
def set_value():
    raise NotImplementedError("Not implemented")


@click.command(help="Check if secrets can be generated")
def check():
    raise NotImplementedError("Not implemented")


@click.command(help="Export secrets to the terminal")
def export():
    raise NotImplementedError("Not implemented")


@click.command(help="Run secrets into a Kubernetes environment")
def run():
    raise ValueError("Not implemented")


main.add_command(generate)
main.add_command(set_value)
main.add_command(check)
main.add_command(export)
main.add_command(run)

if __name__ == '__main__':
    main()