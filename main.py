from concurrent import futures
import logging
import grpc
from db import db
from services.project import ProjectEmbeddingService
from services.user import UserEmbeddingService
from generated import findme_pb2_grpc, findme_pb2
from grpc_reflection.v1alpha import reflection


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {message}",
    style="{",
)


def serve():
    db.QDRANT_CLIENT = db.qdrant_client_connect()
    db.ensure_collections(db.QDRANT_CLIENT)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    findme_pb2_grpc.add_UserEmbeddingServiceServicer_to_server(
        UserEmbeddingService(), server
    )

    findme_pb2_grpc.add_ProjectEmbeddingServiceServicer_to_server(
        ProjectEmbeddingService(), server
    )

    SERVICE_NAMES = (
        findme_pb2.DESCRIPTOR.services_by_name["UserEmbeddingService"].full_name,
        findme_pb2.DESCRIPTOR.services_by_name["ProjectEmbeddingService"].full_name,
        reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:8000")
    server.start()
    logging.info("[gRPC] Server started on port 8000")
    server.wait_for_termination()


serve()
