from app.model.base_model import BaseModel
from app.schema.user import UserInfo


class Token(BaseModel):
    code: int = 200
    msg: str = 'Success'
    access_token: str
    token_type: str = 'Bearer'
    user: UserInfo