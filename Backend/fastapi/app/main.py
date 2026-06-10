from app.crud.database import init_db, engine
from app.crud.db_manager import init_admin, init_rag_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.web_chatbot import router as chatbot_router
from app.api.web_dashboard import router as dashboard_router
from app.api.web_conversation import router as conversation_router
from app.api.insert_and_delete_docs import router as file_router
from app.api.auth import router as auth_router
from app.api.line_webhook import router as line_router
from app.api.edit_prompt import router as prompt_router
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import time


def wait_for_mysql(max_retries=30, delay=2):
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print("[Database] MySQL connected")
            return

        except OperationalError:
            print(
                f"[Database] Waiting for MySQL "
                f"({i + 1}/{max_retries})"
            )
            time.sleep(delay)

    raise Exception("MySQL is not available")

@asynccontextmanager
async def lifespan(app: FastAPI):

    wait_for_mysql()

    init_db()
    init_admin()
    init_rag_db()
    
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)
app.include_router(dashboard_router)
app.include_router(conversation_router)
app.include_router(file_router)
app.include_router(auth_router)
app.include_router(line_router)
app.include_router(prompt_router)