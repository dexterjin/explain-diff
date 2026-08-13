# Explain Diff

코드 변경(diff, branch, commit, PR)을 깊이 이해할 수 있도록 **한국어 인터랙티브 HTML 설명서**를 생성하는 Agent Skill입니다.

Claude Code, Google Antigravity, ChatGPT 등 `SKILL.md` 기반 Agent Skills 환경에서 최대한 공통으로 사용할 수 있도록 플랫폼 종속 지시를 최소화했습니다.

## 주요 기능

- 변경 배경과 기존 동작 설명
- 핵심 직관을 작은 예제로 설명
- 파일 순서가 아닌 실행 흐름 중심 코드 설명
- 엣지 케이스와 트레이드오프 점검
- 5문항 인터랙티브 퀴즈
- 외부 의존성 없는 단일 HTML 생성
- 선택지 순서 결정적 셔플
- diff/PR 내부 prompt injection 방어 원칙

## 설치

### Google Antigravity

#### 프로젝트 설치 — 권장

Antigravity 공식 workspace Skill 경로는 `.agents/skills/`입니다. 프로젝트 루트에서 다음을 실행하세요.

```bash
npx skills add dexterjin/explain-diff -a antigravity --copy -y
```

`--copy`는 Antigravity가 symlink된 Skill을 인식하지 못하는 환경을 피하기 위해 사용합니다.

설치 후 확인:

```bash
ls .agents/skills/explain-diff/SKILL.md
```

#### 전역 설치 — 모든 프로젝트에서 사용

Antigravity 공식 global Skill 경로는 `~/.gemini/config/skills/`입니다. 현재 `skills` CLI의 Antigravity 전역 경로와 공식 경로가 어긋나는 사례가 있어, 전역 설치는 아래 스크립트를 권장합니다.

```bash
curl -fsSL https://raw.githubusercontent.com/dexterjin/explain-diff/main/install-antigravity.sh | bash
```

설치 후 확인:

```bash
ls ~/.gemini/config/skills/explain-diff/SKILL.md
```

업데이트:

```bash
git -C ~/.gemini/config/skills/explain-diff pull --ff-only
```

### Agent Skills CLI 자동 감지

```bash
npx skills add dexterjin/explain-diff
```

### Claude Code

프로젝트 설치:

```bash
npx skills add dexterjin/explain-diff -a claude-code -y
```

전역 설치:

```bash
npx skills add dexterjin/explain-diff -a claude-code -g -y
```

### ChatGPT

ChatGPT용 UI 메타데이터는 `agents/openai.yaml`에 포함되어 있습니다. ChatGPT의 Skill 업로드 기능을 사용하는 경우 저장소 내용을 Skill ZIP으로 패키징해 업로드하세요.

## 사용 예

- "현재 브랜치 변경사항을 explain-diff로 설명해줘"
- "이 PR을 처음 보는 개발자가 이해할 수 있게 설명해줘"
- "이 리팩터링이 왜 필요한지 기존/신규 흐름을 비교해서 보여줘"

Skill은 주변 코드와 테스트까지 살펴본 뒤 한국어 설명 HTML을 생성합니다.

## 렌더러

`scripts/render.py`는 콘텐츠 JSON을 받아 self-contained HTML을 생성합니다.

```bash
python scripts/render.py content.json --output /tmp/2026-08-13-explanation-example.html
```

입력 JSON에는 정확히 5개의 quiz 항목이 있어야 합니다.

## 업데이트

`skills` CLI로 설치했다면 다음 명령을 사용할 수 있습니다.

```bash
npx skills update explain-diff
```

Antigravity 전역 설치 스크립트를 사용했다면 저장소 자체가 설치되므로 `git pull`로 갱신할 수 있습니다.

## Credits

이 프로젝트는 Geoffrey Litt가 공개한 `explain-diff` 아이디어와 커뮤니티에서 논의된 개선 아이디어(퀴즈 선택지 편향 방지, 렌더러 분리, prompt-injection 주의)에서 영감을 받았습니다. 이 저장소의 Skill 문구와 구현은 별도로 작성되었습니다.
