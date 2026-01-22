import logging
import grpc
from qdrant_client.models import PointStruct
from db.db import get_qdrant_client
from generated import emb_pb2_grpc, emb_pb2
from model.embedding import generate_user_embedding


class UserEmbeddingService(emb_pb2_grpc.UserEmbeddingServiceServicer):
    def CreateUserEmbedding(self, request, context):
        """Creates and stores a vector embedding for a new user"""
        try:
            user_id = request.user_id
            bio = request.bio
            skills = list(request.skills)
            interests = list(request.interests)
            status = True

            client = get_qdrant_client()
            vector = generate_user_embedding(bio, skills, interests)

            client.upsert(
                collection_name="users",
                points=[
                    PointStruct(
                        id=user_id,
                        vector={"profile": vector},
                        payload={
                            "bio": bio,
                            "skills": skills,
                            "status": status,
                            "interests": interests,
                        },
                    )
                ],
            )

            logging.info(f"Added a vector embedding for user with id -> {user_id}")

            return emb_pb2.EmbeddingResponse(success=True, msg="Created successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to create a new user vector -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def UpdateUserEmbedding(self, request, context):
        """Updates the vector embedding of a user"""
        user_id = request.user_id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="users", ids=[user_id])

            if not existing:
                logging.info(f"Failed to fetch user with id -> {user_id} not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {user_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"User {user_id} not found"
                )

            bio = request.bio
            skills = list(request.skills)
            interests = list(request.interests)

            vector = generate_user_embedding(bio, skills, interests)

            client.upsert(
                collection_name="users",
                points=[
                    PointStruct(
                        id=user_id,
                        vector={"profile": vector},
                        payload={
                            "bio": bio,
                            "skills": skills,
                            "interests": interests,
                        },
                    )
                ],
            )

            logging.info(f"Updated the vector embedding of user with id -> {user_id}")

            return emb_pb2.EmbeddingResponse(success=True, msg="Updated successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to update the user vector with id -> {user_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def UpdateUserStatus(self, request, context):
        """Updates the status payload of a user vector"""
        user_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="users", ids=[user_id])
            if not existing:
                logging.info(f"Failed to fetch user with id -> {user_id} not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {user_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"User {user_id} not found"
                )

            status = request.status

            client.set_payload(
                collection_name="users", payload={"status": status}, points=[user_id]
            )

            logging.info(
                f"Updated the status payload for the user vector with id -> {user_id}"
            )
            return emb_pb2.EmbeddingResponse(success=True, msg="Updated successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to update the status payload of a user vector with id -> {user_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def DeleteUserEmbedding(self, request, context):
        """Deletes a user vector"""
        user_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="users", ids=[user_id])

            if not existing:
                logging.info(f"Failed to fetch user with id -> {user_id} not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User {user_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"User {user_id} not found"
                )

            client.delete(collection_name="users", points_selector=[user_id])

            logging.info(f"Deleted the user vector with id -> {user_id}")

            return emb_pb2.EmbeddingResponse(success=True, msg="Deleted successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to delete a user vector with id -> {user_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))
