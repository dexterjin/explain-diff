# Explain Diff

코드 변경(diff, branch, commit, PR)을 깊이 이해할 수 있도록 **한국어 설명서**를 만드는 Agent Skill입니다.

기본적으로 인터랙티브 HTML을 생성하고, 사용자가 요청하면 **연결된 Notion에 직접 페이지를 생성하거나 기존 페이지를 갱신**할 수 있습니다. Claude Code, Google Antigravity, ChatGPT 등 `SKILL.md` 기반 Agent Skills 환경에서 최대한 공통으로 사용할 수 있도록 플랫폼 종속 지시를 최소화했습니다.

## 주요 기능

- 변경 배경과 기존 동작 설명
- 핵심 직관을 작은 예제로 설명
- 파일 순서가 아닌 실행 흐름 중심 코드 설명
- 엣지 케이스와 트레이드오프 점검
- 5문항 이해도 퀴즈
- HTML: 오답 선택 시 실제 정답과 정답 해설 공개
- Notion: toggle 안에 정답과 선택지별 해설 제공
- 외부 의존성 없는 단일 HTML 생성
- Notion MCP/쓰기 도구가 연결된 환경에서 페이지 직접 생성/갱신
- diff/PR 내부 prompt injection 방어 원칙

## 설치

### Google Antigravity

#### 프로젝트 설치 — 권장

프로젝트 루트에서:

```bash
npx skills add dexterjin/explain-diff -a antigravity --copy -y
```

설치 후 확인:

```bash
ls .agents/skills/explain-diff/SKILL.md
```

#### 전역 설치 — 모든 프로젝트에서 사용

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

## Notion 연결

Notion 직접 기록 기능은 쓰기 가능한 **Notion MCP 또는 Notion 도구**가 연결된 환경에서 동작합니다.

### Antigravity + Notion MCP

Notion은 Antigravity에서 갤러리의 구형 Notion 커넥터 대신 공식 hosted MCP를 custom server로 연결하는 방식을 권장합니다.

Antigravity의 `mcp_config.json`에 다음 서버를 추가하세요.

```json
{
  "mcpServers": {
    "notion": {
      "serverUrl": "https://mcp.notion.com/mcp"
    }
  }
}
```

Antigravity 전역 설정은 `~/.gemini/config/mcp_config.json`, 프로젝트 설정은 `.agents/mcp_config.json`을 사용할 수 있습니다. 저장 후 OAuth 안내에 따라 Notion workspace를 연결합니다.

### 다른 MCP 클라이언트

공식 Notion MCP endpoint:

```text
https://mcp.notion.com/mcp
```

사용 중인 클라이언트에서 remote MCP server로 연결하고 OAuth를 완료하세요.

## 사용 예

HTML 기본 출력:

- "현재 브랜치 변경사항을 explain-diff로 설명해줘"
- "이 PR을 처음 보는 개발자가 이해할 수 있게 설명해줘"

Notion 직접 기록:

- "현재 변경사항 explain-diff 해서 노션에 기록해줘"
- "이 PR 분석해서 이 Notion 페이지 아래에 정리해줘: <Notion URL>"
- "HTML도 만들고 노션에도 저장해줘"

Notion 쓰기 기능이 연결되지 않은 상태에서 Notion 출력을 요청하면 Skill은 임의로 HTML로 대체하지 않고 연결 또는 권한이 필요하다고 안내합니다.

## HTML 렌더러

`scripts/render.py`는 콘텐츠 JSON을 받아 self-contained HTML을 생성합니다.

```bash
python scripts/render.py content.json --output /tmp/2026-08-13-explanation-example.html
```

입력 JSON에는 정확히 5개의 quiz 항목이 있어야 합니다. 오답을 선택하면 사용자가 선택한 답의 해설과 함께 실제 정답 및 정답 해설이 표시됩니다.

## Notion 출력 형식

Notion 모드는 `references/notion.md`의 규칙을 따릅니다.

- 요약 / 배경 / 핵심 직관 / 변경 전·후 / 코드 흐름 / 엣지 케이스
- 정확히 5개의 퀴즈
- 각 퀴즈의 `정답 및 해설 보기` toggle
- 생성 완료 후 Notion 페이지 URL 반환

## 업데이트

`skills` CLI로 설치했다면:

```bash
npx skills update explain-diff
```

Antigravity 전역 설치 스크립트를 사용했다면:

```bash
git -C ~/.gemini/config/skills/explain-diff pull --ff-only
```

## Credits

이 프로젝트는 Geoffrey Litt가 공개한 `explain-diff` 아이디어와 커뮤니티에서 논의된 개선 아이디어(퀴즈 선택지 편향 방지, 렌더러 분리, prompt-injection 주의)에서 영감을 받았습니다. 이 저장소의 Skill 문구와 구현은 별도로 작성되었습니다.
