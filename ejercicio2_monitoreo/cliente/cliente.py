import grpc

import monitoreo_pb2
import monitoreo_pb2_grpc


IP_SERVIDOR = "192.168.1.14"
PUERTO = 50052


def main():
    input("presione Enter para consultar el estado del servidor..")

    destino = f"{IP_SERVIDOR}:{PUERTO}"

    with grpc.insecure_channel(destino) as canal:
        stub = monitoreo_pb2_grpc.MonitorServidorStub(canal)

        try:
            reportes = stub.Monitorear(
                monitoreo_pb2.SolicitudMonitoreo(),
                timeout=30,
            )
            for reporte in reportes:
                print(f"\nReporte {reporte.numero}")
                print(f"CPU en uso: {reporte.cpu_porcentaje:.0f} %")
                print(f"RAM disponible: {reporte.ram_disponible_mb} MB")
                print(f"Disco disponible: {reporte.disco_disponible_gb} GB")

        except grpc.RpcError as error:
            print(f"\nError gRPC [{error.code().name}]: {error.details()}")
            return

    print("\nMonitoreo finalizado.")


if __name__ == "__main__":
    main()
