import grpc
from qdrant_client.models import PointStruct
from db.db import get_qdrant_client
from generated import findme_pb2, findme_pb2_grpc
from model.embedding import generate_project_embedding


class ProjectEmbeddingService(findme_pb2_grpc.ProjectEmbeddingServiceServicer):
    def CreateProjectEmbedding(self, request, context):
        try:
            project_id = request.project_id
            title = request.title
            description = request.description
            skills = list(request.skills)

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
                        },
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

    def UpdateProjectEmbedding(self, request, context):
        project_id = request.project_id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="projects", ids=[project_id])
            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {project_id} not found")
                return findme_pb2.EmbeddingResponse(
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

            return findme_pb2.EmbeddingResponse(
                success=True, msg="Updated successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return findme_pb2.EmbeddingResponse(success=False, msg=str(e))

    def DeleteProjectEmbedding(self, request, context):
        project_id = request.id
        client = get_qdrant_client()

        try:
            existing = client.retrieve(collection_name="projects", ids=[project_id])

            if not existing:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Project {project_id} not found")
                return findme_pb2.EmbeddingResponse(
                    success=False, msg=f"Project {project_id} not found"
                )

            client.delete(collection_name="projects", points_selector=[project_id])

            return findme_pb2.EmbeddingResponse(
                success=True, msg="Deleted successfully"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occured -> {str(e)}")
            return findme_pb2.EmbeddingResponse(success=False, msg=str(e))
