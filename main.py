from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(app):
    
    # 애플리케이션 시작 시 수행할 작업
    print("Initialize...")
    #load_dotenv()  # 환경 변수를 로드합니다.
    #init_filesystem()
    #init_db()
    print("Done. Application has started.")
    
    yield
    
    print("Close...")
    # 애플리케이션 종료 시 수행할 작업
    #connection_pool.closeall()
    print("Done. Application has shut down.")
    
app = FastAPI(lifespan = app_lifespan)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (개발 목적용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


# Serve the contents of the 'public' directory as static files
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/{layout_name}/")
async def get_layout(layout_name: str):
    '''
    valid_layouts = [
        "App_Layout", "App_Layout_dark", "Boxed_App_Layout", 
        # ... add all valid layout names here
    ]
    if layout_name not in valid_layouts:
        raise HTTPException(status_code=404, detail="Layout not found")
    '''
    
    return FileResponse(f"./Demos/{layout_name}/index.html")

@app.get("/")
async def get_root():
    # Serve 'index.html' from 'Application_Shells/app_layout'
    return FileResponse("./Demos/App_Layout/index.html")

@app.get("/{page_name}")
async def get_page_name(page_name: str):
    # Serve 'index.html' from 'Application_Shells/app_layout'
    return FileResponse(f"./Demos/App_Layout/{page_name}")

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000)