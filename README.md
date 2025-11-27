# 🎮 Pygame 테트리스 게임

Python의 Pygame 라이브러리를 사용하여 만든 데스크톱 테트리스 게임입니다.

## 🎯 기능

- ✨ 7가지 테트리스 블록 (I, O, T, S, Z, J, L)
- 🎨 **네온 스타일 UI 디자인** (발광 효과, 다크 테마)
- 🎮 완전한 게임 컨트롤 (연속 이동 지원)
- 📦 블럭 보관함 (Hold) 기능
- 👻 **고스트 블럭** (낙하 위치 미리보기)
- 📊 점수, 레벨, 라인 수 추적
- 👀 다음 블록 5개 미리보기
- ⏸️ 일시정지 기능
- 🎨 3단 레이아웃 (보관함 | 게임 | 정보)

## 🕹️ 조작법

- `←` `→` : 블록 좌우 이동
- `↑` : 블록 회전
- `↓` : 빠른 낙하
- `Space` : 즉시 낙하
- `C` : 블럭 보관/교체
- `P` : 일시정지/재개
- `R` : 게임 오버 시 재시작

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

### 3. 게임 실행

```bash
python app.py
```

## 📁 프로젝트 구조

```
테트리스/
├── venv/                 # 가상환경 (git에서 제외)
├── app.py               # Pygame 게임 로직 및 실행
├── requirements.txt     # 의존성 (pygame)
├── .gitignore          # Git 제외 파일
└── README.md           # 프로젝트 설명
```

## 🛠️ 기술 스택

- **Language**: Python 3
- **Library**: Pygame

## 📝 라이센스

MIT License

## 👨‍💻 개발자

명학
