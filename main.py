from concurrent import futures
import logging
import grpc
from services.project import ProjectEmbeddingService
from services.user import UserEmbeddingService
from generated import findme_pb2_grpc


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {message}",
    style="{",
)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    findme_pb2_grpc.add_UserEmbeddingServiceServicer_to_server(
        UserEmbeddingService, server
    )

    findme_pb2_grpc.add_ProjectEmbeddingServiceServicer_to_server(
        ProjectEmbeddingService, server
    )

    server.add_insecure_port("[::]:8000")
    server.start()
    logging.info("[gRPC] Server started on port 8000")
    server.wait_for_termination()


serve()
