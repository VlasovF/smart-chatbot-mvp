import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.api.schemas import ChatRequest
from src.core.logger import logger
from src.db.database import get_db
from src.db.models import User
from src.llm.factory import get_llm_client

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Эндпоинт для стриминга ответов от LLM

    Возвращает Server-Sent Events (SSE) поток с токенами
    """
    try:
        # Получаем LLM клиент
        llm_client = get_llm_client()

        # Если указана модель, пересоздаём клиент с ней
        if request.model:
            from src.llm.ollama import OllamaLLMClient

            llm_client = OllamaLLMClient(model=request.model)

        logger.info(
            f"User {current_user.username} sent message. "
            f"Temperature: {request.temperature}, "
            f"Max tokens: {request.max_tokens}"
        )

        # Создаём генератор для SSE
        async def generate():
            try:
                async for token in llm_client.stream_generate(
                    messages=request.messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    system_prompt=request.system_prompt,
                ):
                    # Отправляем токен в формате SSE
                    yield f"data: {json.dumps({'token': token})}\n\n"

                # Отправляем сигнал окончания
                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                logger.error(f"Error during generation: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Отключаем буферизацию nginx
            },
        )

    except Exception as e:
        logger.error(f"Error in /chat/stream: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
