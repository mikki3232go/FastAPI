# 공공시설 예약 시스템

FastAPI와 MySQL을 사용한 공공시설 예약 시스템입니다. 공공체육시설, 공공도서관, 주민센터 등의 시설을 예약하고 관리할 수 있습니다.

## 기술 스택

- Backend: FastAPI
- Database: MySQL 8.0
- ORM: SQLAlchemy
- Template Engine: Jinja2
- Container: Docker & Docker Compose

## 주요 기능

1. 시설 관리 (CRUD)
   - 시설 등록
   - 시설 목록 조회
   - 시설 상세 정보 조회
   - 시설 정보 수정
   - 시설 삭제

2. 예약 관리 (CRUD)
   - 예약 생성
   - 예약 목록 조회
   - 예약 상세 정보 조회
   - 예약 수정
   - 예약 삭제

## 프로젝트 구조

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── routers/
    │   ├── __init__.py
    │   ├── facilities.py
    │   └── reservations.py
    └── templates/
        ├── index.html
        ├── facilities/
        │   └── list.html
        └── reservations/
            ├── list.html
            └── new.html
```

## 설치 및 실행 방법

1. 프로젝트 클론
```bash
git clone [프로젝트_URL]
cd [프로젝트_디렉토리]
```

2. Docker 컨테이너 실행
```bash
docker-compose up --build
```

3. 웹 브라우저에서 접속
- 메인 페이지: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 데이터베이스 스키마

### facilities 테이블
- id (PK): Integer
- name: String(100)
- type: Enum (sports, library, community_center)
- location: String(200)
- capacity: Integer
- description: String(500)
- created_at: DateTime
- updated_at: DateTime

### reservations 테이블
- id (PK): Integer
- facility_id (FK): Integer
- user_name: String(100)
- user_phone: String(20)
- start_time: DateTime
- end_time: DateTime
- purpose: String(200)
- created_at: DateTime
- updated_at: DateTime

## API 엔드포인트

### 시설 관련
- GET /facilities/ - 시설 목록 조회
- POST /facilities/ - 시설 생성
- GET /facilities/{id} - 시설 상세 정보 조회
- PUT /facilities/{id} - 시설 정보 수정
- DELETE /facilities/{id} - 시설 삭제

### 예약 관련
- GET /reservations/ - 예약 목록 조회
- POST /reservations/ - 예약 생성
- GET /reservations/{id} - 예약 상세 정보 조회
- PUT /reservations/{id} - 예약 수정
- DELETE /reservations/{id} - 예약 삭제
- GET /reservations/new - 예약 생성 폼

## 초기 데이터

시스템 시작 시 자동으로 다음 시설들이 등록됩니다:

1. 종합체육관
   - 위치: 서울시 강남구 테헤란로 123
   - 수용 인원: 100명
   - 설명: 다목적 체육시설로 농구장, 배구장, 배드민턴장이 구비되어 있습니다.

2. 중앙도서관
   - 위치: 서울시 서초구 서초대로 456
   - 수용 인원: 200명
   - 설명: 3층 규모의 종합 도서관으로 열람실, 세미나실이 구비되어 있습니다.

3. 주민센터
   - 위치: 서울시 송파구 올림픽로 789
   - 수용 인원: 50명
   - 설명: 다목적 강당과 회의실이 구비된 주민센터입니다.

## 주의사항

1. MySQL 포트 충돌
   - 기본 MySQL 포트(3306)가 이미 사용 중인 경우, docker-compose.yml 파일에서 포트를 변경할 수 있습니다.
   - 예: "3307:3306"으로 변경

2. 데이터베이스 접속 정보
   - 기본 설정:
     - 데이터베이스: facility_db
     - 사용자: user
     - 비밀번호: password
   - 필요시 docker-compose.yml 파일에서 환경 변수를 수정할 수 있습니다.

## 개발 환경 설정

1. Python 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 