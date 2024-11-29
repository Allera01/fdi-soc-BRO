import descarga
import anlalisis
import click

@click.command(
    help="\n"
)  # Define el comando principal
@click.argument("file", type=click.File("r"))
@click.option(
    "-a", "--all", is_flag=True, help="Se ejecutan todas las funciones.\n"
)
# Define argumentos que el usuario debe pasar (en este caso, el archivo de lista de aristas)
def my_main(file, all):
    print("hola")

if __name__ == "__main__":
    my_main()