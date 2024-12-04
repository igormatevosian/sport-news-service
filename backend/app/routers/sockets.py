import json

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.db import schemas, services
from app.dependencies import get_db

router = APIRouter(tags=["sockets"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{article_id}")
async def websocket_endpoint(
    article_id: int, websocket: WebSocket, db: Session = Depends(get_db)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                comment_data = json.loads(data)
                user_id = comment_data.get("userId")
                comment_text = comment_data.get("comment")
                if user_id and comment_text:
                    await save_comment(db, article_id, comment_text, user_id)
                    user_service = services.UserService(db)
                    user_name = user_service.get_user(user_id).name
                    message = json.dumps(
                        {"userName": user_name, "comment": comment_text}
                    )
                    await manager.broadcast(message)
            except json.JSONDecodeError:
                print("Invalid JSON format received")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def save_comment(db: Session, article_id: int, comment_text: str, user_id: int):
    try:
        comment = schemas.ArticleCommentCreate(content=comment_text)
        comment_service = services.ArticleCommentService(db)
        comment_service.create_article_comment(
            comment=comment, article_id=article_id, commenter_id=user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving comment: {e}")
