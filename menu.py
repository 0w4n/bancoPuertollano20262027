from cliente import cargarCliente
from logs import Log
import os
import sys

# Configuración para lectura de teclas sin dependencias externas
if os.name == 'nt':
    import msvcrt
    def get_key():
        # En Windows, las flechas devuelven una secuencia de dos bytes (0xE0 o 0x00 seguido de la tecla)
        c = msvcrt.getch()
        if c in b'\x00\xe0':
            c2 = msvcrt.getch()
            if c2 == b'H': return 'UP'
            if c2 == b'P': return 'DOWN'
        elif c == b'\r':
            return 'ENTER'
        return None
else:
    import termios
    import tty
    def get_key():
        # En Linux/macOS configuramos la terminal en modo raw para leer las teclas al vuelo
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                if ch2 == '[':
                    if ch3 == 'A': return 'UP'
                    if ch3 == 'B': return 'DOWN'
            elif ch == '\r' or ch == '\n':
                return 'ENTER'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

log = Log()

def menu():
    opciones = [
        "1) Cargar Datos Cliente",
        "2) Consultar cuenta Deposito",
        "3) Listar clientes cargados",
        "4) Salir"
    ]
    
    seleccion = 0

    # Limpiamos la pantalla inicialmente (opcional)
    print("\033[2J\033[H", end="")

    while True:
        # Movemos el cursor al inicio para sobrescribir el menú y evitar parpadeos molestos
        print("\033[H", end="")
        print("--- MENÚ PRINCIPAL (Usa las flechas Arriba/Abajo y pulsa Enter) ---\n")

        for i, opcion in enumerate(opciones):
            if i == seleccion:
                # Código ANSI para subrayar solo el número (ej: '\033[4m1\033[24m')
                numero = opcion[0]
                resto = opcion[1:]
                opcion_subrayada = f"\033[4m{numero}\033[24m{resto}"
                print(f" > {opcion_subrayada}")
            else:
                print(f"   {opcion}")

        print("\n" + " " * 50) # Línea de limpieza para rastros anteriores

        key = get_key()

        if key == 'UP':
            seleccion = (seleccion - 1) % len(opciones)
        elif key == 'DOWN':
            seleccion = (seleccion + 1) % len(opciones)
        elif key == 'ENTER':
            # Limpiamos antes de ejecutar la opción para que la salida en consola sea limpia
            print("\033[2J\033[H", end="")
            
            opt = str(seleccion + 1)

            if opt == "1":
                cargarCliente("movimientos")

            elif opt == "2":
                cliente = cargarCliente("guardado")
                if cliente is not None:
                    log.escribir("INFO", f"CONSULTA DATOS CLIENTE CON NÚMERO: {cliente.numero}")
                    print(f"Cliente: {cliente.numero}")
                    print(f"Saldo cuenta: {cliente.cuenta.saldo} €")
                    print(f"Saldo depósito: {cliente.deposito.saldo} €")
                    print(f"Saldo total: {cliente.getSaldoTotal()} €")
                else:
                    print("No se ha podido cargar el cliente.")

            elif opt == "3":
                log.escribir("INFO", "LISTADO DE CLIENTES CARGADOS")
                print("Clientes cargados:")
                if os.path.exists("datosClientes"):
                    for filename in os.listdir("datosClientes"):
                        if filename.endswith(".txt"):
                            numero_cliente = filename.split(".")[0]
                            print(f"- Cliente número: {numero_cliente}")
                else:
                    print("La carpeta 'datosClientes' no existe.")

            elif opt == "4":
                log.escribir("INFO", "FIN EJECUCIÓN")
                print("Hasta pronto")
                break

            input("\nPresiona Enter para volver al menú...")
            print("\033[2J\033[H", end="") # Limpiar pantalla al volver al menú