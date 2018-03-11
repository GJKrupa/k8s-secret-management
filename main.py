import click
from click import BadParameter

from lib.secrets import Secrets

secrets = Secrets()


def print_affected(affected):
    for secret in affected.keys():
        print 'Secret ' + secret + ' has been generated and needs to be applied'


@click.group()
def main():
    pass


@click.command(help="Generate or re-generate one or more values")
@click.option("--namespace", "-n", required=True, help="k8s namespace")
@click.option("--secret", "-s", help="Secret name (optional)")
@click.option("--value", "-v", help="Value name (optional)")
def generate(namespace, secret, value):
    if secret is None and value is not None:
        raise BadParameter("Cannot specify value without secret")
    print_affected(secrets.generate(namespace, secret, value))


@click.command("set", help="Set the content of a non-generated value")
@click.option("--namespace", "-n", required=True, help="k8s namespace")
@click.option("--secret", "-s", required=True, help="Secret name")
@click.option("--value", "-v", required=True, help="Value name")
@click.option("--file", "-f", help="File from which to read data")
@click.argument("content", required=False)
def set_value(secret, namespace, value, file, content):
    if file is None and content is None:
        raise BadParameter("Please specify either --file or CONTENT")
    elif file is not None and content is not None:
        raise BadParameter("--file and CONTENT are mutually exclusive")

    if file is not None:
        print_affected(secrets.set_from_file(namespace, secret, value, file))
    elif content is not None:
        print_affected(secrets.set_from_text(namespace, secret, value, content))


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