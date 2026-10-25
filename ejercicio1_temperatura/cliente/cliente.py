import math
import grpc
import temperatura_pb2
import temperatura_pb2_grpc


IP_SERVIDOR = "192.168.1.14"
PUERTO = 50051


def pedir_temperatura():
    while True:
        texto = input("ingresa una temperatura en °C: ").strip()
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            print("Error: debés ingresar un numero")
            continue

        if math.isnan(valor) or math.isinf(valor):
            print("Error: debés ingresar un numero finito")
            continue

        return valor


def main():
    celsius = pedir_temperatura()

    destino = f"{IP_SERVIDOR}:{PUERTO}"

    with grpc.insecure_channel(destino) as canal:
        stub = temperatura_pb2_grpc.ConversorStub(canal)

        solicitud = temperatura_pb2.SolicitudTemperatura(celsius=celsius)

        try:
            respuesta = stub.CelsiusAFahrenheit(solicitud, timeout=5)
        except grpc.RpcError as error:
            print(f"Error gRPC [{error.code().name}]: {error.details()}")
            return

    print(f"{respuesta.celsius:g} °C = {respuesta.fahrenheit:.2f} °F")


if __name__ == "__main__":
    main()
