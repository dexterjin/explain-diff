#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import html
import json
import random
from pathlib import Path


def esc(value):
    return html.escape(str(value), quote=True)


def safe_section_html(raw):
    # Content is authored by the agent. Keep the useful markup but block active/external HTML.
    text = str(raw)
    lowered = text.lower()
    blocked = ("<script", "<iframe", "<object", "<embed", "javascript:", "http://", "https://")
    if any(token in lowered for token in blocked):
        return f"<pre><code>{esc(text)}</code></pre>"
    return text


def shuffled_options(question, seed):
    options = question["options"]
    explanations = question["explanations"]
    correct = int(question["correct"])
    items = [
        {"text": options[i], "explanation": explanations[i], "correct": i == correct}
        for i in range(len(options))
    ]
    rng = random.Random(seed)
    rng.shuffle(items)
    return items


def render(data):
    title = esc(data.get("title", "코드 변경 설명"))
    summary = esc(data.get("summary", ""))
    assumptions = data.get("assumptions", []) or []
    sections = data.get("sections", []) or []
    quiz = data.get("quiz", []) or []
    if len(quiz) != 5:
        raise ValueError("quiz must contain exactly 5 questions")

    seed_source = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    base_seed = int(hashlib.sha256(seed_source).hexdigest()[:16], 16)

    toc = "".join(f'<li><a href="#{esc(s.get("id", "section"))}">{esc(s.get("title", "섹션"))}</a></li>' for s in sections)
    toc += '<li><a href="#quiz">이해도 퀴즈</a></li>'

    assumptions_html = ""
    if assumptions:
        items = "".join(f"<li>{esc(x)}</li>" for x in assumptions)
        assumptions_html = f'<aside class="callout"><strong>분석 가정</strong><ul>{items}</ul></aside>'

    section_html = "".join(
        f'<section id="{esc(s.get("id", "section"))}"><h2>{esc(s.get("title", "섹션"))}</h2>{safe_section_html(s.get("html", ""))}</section>'
        for s in sections
    )

    quiz_cards = []
    for qi, q in enumerate(quiz):
        items = shuffled_options(q, base_seed + qi * 7919)
        buttons = []
        for idx, item in enumerate(items):
            buttons.append(
                '<button class="option" type="button" '
                f'data-correct="{str(item["correct"]).lower()}" '
                f'data-answer="{esc(item["text"])}" '
                f'data-feedback="{esc(item["explanation"])}">'
                f'<span class="option-label">{chr(65 + idx)}</span>{esc(item["text"])}</button>'
            )
        quiz_cards.append(
            f'<article class="quiz-card"><h3>{qi + 1}. {esc(q.get("question", ""))}</h3>'
            f'<div class="options">{"".join(buttons)}</div>'
            '<div class="feedback" aria-live="polite"></div></article>'
        )

    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root {{ color-scheme: light dark; --bg:#fbfbfd; --fg:#17171a; --muted:#62626a; --card:#ffffff; --line:#d9d9e0; --accent:#315efb; --ok:#166534; --bad:#9f1239; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111216; --fg:#f2f3f5; --muted:#a7aab3; --card:#191b21; --line:#363945; --accent:#8da2ff; --ok:#86efac; --bad:#fda4af; }} }}
* {{ box-sizing:border-box; }} body {{ margin:0; font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:var(--bg); color:var(--fg); line-height:1.7; }}
main {{ width:min(980px, calc(100% - 32px)); margin:0 auto; padding:48px 0 80px; }}
h1 {{ font-size:clamp(2rem,5vw,3.5rem); line-height:1.1; margin:0 0 16px; }} h2 {{ margin-top:56px; border-bottom:1px solid var(--line); padding-bottom:10px; }} h3 {{ margin-top:0; }}
.summary {{ font-size:1.08rem; color:var(--muted); }} nav,.callout,.quiz-card,.panel {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; margin:22px 0; }}
nav ul {{ margin:8px 0 0; padding-left:22px; }} a {{ color:var(--accent); }}
pre {{ white-space:pre-wrap; overflow-wrap:anywhere; overflow-x:auto; padding:16px; border-radius:10px; background:#0b1020; color:#e9eefc; }} code {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }}
.flow {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:18px 0; }} .node {{ border:1px solid var(--line); background:var(--card); border-radius:10px; padding:10px 14px; }} .arrow {{ color:var(--muted); font-weight:700; }}
.compare {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }} @media (max-width:700px) {{ .compare {{ grid-template-columns:1fr; }} main {{ width:min(100% - 22px,980px); padding-top:28px; }} }}
.options {{ display:grid; gap:10px; }} .option {{ width:100%; text-align:left; border:1px solid var(--line); background:var(--card); color:var(--fg); padding:12px 14px; border-radius:10px; cursor:pointer; font:inherit; }}
.option:hover,.option:focus-visible {{ border-color:var(--accent); outline:3px solid color-mix(in srgb,var(--accent) 24%,transparent); }} .option[disabled] {{ cursor:default; opacity:.9; }} .option.selected {{ font-weight:700; }} .option.correct-answer {{ border-color:var(--ok); }} .option.wrong-selected {{ border-color:var(--bad); }} .option-label {{ display:inline-grid; place-items:center; width:1.8em; height:1.8em; margin-right:9px; border:1px solid var(--line); border-radius:999px; }} .result-badge {{ float:right; margin-left:10px; padding:2px 8px; border:1px solid currentColor; border-radius:999px; font-size:.82em; font-weight:700; }} .result-badge.correct {{ color:var(--ok); }} .result-badge.selected-wrong {{ color:var(--bad); }}
.feedback {{ margin-top:12px; min-height:1.5em; }} .feedback.ok {{ color:var(--ok); }} .feedback.bad {{ color:var(--bad); }} .feedback p {{ margin:.45em 0; }} .feedback .correct-detail {{ color:var(--ok); }}
table {{ width:100%; border-collapse:collapse; display:block; overflow-x:auto; }} th,td {{ border:1px solid var(--line); padding:8px 10px; text-align:left; }}
</style>
</head>
<body><main>
<header><h1>{title}</h1><p class="summary">{summary}</p></header>
<nav aria-label="목차"><strong>목차</strong><ul>{toc}</ul></nav>
{assumptions_html}
{section_html}
<section id="quiz"><h2>이해도 퀴즈</h2>{''.join(quiz_cards)}</section>
</main>
<script>
(() => {{
  document.querySelectorAll('.quiz-card').forEach(card => {{
    const feedback = card.querySelector('.feedback');
    const buttons = [...card.querySelectorAll('.option')];
    const optionText = target => `${{target.querySelector('.option-label').textContent}}. ${{target.dataset.answer}}`;
    const addBadge = (target, label, className) => {{
      const badge = document.createElement('span');
      badge.className = `result-badge ${{className}}`;
      badge.textContent = label;
      target.appendChild(badge);
    }};
    buttons.forEach(button => button.addEventListener('click', () => {{
      const correct = button.dataset.correct === 'true';
      const correctButton = buttons.find(b => b.dataset.correct === 'true');
      buttons.forEach(b => {{
        b.disabled = true;
        b.classList.remove('selected', 'correct-answer', 'wrong-selected');
      }});
      button.classList.add('selected');
      correctButton.classList.add('correct-answer');
      addBadge(correctButton, '정답', 'correct');
      if (!correct) {{
        button.classList.add('wrong-selected');
        addBadge(button, '내 선택', 'selected-wrong');
      }}

      feedback.replaceChildren();
      feedback.className = 'feedback ' + (correct ? 'ok' : 'bad');

      const status = document.createElement('p');
      status.textContent = correct ? '정답입니다.' : '오답입니다.';
      feedback.appendChild(status);

      const selectedDetail = document.createElement('p');
      selectedDetail.textContent = `선택한 답: ${{optionText(button)}} — ${{button.dataset.feedback}}`;
      feedback.appendChild(selectedDetail);

      if (!correct) {{
        const correctDetail = document.createElement('p');
        correctDetail.className = 'correct-detail';
        correctDetail.textContent = `정답: ${{optionText(correctButton)}} — ${{correctButton.dataset.feedback}}`;
        feedback.appendChild(correctDetail);
      }}
    }}));
  }}));
}})();
</script>
</body></html>'''


def main():
    parser = argparse.ArgumentParser(description="Render explain-diff JSON into a self-contained HTML file")
    parser.add_argument("input", help="content JSON path")
    parser.add_argument("--output", help="output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else Path("/tmp") / f"{dt.date.today().isoformat()}-explanation.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()
