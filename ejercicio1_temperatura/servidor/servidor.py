from concurrent import futures
import math

import grpc

import temperatura_pb2
import temperatura_pb2_grpc


class Conversor(temperatura_pb2_grpc.ConversorServicer):
    def CelsiusAFahrenheit(self, request, context):
        celsius = request.celsius

        print(f"[Servidor] Solicitud recibida: {celsius} °C", flush=True)

        #valido por las dudas 
        if math.isnan(celsius) or math.isinf(celsius):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "La temperatura debe ser un número finito.",
            )

        # parte logica
        fahrenheit = celsius * 1.8 + 32

        print(f"[Servidor] Resultado: {fahrenheit} °F", flush=True)

        return temperatura_pb2.RespuestaTemperatura(
            celsius=celsius,
            fahrenheit=fahrenheit,
        )


def main():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    temperatura_pb2_grpc.add_ConversorServicer_to_server(
        Conversor(), servidor
    )

    servidor.add_insecure_port("0.0.0.0:50051")
    servidor.start()

    print("[Servidor] Escuchando en el puerto 50051.", flush=True)

    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Servidor] Deteniendo servidor...", flush=True)
        servidor.stop(3).wait()


if __name__ == "__main__":
    main()
