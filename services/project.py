import logging
import grpc
from qdrant_client.models import PointStruct
from db.db import get_qdrant_client
from generated import emb_pb2, emb_pb2_grpc
from model.embedding import generate_project_embedding


class ProjectEmbeddingService(emb_pb2_grpc.ProjectEmbeddingServiceServicer):
    def CreateProjectEmbedding(self, request, context):
        """Creates and stores a vector embedding for a project"""
        try:
            project_id = request.project_id
            user_id = request.user_id
            title = request.title
            description = request.description
            skills = list(request.skills)
            status = True

            client = get_qdrant_client()
            vector = generate_project_embedding(title, description, skills)

            client.upsert(
                collection_name="projects",
                points=[
                    PointStruct(
                        id=project_id,
                        vector=vector,
                        payload={
                            "title": title,
                            "description": description,
                            "skills": skills,
                            "status": status,
                            "user_id": user_id,
                        },
                    )
                ],
            )

            logging.info(
                f"Added a vector embedding for project with id -> {project_id}"
            )

            return emb_pb2.EmbeddingResponse(success=True, msg="Created successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to create a project vector -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def UpdateProjectEmbedding(self, request, context):
        """Updates the vector embedding of a project"""
        project_id = request.project_id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="projects", ids=[project_id])
            if not existing:
                logging.info(
                    f"Failed to retrieve project with id -> {project_id} not found"
                )
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {project_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"Project {project_id} not found"
                )

            title = request.title
            description = request.description
            skills = list(request.skills)

            vector = generate_project_embedding(title, description, skills)

            client.upsert(
                collection_name="projects",
                points=[
                    PointStruct(
                        id=project_id,
                        vector=vector,
                        payload={
                            "title": title,
                            "description": description,
                            "skills": skills,
                        },
                    )
                ],
            )

            logging.info(
                f"Updated the vector embedding for project with id -> {project_id}"
            )

            return emb_pb2.EmbeddingResponse(success=True, msg="Updated successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to update a project vector  id -> {project_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def UpdateProjectStatus(self, request, context):
        """Updates the status payload of a project vector"""
        project_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve("projects", ids=[project_id])
            if not existing:
                logging.info(
                    f"Failed to retrieve project with id -> {project_id} not found"
                )
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {project_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"Project {project_id} not found"
                )

            status = request.status

            client.set_payload(
                collection_name="projects",
                payload={"status": status},
                points=[project_id],
            )

            logging.info(
                f"Updated the status payload for the project vector with id -> {project_id}"
            )

            return emb_pb2.EmbeddingResponse(success=True, msg="Updated successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to update a project status id -> {project_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))

    def DeleteProjectEmbedding(self, request, context):
        """Deletes a project vector"""
        project_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="projects", ids=[project_id])

            if not existing:
                logging.info(
                    f"Failed to retrieve project with id -> {project_id} not found"
                )
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {project_id} not found")
                return emb_pb2.EmbeddingResponse(
                    success=False, msg=f"Project {project_id} not found"
                )

            client.delete(collection_name="projects", points_selector=[project_id])

            logging.info(f"Deleted the vector for project with id -> {project_id}")

            return emb_pb2.EmbeddingResponse(success=True, msg="Deleted successfully")

        except Exception as e:
            logging.error(
                f"An error occured while trying to delete a project vector with id -> {project_id}, err -> {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return emb_pb2.EmbeddingResponse(success=False, msg=str(e))
