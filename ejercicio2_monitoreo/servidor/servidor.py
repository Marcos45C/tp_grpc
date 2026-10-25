from concurrent import futures
import shutil
import time

import grpc
import psutil

import monitoreo_pb2
import monitoreo_pb2_grpc


CANTIDAD_REPORTES = 5
INTERVALO_SEGUNDOS = 2


class MonitorServidor(monitoreo_pb2_grpc.MonitorServidorServicer):
    def Monitorear(self, request, context):
        print("Servidor Solicitud de monitoreo recibida.", flush=True)
        psutil.cpu_percent(interval=None)

        for numero in range(1, CANTIDAD_REPORTES + 1):
            time.sleep(INTERVALO_SEGUNDOS)

            # por si el cliente cancela la llamada, se termina la función y gRPC cierra la llamada con estado CANCELLED.
            if not context.is_active():
                print("[Servidor] El cliente canceló la llamada.", flush=True)
                return

            try:
                cpu = psutil.cpu_percent(interval=None)
                ram_mb = psutil.virtual_memory().available // (1024 ** 2)
                disco_gb = shutil.disk_usage("/").free // (1024 ** 3)
            except Exception as ex:
                context.abort(
                    grpc.StatusCode.INTERNAL,
                    f"No se pudieron leer las métricas: {ex}",
                )

            print(f"[Servidor] Enviando reporte {numero}.", flush=True)

            
            yield monitoreo_pb2.ReporteEstado(
                numero=numero,
                cpu_porcentaje=cpu,
                ram_disponible_mb=ram_mb,
                disco_disponible_gb=disco_gb,
            )

        # al terminar avisamos al cliente que ya no habrá más reportes, cerrando el stream de respuesta.
        print("[Servidor] Monitoreo finalizado.", flush=True)


def main():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    monitoreo_pb2_grpc.add_MonitorServidorServicer_to_server(
        MonitorServidor(), servidor
    )

    servidor.add_insecure_port("0.0.0.0:50052")
    servidor.start()

    print("[Servidor] Escuchando en el puerto 50052.", flush=True)

    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Servidor] Deteniendo servidor...", flush=True)
        servidor.stop(3).wait()


if __name__ == "__main__":
    main()
