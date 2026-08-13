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

### 자동 감지

프로젝트 디렉터리에서 실행하면 설치 가능한 에이전트를 감지해 선택할 수 있습니다.

```bash
npx skills add dexterjin/explain-diff
```

전역 설치가 필요하면 `-g`를 추가합니다.

```bash
npx skills add dexterjin/explain-diff -g
```

### Google Antigravity

프로젝트에 설치:

```bash
npx skills add dexterjin/explain-diff -a antigravity -y
```

전역 설치:

```bash
npx skills add dexterjin/explain-diff -a antigravity -g -y
```

### Claude Code

프로젝트에 설치:

```bash
npx skills add dexterjin/explain-diff -a claude-code -y
```

전역 설치:

```bash
npx skills add dexterjin/explain-diff -a claude-code -g -y
```

### Antigravity + Claude Code 동시에

```bash
npx skills add dexterjin/explain-diff -a antigravity -a claude-code -g -y
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

`skills` CLI로 설치했다면 이후에는 다음 명령으로 최신 버전을 확인/업데이트할 수 있습니다.

```bash
npx skills update explain-diff
```

## Credits

이 프로젝트는 Geoffrey Litt가 공개한 `explain-diff` 아이디어와 커뮤니티에서 논의된 개선 아이디어(퀴즈 선택지 편향 방지, 렌더러 분리, prompt-injection 주의)에서 영감을 받았습니다. 이 저장소의 Skill 문구와 구현은 별도로 작성되었습니다.
