import grpc
from qdrant_client.models import PointStruct
from db.db import get_qdrant_client
from generated import findme_pb2_grpc, findme_pb2


class UserEmbeddingService(findme_pb2_grpc.UserEmbeddingServiceServicer):
    def CreateUserEmbedding(self, request, context):
        try:
            user_id = request.user_id
            bio = request.bio
            skills = list(request.skills)
            interests = list(request.interests)

            client = get_qdrant_client()

            client.upsert(
                collection_name="users",
                points=[
                    PointStruct(
                        id=user_id,
                        vector=[],
                        payload={"bio": bio, "skills": skills, "interests": interests},
                    )
                ],
            )

            return findme_pb2.EmbeddingResponse(
                success=True, msg="Created successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return findme_pb2.EmbeddingResponse(success=False, msg=str(e))

    def UpdateUserEmbedding(self, request, context):
        user_id = request.user_id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="users", ids=[user_id])

            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {user_id} not found")
                return findme_pb2.EmbeddingResponse(
                    success=False, msg=f"User {user_id} not found"
                )

            bio = request.bio
            skills = list(request.skills)
            interests = list(request.interests)

            client.upsert(
                collection_name="users",
                points=[
                    PointStruct(
                        id=user_id,
                        vector=[],
                        payload={"bio": bio, "skills": skills, "interests": interests},
                    )
                ],
            )

            return findme_pb2.EmbeddingResponse(
                success=True, msg="Updated successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return findme_pb2.EmbeddingResponse(success=False, msg=str(e))

    def DeleteUserEmbedding(self, request, context):
        user_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="users", ids=[user_id])

            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {user_id} not found")
                return findme_pb2.EmbeddingResponse(
                    success=False, msg=f"User {user_id} not found"
                )

            client.delete(collection_name="users", points_selector=[user_id])

            return findme_pb2.EmbeddingResponse(
                success=True, msg="Deleted successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return findme_pb2.EmbeddingResponse(success=False, msg=str(e))
