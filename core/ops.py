from schemas.project import ProjectPayload
from schemas.user import UserPayload


def user_to_point(user_id: str, vector: list[float]):
    payload = UserPayload(id=user_id).model_dump()

    return {"id": f"user:{user_id}", "vector": vector, "payload": payload}


def project_to_point(project_id: str, vector: list[float]):
    payload = ProjectPayload(id=project_id).model_dump()

    return {"id": f"project:{project_id}", "vector": vector, "payload": payload}
