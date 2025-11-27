# 🎮 Flask 테트리스 게임

Flask를 사용하여 만든 브라우저 기반 테트리스 게임입니다.

## 🎯 기능

- ✨ 7가지 테트리스 블록 (I, O, T, S, Z, J, L)
- 🎨 모던한 UI 디자인 (그라디언트, 글래스모피즘)
- 🎮 완전한 게임 컨트롤
- 📦 블럭 보관함 (Hold) 기능
- 📊 점수, 레벨, 라인 수 추적
- 👀 다음 블록 미리보기
- ⏸️ 일시정지 기능
- 🎨 3단 레이아웃 (보관함 | 게임 | 정보)

## 🕹️ 조작법

- `←` `→` : 블록 좌우 이동
- `↑` : 블록 회전
- `↓` : 빠른 낙하
- `Space` : 즉시 낙하
- `C` : 블럭 보관/교체
- `P` : 일시정지/재개

## 🚀 실행 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
python app.py
```

### 4. 브라우저에서 접속

```
http://localhost:5000
```

## 📁 프로젝트 구조

```
테트리스/
├── venv/                 # 가상환경 (git에서 제외)
├── templates/
│   └── index.html       # 게임 UI 및 로직
├── app.py               # Flask 서버
├── requirements.txt     # 의존성
├── .gitignore          # Git 제외 파일
└── README.md           # 프로젝트 설명
```

## 🛠️ 기술 스택

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Graphics**: HTML5 Canvas API

## 📝 라이센스

MIT License

## 👨‍💻 개발자

명학
