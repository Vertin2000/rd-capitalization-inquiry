# 数据质量审计报告

生成时间: 2026-06-20T15:28:24.582171
metadata 记录数: 150
PDF 文件数: 150

## 检查项汇总

| 检查项 | 状态 | 说明 |
|--------|------|------|
| metadata_non_empty | ✅ PASS | metadata.csv 共 150 条记录 |
| no_duplicate_doc_id | ✅ PASS | 所有 doc_id 唯一 |
| pdf_exists | ✅ PASS | 所有 150 个 PDF 文件存在 |
| pdf_integrity | ✅ PASS | 所有 PDF 文件完整性校验通过 |
| title_keywords | ✅ PASS | 所有标题包含必要关键词 |
| download_status | ✅ PASS | download_status 覆盖完整: {'success': 150} |
| error_message | ✅ PASS | error_message 与 download_status 一致 |
| pdf_hash_unique | ✅ PASS | 所有 PDF SHA256 唯一（共 150 个） |

## 结论

✅ **全部检查通过**，数据质量合格。
