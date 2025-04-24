from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import requests
import os
import logging
from dotenv import load_dotenv
import json
from typing import Optional
import urllib3

# SSL 경고 무시 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 Obsidian API 정보 가져오기
OBSIDIAN_API_URL = os.getenv("OBSIDIAN_API_URL", "http://127.0.0.1:27123")
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY", "your_api_key_here")
VAULT_PATH = os.getenv("VAULT_PATH", "./vault")

# FastAPI 앱 생성
app = FastAPI(title="Obsidian Bridge API")


# ✅ 외부에서 접근 가능한 OpenAPI 서버 주소 명시
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Obsidian Bridge API",
        version="1.0.0",
        description="GPT용 FastAPI Actions 서버",
        routes=app.routes,
    )

    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000"  # Default local development server
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# ✅ FastAPI에 커스텀 OpenAPI 설정 적용
app.openapi = custom_openapi

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Obsidian API 요청 헤더
def get_obsidian_headers():
    return {
        "Authorization": f"Bearer {OBSIDIAN_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to Obsidian Bridge API", "status": "running"}

# 서버 상태 확인
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Bridge server is running"}

# API 연결 테스트 (다양한 경로 시도)
@app.get("/test-api")
def test_api():
    endpoints = ["/", "/vault/", "/notes/", "/api/vault/"]
    results = {}
    
    for endpoint in endpoints:
        try:
            url = f"{OBSIDIAN_API_URL}{endpoint}"
            logger.debug(f"Testing endpoint: {url}")
            
            try:
                response = requests.get(
                    url,
                    headers=get_obsidian_headers(),
                    verify=False,
                    timeout=10
                )
                results[endpoint] = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.text[:200] if response.text else "Empty response"
                }
                logger.debug(f"Response from {endpoint}: {response.status_code}")
            except requests.exceptions.Timeout:
                results[endpoint] = {"error": "Request timed out"}
            except requests.exceptions.ConnectionError as e:
                results[endpoint] = {"error": f"Connection error: {str(e)}"}
            except Exception as e:
                results[endpoint] = {"error": f"Request error: {str(e)}"}
                
        except Exception as e:
            results[endpoint] = {"error": f"Unexpected error: {str(e)}"}
    
    return results

# 보관함 정보 가져오기 (API 사용)
@app.get("/vault")
def get_vault():
    try:
        logger.debug("Attempting to get vault info via API")
        url = f"{OBSIDIAN_API_URL}/vault/"
        
        try:
            response = requests.get(
                url,
                headers=get_obsidian_headers(),
                verify=False,
                timeout=30
            )
            logger.debug(f"Vault API response status: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get vault via API: {str(e)}")
            # API가 실패하면 파일 시스템으로 폴백
            return get_vault_files()
            
    except Exception as e:
        logger.error(f"Error in get_vault: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 보관함 경로 파라미터를 포함한 요청 시도
@app.get("/vault-path")
def get_vault_with_path():
    try:
        # 보관함 경로를 포함한 요청
        url = f"{OBSIDIAN_API_URL}/vault/?path={VAULT_PATH}"
        logger.debug(f"Requesting vault with path: {url}")
        
        response = requests.get(
            url,
            headers=get_obsidian_headers(),
            verify=False,
            timeout=30
        )
        logger.debug(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": response.status_code, "content": response.text}
    except Exception as e:
        logger.error(f"Error in get_vault_with_path: {str(e)}")
        return {"error": str(e)}

# 파일 시스템을 통해 직접 보관함 파일 목록 가져오기
@app.get("/files")
def get_vault_files():
    try:
        logger.debug(f"Reading files from: {VAULT_PATH}")
        files = []
        
        if not os.path.exists(VAULT_PATH):
            return {"error": f"Path not found: {VAULT_PATH}"}
        
        for root, dirs, filenames in os.walk(VAULT_PATH):
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, VAULT_PATH)
                    files.append(rel_path)
        
        return {"files": files, "count": len(files), "vault_path": VAULT_PATH}
    except Exception as e:
        logger.error(f"Error reading files: {str(e)}")
        return {"error": str(e)}

# 파일 내용 읽기
@app.get("/read-file")
def read_file(path: str):
    try:
        full_path = os.path.join(VAULT_PATH, path)
        logger.debug(f"Reading file: {full_path}")
        
        if not os.path.exists(full_path):
            return {"error": f"File not found: {full_path}"}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {"content": content, "path": path}
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        return {"error": str(e)}

# 노트 목록 가져오기 (API 사용 시도 후 파일 시스템으로 폴백)
@app.get("/notes")
def get_notes():
    try:
        logger.debug("Attempting to get notes via API")
        url = f"{OBSIDIAN_API_URL}/notes/"
        
        try:
            response = requests.get(
                url,
                headers=get_obsidian_headers(),
                verify=False,
                timeout=10
            )
            logger.debug(f"Notes API response status: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get notes via API: {str(e)}")
            # API가 실패하면 파일 시스템으로 폴백
            return get_vault_files()
            
    except Exception as e:
        logger.error(f"Error in get_notes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 특정 노트 가져오기 (API 시도 후 파일 시스템으로 폴백)
@app.get("/notes/{note_id}")
def get_note(note_id: str):
    try:
        logger.debug(f"Attempting to get note {note_id} via API")
        url = f"{OBSIDIAN_API_URL}/notes/{note_id}"
        
        try:
            response = requests.get(
                url,
                headers=get_obsidian_headers(),
                verify=False,
                timeout=10
            )
            logger.debug(f"Note API response status: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get note via API: {str(e)}")
            # API가 실패하면 파일 시스템으로 폴백
            return read_file(note_id)
            
    except Exception as e:
        logger.error(f"Error in get_note: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 노트 검색
@app.get("/search")
def search_notes(query: str):
    try:
        logger.debug(f"Searching notes for: {query}")
        files = []
        
        if not os.path.exists(VAULT_PATH):
            return {"error": f"Path not found: {VAULT_PATH}"}
        
        for root, dirs, filenames in os.walk(VAULT_PATH):
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            if query.lower() in content:
                                rel_path = os.path.relpath(file_path, VAULT_PATH)
                                files.append(rel_path)
                    except Exception as e:
                        logger.error(f"Error reading file {file_path}: {str(e)}")
        
        return {"files": files, "count": len(files), "query": query}
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return {"error": str(e)}

# 프록시 엔드포인트 - 모든 다른 요청을 Obsidian API로 전달
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_endpoint(path: str, request: Request):
    try:
        # 요청 바디 읽기
        body = b""
        if request.method in ["POST", "PUT"]:
            body = await request.body()
        
        # 쿼리 파라미터 가져오기
        params = dict(request.query_params)
        
        # Obsidian API로 요청 전달
        url = f"{OBSIDIAN_API_URL}/{path}"
        logger.debug(f"Proxying {request.method} request to: {url}")
        
        response = requests.request(
            method=request.method,
            url=url,
            headers=get_obsidian_headers(),
            params=params,
            data=body,
            verify=False,
            timeout=30
        )
        
        # 응답 반환
        return response.json() if response.text else {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error in proxy endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")