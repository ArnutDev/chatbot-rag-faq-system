from http.client import HTTPException

from langchain_chroma import Chroma
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
from langchain_core.documents import Document
import json
from datetime import datetime
import os
from pathlib import Path
from app.crud.database import SessionLocal
import bcrypt
from app.models.mysql_models import User, PlatformType, UserRole

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "services", "llm", "chroma_db")
#print(f"กำลังจะเก็บข้อมูลไว้ที่: {os.path.abspath(db_path)}")

#client = chromadb.PersistentClient(path=db_path)  #ดู path folderให้ถูกต้อง
#client = chromadb.HttpClient(host="chromadb", port=4000)
client = chromadb.HttpClient(host="chromadb", port=8000)
# collection = client.get_or_create_collection("chatbot_rag_documents") #อันเก่า L2
collection = client.get_or_create_collection(
    name="rag_documents",
    metadata={"hnsw:space": "cosine"} 
)#อันใหม่ ใช้cosine
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="rag_documents",
    embedding_function=embedding_model,
)

def watch_collect():
    all_collections = client.list_collections()

    print("รายการ Collection ทั้งหมดในฐานข้อมูล:")
    for col in all_collections:
        print(f"- ชื่อ: {col.name}")

# def add_docs(path,vector_store_from_client):
#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     documents = []

#     for i,item in enumerate(data, start=1):
#         # now = datetime.now()
#         # formatted = now.strftime("%d/%m/%Y %H:%M")
#         doc = Document(
#             page_content=item["content"],
#             metadata=item["metadata"]
#         )
#         documents.append(doc)

#     for doc in documents:
#         print(doc.page_content)
#         print(doc.metadata)
#         print("-"*30)

#     uuids = [str(uuid4()) for _ in range(len(documents))]
#     vector_store_from_client.add_documents(documents=documents, ids=uuids)
#     print("add completed")

def add_docs(data):
    # print("test test")
    documents = []

    for i,item in enumerate(data, start=1):
        # now = datetime.now()
        # formatted = now.strftime("%d/%m/%Y %H:%M")
        doc = Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        documents.append(doc)

    for doc in documents:
        print(doc.page_content)
        print(doc.metadata)
        print("-"*30)
    
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store_from_client.add_documents(documents=documents, ids=uuids)
    print("add completed")
    #show_all_docs()

def show_all_docs():
     
    documents = collection.get()
    for doc_id, content, metadata in zip(documents["ids"], documents["documents"], documents["metadatas"]):
        print(f"ID: {doc_id}")
        print(f"Content: {content}")
        print(f"Metadata: {metadata}")
        print("-" * 30)
    
    print("Collection name:", collection.name)
    print("Number of documents:", collection.count())
    # print("Metadata fields:", collection.get()["metadatas"])
    
def get_all_docs():
    results = collection.get()
    formatted_docs = []

    if results["ids"]:
        # ใช้ zip เพื่อจับคู่ id, content, metadata ของแต่ละรายการเข้าด้วยกัน
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def delete_docs(uuid):
    # uuids_to_delete = [
    #     "1fd8ecfe-3b21-4899-a775-27e71f865e75"
    # ]
    # vector_store_from_client.delete(ids=uuids_to_delete)

    collection.delete(ids=[uuid])

def query_by_agency(agency_name):
    #กองบริหารวิชาการ, สำนักดิจิทัลเทคโนโลยี, กองกิจการนักศึกษา
    results = collection.get(
        where={"agency": agency_name}
    )
    formatted_docs = []
    if results["ids"]:
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def query_by_category(category_name):
    #Reg, บริการคอมพิวเตอร์, กองทุนเงินให้กู้ยืมเพื่อการศึกษา, หอพัก
    results = collection.get(
        where={"category": category_name}
    )
    formatted_docs = []
    if results["ids"]:
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def query_by_text(text):
    query_vector = embedding_model.embed_query(text)
    #.query กับ .get ให้ return มา format ไม่เหมือนกันเลยต้องเปลี่ยนวิธีการ mapping ก่อนจะส่งออกให้ api
    results = collection.query(
        n_results= 10,
        query_embeddings= [query_vector]
    )
    formatted_docs = []
    if results["ids"] and results["ids"][0]: 
        
        for doc_id, content, metadata in zip(results["ids"][0], results["documents"][0], results["metadatas"][0]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

# add_docs("Backend/fastapi/app/services/llm/docs-FAQ/รวมไฟล์ json.json",vector_store_from_client)
# delete_docs(vector_store_from_client)
# show_all_docs()



def init_rag_db():

    doc_count = collection.count()
    print(f"ตรวจสอบฐานข้อมูล RAG: ปัจจุบันมีข้อมูลอยู่ {doc_count} รายการ")

    if doc_count == 0:
        print("ไม่พบข้อมูลใน ChromaDB! กำลังเปิดระบบโหลดข้อมูลเริ่มต้นจากไฟล์ JSON...")
        
        current_file = Path(__file__).resolve()
        
        
        fastapi_root = current_file.parent.parent.parent  # ถอยจาก crud -> app -> fastapi
        
        # ต่อพิกัดวิ่งเข้าหาไฟล์ json จากหน้าโฟลเดอร์ fastapi
        json_path = fastapi_root / "app" / "services" / "llm" / "docs-FAQ" / "รวมไฟล์ json.json"
        
        # ดักทางเลือกสำรอง: เผื่อกรณีโครงสร้างไม่มีโฟลเดอร์ fastapi ซ้อน (รันสคริปต์บางประเภท)
        if not json_path.exists():
            # ถอยแค่ 2 ชั้น จาก crud -> app แล้วเข้า services เลย
            json_path = current_file.parent.parent / "services" / "llm" / "docs-FAQ" / "รวมไฟล์ json.json"

        print(f"[DEBUG] พิกัดไฟล์ที่ระบบกำลังจะวิ่งไปเปิด: {json_path}")

        try:
            # ตรวจสอบให้มั่นใจก่อนสั่งเปิดไฟล์
            if not json_path.exists():
                raise FileNotFoundError(f"หาไฟล์ไม่เจอในระบบ พิกัดที่เช็กคือ: {json_path}")
                
            # แปลง Path เป็น string ก่อนส่งให้ฟังก์ชันเดิมของคุณ
            add_docs_from_file(str(json_path), vector_store_from_client)
            print("โหลดข้อมูลเริ่มต้นเข้าสู่ ChromaDB สำเร็จเรียบร้อยแล้ว!")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลดไฟล์เริ่มต้น: {e}")
    else:
        print(" ฐานข้อมูลมีข้อมูลอยู่แล้ว พร้อมใช้งานระบบ RAG ได้ทันที")

def add_docs_from_file(path, vector_store_from_client):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        doc = Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        documents.append(doc)

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store_from_client.add_documents(documents=documents, ids=uuids)
    print(f"ลงข้อมูลเพิ่มสำเร็จจำนวน {len(documents)} รายการ")

def init_admin():
    db = SessionLocal()

    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if not all([admin_email, admin_username, admin_password]):
            print("[Database] Admin env variables are missing.")
            return

        admin_exists = (
            db.query(User)
            .filter(User.email == admin_email)
            .first()
        )

        if admin_exists:
            print(
                f"[Database] Admin account already exists. "
                f"Skipping injection."
            )
            return

        # hash password
        bytes_password = admin_password.encode("utf-8")
        hashed_password = bcrypt.hashpw(
            bytes_password,
            bcrypt.gensalt()
        ).decode("utf-8")

        new_admin = User(
            username=admin_username,
            email=admin_email,
            password=hashed_password,
            line_user_id=None,
            platform=PlatformType.web,
            role=UserRole.admin,
        )

        db.add(new_admin)
        db.commit()

        print(
            f"[Database] Admin account successfully "
            f"injected: {admin_email}"
        )

    except Exception as e:
        db.rollback()
        print(f"[Database] Failed to inject admin: {e}")

    finally:
        db.close()