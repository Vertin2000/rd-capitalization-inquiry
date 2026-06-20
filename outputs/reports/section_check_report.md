# Section Check Report

route 阶段章节定位质量检查（Week 13 讲义要求：定位后要检查是否找对）。

- 检查行数: 750
- 定位成功行: 750
- 未定位行: 0

## 质量问题分布

| 问题标记 | 出现次数 |
| -------- | --------: |
| page_unavailable | 750 |
| no_positive_keyword | 209 |
| negative_keyword_hit | 67 |
| low_score(16) | 10 |
| low_score(26) | 7 |
| low_score(22) | 7 |
| low_score(-6) | 7 |
| low_score(29) | 4 |
| low_score(8) | 3 |
| low_score(19) | 2 |
| low_score(10) | 2 |
| low_score(18) | 1 |
| low_score(-9) | 1 |
| low_score(-2) | 1 |
| low_score(14) | 1 |
| low_score(28) | 1 |

## 字段说明

- `found`: 该 doc 是否定位到任一目标章节
- `section_title`: 切片文本首个 Markdown 标题（规则名见 `target_section`）
- `page_start/page_end`: parsed Markdown 无页码来源，留空，`quality_issue` 标 `page_unavailable`
- `quality_issue`: 由 match_score / match_reason / 文本长度推导

