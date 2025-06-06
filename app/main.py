from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import engine, SessionLocal, get_db
from app import models
from app.routers import facilities, reservations
from sqlalchemy.orm import Session

app = FastAPI(title="공공시설 예약 시스템")

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 템플릿 설정
templates = Jinja2Templates(directory="app/templates")

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 라우터 등록
app.include_router(facilities.router)
app.include_router(reservations.router)

def init_db(db: Session):
    # 시설 데이터가 있는지 확인
    facilities = db.query(models.Facility).first()
    if not facilities:
        # 기본 시설 데이터 추가
        default_facilities = [
            models.Facility(
                name="종합체육관",
                type=models.FacilityType.SPORTS,
                location="서울시 강남구 테헤란로 123",
                capacity=100,
                description="다목적 체육시설로 농구장, 배구장, 배드민턴장이 구비되어 있습니다."
            ),
            models.Facility(
                name="중앙도서관",
                type=models.FacilityType.LIBRARY,
                location="서울시 서초구 서초대로 456",
                capacity=200,
                description="3층 규모의 종합 도서관으로 열람실, 세미나실이 구비되어 있습니다."
            ),
            models.Facility(
                name="주민센터",
                type=models.FacilityType.COMMUNITY_CENTER,
                location="서울시 송파구 올림픽로 789",
                capacity=50,
                description="다목적 강당과 회의실이 구비된 주민센터입니다."
            )
        ]
        db.add_all(default_facilities)
        db.commit()
        print("기본 시설 데이터가 추가되었습니다.")

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    facilities = db.query(models.Facility).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "facilities": facilities
    }) 