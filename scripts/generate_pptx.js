/**
 * Generate final_slides.pptx from ppt_outline.md
 *
 * Uses PptxGenJS per C:\Users\Vertin2000\.claude\skills\pptx\ guidelines.
 * Color palette: Teal Trust (finance/academic).
 *
 * Usage: node scripts/generate_pptx.js
 * Output: outputs/final_slides.pptx
 */

const pptxgen = require("pptxgenjs");

// ── Palette ──────────────────────────────────────────────────────────
const C = {
  teal:        "028090",
  seafoam:     "00A896",
  mint:        "02C39A",
  dark:        "1A2F3B",
  white:       "FFFFFF",
  offWhite:    "F5F7F8",
  body:        "2D3A3A",
  muted:       "64748B",
  accent:      "F59E0B",   // warm accent for callouts
  red:         "DC2626",
  tableBorder: "D1D5DB",
  tableHeader: "028090",
  tableStripe: "F0FDFA",
};

// ── Helpers ───────────────────────────────────────────────────────────
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.10,
});

const FONT = { header: "Georgia", body: "Arial" };

function addSlideNumber(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 8.8, y: 5.15, w: 1, h: 0.35,
    fontSize: 8, color: C.muted, fontFace: FONT.body, align: "right",
  });
}

function addBottomLine(slide) {
  slide.addShape("rect", {
    x: 0.6, y: 5.15, w: 8.2, h: 0.008,
    fill: { color: C.seafoam }, line: { color: C.seafoam, width: 0 },
  });
}

function addSectionHeader(slide, title, fontSize = 28) {
  slide.addText(title, {
    x: 0.6, y: 0.25, w: 8.8, h: 0.55,
    fontSize, fontFace: FONT.header, color: C.teal, bold: true,
    margin: 0,
  });
}

function bulletSlide(pres, slide, title, bullets, notes, pageNum) {
  slide.background = { color: C.white };
  addSectionHeader(slide, title);
  addBottomLine(slide);

  const textItems = bullets.map((b, i) => ({
    text: b,
    options: {
      bullet: true,
      breakLine: true,
      fontSize: 15,
      fontFace: FONT.body,
      color: C.body,
      paraSpaceAfter: 8,
    },
  }));

  slide.addText(textItems, {
    x: 0.8, y: 1.05, w: 8.4, h: 3.8,
    valign: "top",
    margin: 0,
  });

  if (notes) slide.addNotes(notes);
  addSlideNumber(slide, pageNum, 14);
  return slide;
}

// ── Main ─────────────────────────────────────────────────────────────
function buildPresentation() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "R&D Capitalization Risk Screening Team";
  pres.title = "研发资本化风险排序与问询函可行性测试";
  pres.subject = "Data Mining & Machine Learning Course Project 2";

  const TOTAL = 14;

  // ═══════════════════════════════════════════════════════════════════
  // Slide 1: Cover
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    // Accent bar at top
    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.mint } });

    // Title
    s.addText("研发资本化风险排序\n与问询函可行性测试", {
      x: 0.8, y: 1.2, w: 8.4, h: 1.8,
      fontSize: 38, fontFace: FONT.header, color: C.white, bold: true,
      align: "left", margin: 0,
    });

    // Subtitle
    s.addText("基于 150 份年报 PDF 的结构化抽取与风险评分", {
      x: 0.8, y: 3.1, w: 8.4, h: 0.5,
      fontSize: 18, fontFace: FONT.body, color: C.seafoam,
      align: "left", margin: 0,
    });

    // Info line
    s.addText("数据挖掘与机器学习 · 课程项目二 · 2026 年 6 月", {
      x: 0.8, y: 4.6, w: 8.4, h: 0.4,
      fontSize: 13, fontFace: FONT.body, color: C.muted,
      align: "left", margin: 0,
    });

    s.addNotes("开场不读封面，直接跳到第2页说金融问题。封面只在教室屏幕亮着即可。GitHub 公开仓库 URL 见报告。");
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 2: 金融问题  (Rubric ①)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "金融问题：哪些研发资本化特征与交易所问询相关？", 23);
    addBottomLine(s);

    // Three sub-questions in card layout
    const cards = [
      { title: "子问题 1", body: "高资本化率是否更容易\n与问询相关？", sub: "行业偏离度" },
      { title: "子问题 2", body: "资本化率的剧烈变化\n是否更容易与问询相关？", sub: "跨期变化" },
      { title: "子问题 3", body: "资本化条件描述模糊\n是否更容易与问询相关？", sub: "文本模糊度" },
    ];

    cards.forEach((card, i) => {
      const cx = 0.6 + i * 3.1;
      // Card background
      s.addShape("rect", {
        x: cx, y: 1.15, w: 2.85, h: 2.3,
        fill: { color: C.offWhite }, shadow: makeShadow(),
      });
      // Card number
      s.addText(card.title, {
        x: cx + 0.2, y: 1.25, w: 2.45, h: 0.35,
        fontSize: 11, fontFace: FONT.body, color: C.teal, bold: true, margin: 0,
      });
      // Card body
      s.addText(card.body, {
        x: cx + 0.2, y: 1.6, w: 2.45, h: 1.2,
        fontSize: 16, fontFace: FONT.body, color: C.body, margin: 0,
      });
      // Card tag
      s.addText(card.sub, {
        x: cx + 0.2, y: 2.9, w: 2.45, h: 0.35,
        fontSize: 11, fontFace: FONT.body, color: C.teal,
        bold: true, margin: 0,
      });
    });

    // Bottom positioning statement
    s.addText("定位：风险排序，不是违规判定。输出的是「复核清单」，不是「黑名单」。", {
      x: 0.6, y: 3.75, w: 8.8, h: 0.6,
      fontSize: 14, fontFace: FONT.body, color: C.accent, bold: true,
      align: "center", margin: 0,
    });

    s.addNotes("这一页要讲清楚「我们做的是什么、不做什么」。「风险排序≠违规判定」要在这页就明确说出来，避免老师后面追问。");
    addSlideNumber(s, 2, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 3: 数据来源与难度档
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    bulletSlide(pres, s,
      "数据来源与规模",
      [
        "数据来源：巨潮资讯网（www.cninfo.com.cn）公开公告，深证信官方 API（OAuth2 认证）",
        "50 家公司 × 3 年（2021-2023）= 150 份年报 PDF，三大行业覆盖",
        "医药制造 20 家 + 电子设备 20 家 + 软件信息 10 家",
        "150 个唯一 SHA256，collision = 0 —— 数据去重完整",
        "难度档位：🔴 挑战档（≥50 份 PDF、≥10 字段、多公告类型、闭环分析）",
      ],
      "强调「挑战档」三个字——数据量和复杂度远超课程基本要求。150 份年报的 SHA256 审计确保没有重复文件，这是数据质量的基础。",
      3
    );
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 4: Schema  (Rubric ②)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "Schema 设计：观察单位与核心字段");
    addBottomLine(s);

    // Two-column: left = design decisions, right = key fields
    // Left column
    s.addText([
      { text: "观察单位", options: { bold: true, fontSize: 14, color: C.teal, breakLine: true } },
      { text: "company-year（公司 × 年报年度）", options: { fontSize: 13, breakLine: true, paraSpaceAfter: 14 } },
      { text: "设计原则", options: { bold: true, fontSize: 14, color: C.teal, breakLine: true } },
      { text: "不训练 ML 模型\n全部使用可解释的金融规则\n每个关键字段带 evidence_text + page_no", options: { fontSize: 13, breakLine: true } },
    ], {
      x: 0.6, y: 1.05, w: 4.2, h: 3.8,
      valign: "top", margin: 0,
    });

    // Right column — field table
    const fieldRows = [
      [{ text: "字段", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, fontSize: 11 } },
       { text: "类型", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, fontSize: 11 } }],
      ["capitalization_rate", "核心自变量"],
      ["industry_percentile", "核心自变量"],
      ["change_zscore", "核心自变量"],
      ["fuzziness_score", "核心自变量"],
      ["capitalization_related", "因变量（问询标签）"],
      ["evidence_text", "证据字段"],
    ];

    s.addTable(fieldRows, {
      x: 5.2, y: 1.05, w: 4.4,
      colW: [2.2, 2.2],
      border: { pt: 0.5, color: C.tableBorder },
      fontFace: FONT.body,
      fontSize: 11,
      color: C.body,
      rowH: [0.35, 0.32, 0.32, 0.32, 0.32, 0.32, 0.32],
      autoPage: false,
    });

    s.addNotes("在 PPT 上放 Schema 的字段表截图或简表，不要列全部 14 个字段——列核心的 6-8 个即可。重点解释「为什么每个字段都要带 evidence_text」。");
    addSlideNumber(s, 4, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 5: MinerU 解析 + Section 检查
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    bulletSlide(pres, s,
      "MinerU 解析与 Section 路由",
      [
        "MinerU API batch：150 份 PDF → Markdown，275 个 page segment 全部 success",
        "超过 200 页的年报自动分段提交，保留 HTML 表格结构",
        "Section 路由：5 条规则（研发费用 / 开发支出 / 无形资产 / 资本化政策 / 收入确认）",
        "关键词匹配 + 正负向打分，输出 750 行真实 corpus 数据",
        "输出：outputs/reports/section_check_report.csv（完整可审计）",
      ],
      "可以用中兴通讯年报的 MinerU 输出截图——展示 <table> 标签里的研发投入三行数值。这是最直观的「PDF 变成结构化数据」的证据。",
      5
    );
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 6: Workflow 全图
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "Workflow：13 阶段 Pipeline");
    addBottomLine(s);

    // Pipeline flow as horizontal steps
    const stages = [
      "crawl", "download", "audit", "parse", "route",
      "extract", "validate", "score", "detect", "inquiry",
      "label", "analyze", "report",
    ];
    const startX = 0.3;
    const boxW = 0.62;
    const gap = 0.08;

    stages.forEach((name, i) => {
      const x = startX + i * (boxW + gap);
      const isKey = ["parse", "extract", "validate", "score"].includes(name);

      s.addShape("rect", {
        x, y: 1.3, w: boxW, h: 0.55,
        fill: { color: isKey ? C.teal : C.offWhite },
        shadow: isKey ? makeShadow() : undefined,
      });
      s.addText(name, {
        x, y: 1.3, w: boxW, h: 0.55,
        fontSize: 7.5, fontFace: FONT.body, color: isKey ? C.white : C.body,
        align: "center", valign: "middle", margin: 0,
      });

      // Arrow between boxes
      if (i < stages.length - 1) {
        s.addText("→", {
          x: x + boxW, y: 1.3, w: gap, h: 0.55,
          fontSize: 7, color: C.muted, align: "center", valign: "middle", margin: 0,
        });
      }
    });

    // Key features below
    const features = [
      { icon: "🔗", text: "确定性表格提取 + LLM 抽取双路线" },
      { icon: "✅", text: "Pydantic 校验 + 会计恒等式（5% 阈值）" },
      { icon: "⚡", text: "CLI 一键调度：uv run python src/main.py --from-stage validate --to-stage report" },
      { icon: "🧪", text: "测试覆盖：51 个 pytest 用例" },
    ];

    features.forEach((f, i) => {
      const y = 2.25 + i * 0.65;
      s.addShape("rect", {
        x: 0.6, y, w: 8.8, h: 0.5,
        fill: { color: C.offWhite },
      });
      s.addText(f.icon, {
        x: 0.75, y, w: 0.4, h: 0.5,
        fontSize: 16, align: "center", valign: "middle", margin: 0,
      });
      s.addText(f.text, {
        x: 1.2, y, w: 8.0, h: 0.5,
        fontSize: 12, fontFace: FONT.body, color: C.body, valign: "middle", margin: 0,
      });
    });

    s.addNotes("不要在 PPT 上放完整代码——放一张 pipeline 流程图（箭头 + 阶段名），口头解释每个阶段做什么。强调「从 PDF 到混淆矩阵只需要一条命令」。");
    addSlideNumber(s, 6, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 7: 风险评分模型四维  (Rubric ②③)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "风险评分模型：四维信号聚合");
    addBottomLine(s);

    // Three signal cards with weights
    const signals = [
      { label: "行业偏离度\nIndustry Score", weight: "0.25", formula: "资本化率在同行业同年度的\n百分位 × 100" },
      { label: "跨期变化\nChange Score", weight: "0.25", formula: "仅取正向跳升（资本化率\n突然上升），Z-score/2 × 100" },
      { label: "条件模糊度\nFuzziness Score", weight: "0.25", formula: "会计估计模糊词命中数 /\n（文本长度/200）× 100" },
    ];

    signals.forEach((sig, i) => {
      const cx = 0.6 + i * 3.1;
      s.addShape("rect", {
        x: cx, y: 1.15, w: 2.85, h: 2.2,
        fill: { color: C.offWhite }, shadow: makeShadow(),
      });
      s.addText(sig.label, {
        x: cx + 0.15, y: 1.2, w: 2.55, h: 0.65,
        fontSize: 12, fontFace: FONT.header, color: C.teal, bold: true, margin: 0,
      });
      s.addText(`权重 ${sig.weight}`, {
        x: cx + 0.15, y: 1.85, w: 2.55, h: 0.3,
        fontSize: 10, fontFace: FONT.body, color: C.accent, margin: 0,
      });
      s.addText(sig.formula, {
        x: cx + 0.15, y: 2.15, w: 2.55, h: 1.0,
        fontSize: 11, fontFace: FONT.body, color: C.body, margin: 0,
      });
    });

    // Identity multiplier callout
    s.addShape("rect", {
      x: 0.6, y: 3.65, w: 8.8, h: 0.65,
      fill: { color: C.dark },
    });
    s.addText("恒等式置信度乘数 I：金额关系越一致，置信度越高；不一致时打折扣而非加信号", {
      x: 0.8, y: 3.65, w: 8.4, h: 0.65,
      fontSize: 12, fontFace: FONT.body, color: C.white, valign: "middle", margin: 0,
    });

    // Final formula
    s.addText("RS = Σ(wᵢ·Sᵢ) / Σwᵢ  ×  I       默认 w 各 0.25，等权即 (IS+CS+FC)/3", {
      x: 0.6, y: 4.55, w: 8.8, h: 0.45,
      fontSize: 15, fontFace: FONT.header, color: C.teal, bold: true,
      align: "center", margin: 0,
    });

    s.addNotes("公式用 LaTeX 渲染或手写体展示。重点解释「为什么 I 是乘数不是加项」——这体现了审慎原则。");
    addSlideNumber(s, 7, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 8: 结果与 Top-K  (Rubric ③)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "当前结果：关键数字");
    addBottomLine(s);

    // Big stat callouts in a row
    const stats = [
      { value: "150", label: "年报 PDF", sub: "全部通过 validate" },
      { value: "83 / 67", label: "有风险分 / 未评分", sub: "no-score 默认非异常" },
      { value: "11.57%", label: "资本化率均值", sub: "中位数 2.67%（n=60）" },
      { value: "17", label: "异常条数", sub: "industry_outlier 16 + change_spike 1" },
    ];

    stats.forEach((st, i) => {
      const cx = 0.3 + i * 2.4;
      s.addText(st.value, {
        x: cx, y: 1.1, w: 2.2, h: 0.7,
        fontSize: 32, fontFace: FONT.header, color: C.teal, bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      s.addText(st.label, {
        x: cx, y: 1.8, w: 2.2, h: 0.35,
        fontSize: 11, fontFace: FONT.body, color: C.body, align: "center", margin: 0,
      });
      s.addText(st.sub, {
        x: cx, y: 2.1, w: 2.2, h: 0.3,
        fontSize: 9, fontFace: FONT.body, color: C.body, align: "center", margin: 0,
      });
    });

    // Industry/Year comparison table
    const compRows = [
      [{ text: "维度", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "分组", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "资本化率均值", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } }],
      ["行业", "医药制造", "15.26%"],
      ["行业", "电子设备", "7.62%"],
      ["行业", "软件信息", "19.09%"],
      ["年度", "2021", "11.45%"],
      ["年度", "2022", "18.03%"],
      ["年度", "2023", "5.47%"],
      ["异常组 vs 非异常", "23.81% vs 6.73%", ""],
    ];

    s.addTable(compRows, {
      x: 0.6, y: 2.65, w: 8.8,
      colW: [2.5, 3.0, 3.3],
      border: { pt: 0.5, color: C.tableBorder },
      fontFace: FONT.body,
      fontSize: 10,
      color: C.body,
      rowH: [0.3, 0.28, 0.28, 0.28, 0.28, 0.28, 0.28, 0.28],
      autoPage: false,
    });

    s.addNotes("把 Top-10 异常表放 PPT 上（或口头列出前3），口头指出「前 3 名资本化率 0% 但满分 50——这是行业百分位不分方向的局限」。");
    addSlideNumber(s, 8, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 9: Demo 证据链 — 中兴通讯 2021  (Rubric ③ 核心)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "Demo 证据链：中兴通讯 2021 年报");
    addBottomLine(s);

    // Pipeline flow top
    s.addText("PDF 年报  →  MinerU Markdown  →  Section 定位  →  LLM 抽取  →  校验  →  最终结果", {
      x: 0.6, y: 0.95, w: 8.8, h: 0.4,
      fontSize: 11, fontFace: FONT.body, color: C.muted, align: "center", margin: 0,
    });

    // Evidence table
    const evidenceRows = [
      [{ text: "项目", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, fontSize: 10 } },
       { text: "金额（万元）", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, fontSize: 10 } },
       { text: "evidence_text（原文片段）", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, fontSize: 10 } }],
      ["研发投入总额", "1,880,400", "「研发投入金额 18,804.0」"],
      ["资本化金额", "180,650", "「资本化的金额 1,806.5」"],
      ["费用化金额", "1,699,750", "「费用化的金额 16,997.5」"],
      ["资本化率", "9.61%", "「资本化研发投入占研发投入的比例 9.61%」"],
    ];

    s.addTable(evidenceRows, {
      x: 0.6, y: 1.5, w: 8.8,
      colW: [2.0, 2.2, 4.6],
      border: { pt: 0.5, color: C.tableBorder },
      fontFace: FONT.body,
      fontSize: 11,
      color: C.body,
      rowH: [0.35, 0.35, 0.35, 0.35, 0.35],
      autoPage: false,
    });

    // Identity check
    s.addShape("rect", {
      x: 0.6, y: 3.4, w: 8.8, h: 0.5,
      fill: { color: C.offWhite },
    });
    s.addText("会计恒等式：180,650 + 1,699,750 = 1,880,400  ✓  差异 < 0.01%", {
      x: 0.8, y: 3.4, w: 8.4, h: 0.5,
      fontSize: 13, fontFace: FONT.body, color: C.teal, bold: true, valign: "middle", margin: 0,
    });

    // Final result
    s.addText([
      { text: "最终结果：", options: { fontSize: 14, color: C.body } },
      { text: "风险分 35.715  ·  非异常  ·  TN  ", options: { fontSize: 14, color: C.teal, bold: true } },
    ], {
      x: 0.6, y: 4.15, w: 8.8, h: 0.5,
      align: "center", valign: "middle", margin: 0,
    });

    s.addNotes("这是全场最关键的一页。一定要在 PPT 上展示 MinerU 输出的 Markdown 表格截图，旁边放 LLM 抽取的 JSON 结果。让老师看到 evidence_text 确实是原文片段。");
    addSlideNumber(s, 9, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 10: 闭环矩阵与 TN 水分  (Rubric ④)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "闭环矩阵与 TN 水分：诚实呈现结果");
    addBottomLine(s);

    // Confusion matrix
    const cmRows = [
      [{ text: "混淆矩阵", options: { bold: true, fill: { color: C.tableHeader }, color: C.white, colSpan: 3 } },
       {}, {}],
      [{ text: "", options: { bold: true, fill: { color: C.offWhite } } },
       { text: "预测异常", options: { bold: true, fill: { color: C.offWhite } } },
       { text: "预测非异常", options: { bold: true, fill: { color: C.offWhite } } }],
      [{ text: "实际异常", options: { bold: true, fill: { color: C.offWhite } } },
       { text: "TP = 0", options: { color: C.red, bold: true } },
       { text: "FN = 1", options: { color: C.red } }],
      [{ text: "实际非异常", options: { bold: true, fill: { color: C.offWhite } } },
       { text: "FP = 17", options: { color: C.accent } },
       { text: "TN = 132", options: {} }],
    ];

    s.addTable(cmRows, {
      x: 0.6, y: 1.05, w: 4.2,
      colW: [1.5, 1.35, 1.35],
      border: { pt: 0.5, color: C.tableBorder },
      fontFace: FONT.body,
      fontSize: 11,
      color: C.body,
      rowH: [0.35, 0.3, 0.3, 0.3],
      autoPage: false,
    });

    // Metrics box
    s.addText([
      { text: "Precision = 0.0", options: { breakLine: true, fontSize: 13, color: C.red, bold: true } },
      { text: "Recall = 0.0", options: { breakLine: true, fontSize: 13, color: C.red } },
      { text: "Top-K Precision = 0.0", options: { fontSize: 13, color: C.red, breakLine: true } },
    ], {
      x: 0.8, y: 2.5, w: 3.8, h: 1.2,
      margin: 0,
    });

    // TN water callout
    s.addShape("rect", {
      x: 5.2, y: 1.05, w: 4.4, h: 2.0,
      fill: { color: C.offWhite }, shadow: makeShadow(),
    });
    s.addText([
      { text: "TN 水分 ⚠", options: { bold: true, fontSize: 14, color: C.accent, breakLine: true } },
      { text: "TN = 132 中 67 条缺数据未评分\n默认归非异常", options: { fontSize: 12, color: C.body, breakLine: true, paraSpaceAfter: 10 } },
      { text: "→ TN 被高估", options: { fontSize: 12, color: C.red, bold: true, breakLine: true, paraSpaceAfter: 10 } },
      { text: "唯一 FN：汇顶科技 2022\n收到研发资本化相关监管工作函\n但资本化率字段缺失，风险分=0.0", options: { fontSize: 11, color: C.body, breakLine: true } },
      { text: "→ 问题出在输入覆盖，不是评分逻辑", options: { fontSize: 11, color: C.muted, italic: true } },
    ], {
      x: 5.4, y: 1.15, w: 4.0, h: 1.8,
      valign: "top", margin: 0,
    });

    // Baseline comparison label
    s.addText("三个 Baseline 对比（precision 全部 ≈ 0）", {
      x: 0.6, y: 3.45, w: 8.8, h: 0.3,
      fontSize: 11, fontFace: FONT.body, color: C.muted, bold: true, margin: 0,
    });

    // Baseline comparison table at bottom
    const blRows = [
      [{ text: "Baseline", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "预测数", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "TP", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "FP", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "FN", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } },
       { text: "Precision", options: { bold: true, fill: { color: C.tableHeader }, color: C.white } }],
      ["规则评分", "17", "0", "17", "1", "0.0"],
      ["cap_rate top20%", "12", "0", "12", "1", "0.0"],
      ["全标正", "150", "1", "149", "0", "0.0067"],
    ];

    s.addTable(blRows, {
      x: 0.6, y: 3.78, w: 8.8,
      colW: [2.0, 1.2, 1.2, 1.2, 1.2, 2.0],
      border: { pt: 0.5, color: C.tableBorder },
      fontFace: FONT.body,
      fontSize: 10,
      color: C.body,
      rowH: [0.3, 0.28, 0.28, 0.28],
      autoPage: false,
    });

    s.addNotes("这一页要诚实。不要试图掩饰 TP=0——直接说「正样本只有 1 条，所有策略 precision 都接近 0，在这个样本池上不存在可用的预测信号」。但强调「方法链路已经接通，问询闭环的工程管道可用」。");
    addSlideNumber(s, 10, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 11: 失败案例与评估局限  (Rubric ④)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "失败案例与评估局限");
    addBottomLine(s);

    // Three categories as cards
    const limits = [
      {
        title: "评分模型局限",
        items: "行业百分位不分方向（0% 资本化率也得满分）\n参数全部启发式、未校准",
      },
      {
        title: "抽取质量（35 条人工评估）",
        items: "准确率 46.4%\nsection_error 27 / data_error 20 / hallucination 8\n评估 agent 与 extractor 同源 LLM——共错风险",
      },
      {
        title: "问询标签",
        items: "MVP 版本（关键词剪枝 + LLM 语义初筛）\n正样本仅 1 条，统计上无法评估\n其他：page_no 缺失、跨期变化仅覆盖两年",
      },
    ];

    limits.forEach((lim, i) => {
      const cx = 0.6 + i * 3.1;
      s.addShape("rect", {
        x: cx, y: 1.15, w: 2.85, h: 3.0,
        fill: { color: C.offWhite }, shadow: makeShadow(),
      });
      s.addText(lim.title, {
        x: cx + 0.15, y: 1.2, w: 2.55, h: 0.4,
        fontSize: 12, fontFace: FONT.header, color: C.teal, bold: true, margin: 0,
      });
      s.addText(lim.items, {
        x: cx + 0.15, y: 1.65, w: 2.55, h: 2.3,
        fontSize: 11, fontFace: FONT.body, color: C.body, valign: "top", margin: 0,
      });
    });

    s.addText("每个局限都有对应的改进方向 —— 详见报告 §13", {
      x: 0.6, y: 4.5, w: 8.8, h: 0.4,
      fontSize: 12, fontFace: FONT.body, color: C.muted, italic: true, align: "center", margin: 0,
    });

    s.addNotes("不要把这页念成「我们做得很差」——要念成「我们知道局限在哪里，而且每个局限都有对应的改进方向」。把局限分类讲（评分模型/抽取质量/标签），每类 1-2 句。");
    addSlideNumber(s, 11, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 12: Vibe Coding 反思  (Rubric ⑤)
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "Vibe Coding 反思：AI 帮了什么、错在哪、如何验证");
    addBottomLine(s);

    // Two columns: left = AI helped, right = AI errors
    // Left
    s.addShape("rect", {
      x: 0.6, y: 1.05, w: 4.2, h: 3.2,
      fill: { color: C.offWhite },
    });
    s.addText("✅ AI 帮了什么", {
      x: 0.8, y: 1.1, w: 3.8, h: 0.35,
      fontSize: 14, fontFace: FONT.header, color: C.seafoam, bold: true, margin: 0,
    });
    s.addText([
      { text: "全流程 13 阶段代码生成", options: { bullet: true, breakLine: true, fontSize: 11 } },
      { text: "MinerU 环境 bug 逐层诊断", options: { bullet: true, breakLine: true, fontSize: 11 } },
      { text: "方法论审计（fuzziness 词表去毒、\nchange_zscore 方向修正、industry 显式化）", options: { bullet: true, fontSize: 11 } },
    ], {
      x: 0.8, y: 1.5, w: 3.8, h: 2.5,
      valign: "top", margin: 0,
    });

    // Right
    s.addShape("rect", {
      x: 5.2, y: 1.05, w: 4.4, h: 3.2,
      fill: { color: C.offWhite },
    });
    s.addText("❌ AI 在哪里出错", {
      x: 5.4, y: 1.1, w: 4.0, h: 0.35,
      fontSize: 14, fontFace: FONT.header, color: C.red, bold: true, margin: 0,
    });
    s.addText([
      { text: "fuzziness 词表含「等/相关/未来」（未看数据就设词表）", options: { bullet: true, breakLine: true, fontSize: 11 } },
      { text: "change_zscore 用 abs()（没区分上升/下降的经济含义）", options: { bullet: true, breakLine: true, fontSize: 11 } },
      { text: "行业靠顺序推断（文档声称申万一级，代码实际靠猜）", options: { bullet: true, breakLine: true, fontSize: 11 } },
      { text: "文档 overclaim（「异常检测」「闭环验证」→ 改为「风险排序」「可行性测试」）", options: { bullet: true, fontSize: 11 } },
    ], {
      x: 5.4, y: 1.5, w: 4.0, h: 2.5,
      valign: "top", margin: 0,
    });

    // Verification bar at bottom
    s.addShape("rect", {
      x: 0.6, y: 4.5, w: 8.8, h: 0.5,
      fill: { color: C.dark },
    });
    s.addText("如何验证：硬数字强制溯源 loop_evaluation.json + 51 个 pytest + mini pipeline + 35 条人工抽查", {
      x: 0.8, y: 4.5, w: 8.4, h: 0.5,
      fontSize: 11, fontFace: FONT.body, color: C.white, valign: "middle", margin: 0,
    });

    s.addNotes("不要泛泛地说「AI 提高了效率」——要具体到「fuzziness 词表里『等』字导致所有记录的模糊度评分被无差别抬升」这种级别的案例。老师要看到你确实用了 AI，也知道 AI 错在哪里。");
    addSlideNumber(s, 12, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 13: 局限与下一步
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addSectionHeader(s, "8 个已知局限与下一步");
    addBottomLine(s);

    const limitItems = [
      "正样本太少（1/150）",
      "TN 含水（67/132 条未评分默认非异常）",
      "问询标签 MVP 版本",
      "page_no 缺失",
      "抽取准确率 46.4%",
      "参数全部启发式",
      "评估 agent 与 extractor 同源 LLM",
      "行业百分位不分方向",
    ];

    // 2-column grid of limit items
    limitItems.forEach((item, i) => {
      const col = i < 4 ? 0 : 1;
      const cy = 1.1 + (i % 4) * 0.7;
      const cx = col === 0 ? 0.6 : 5.2;

      s.addShape("rect", {
        x: cx, y: cy, w: 4.3, h: 0.55,
        fill: { color: C.offWhite },
      });
      s.addText(`${i + 1}.  ${item}`, {
        x: cx + 0.15, y: cy, w: 4.0, h: 0.55,
        fontSize: 12, fontFace: FONT.body, color: C.body, valign: "middle", margin: 0,
      });
    });

    // Next steps
    s.addShape("rect", {
      x: 0.6, y: 4.1, w: 8.8, h: 0.8,
      fill: { color: C.teal },
    });
    s.addText("如果有更多时间 → 扩大公司池 · 全文语义标签 · 参数敏感性分析 · 抽取质量提升", {
      x: 0.8, y: 4.1, w: 8.4, h: 0.8,
      fontSize: 13, fontFace: FONT.body, color: C.white, bold: true,
      valign: "middle", align: "center", margin: 0,
    });

    s.addNotes("快速过（每点 5-10 秒），不要展开。重点是让老师看到「你知道自己项目哪里还不够好」——这本身就是学术素养的体现。");
    addSlideNumber(s, 13, TOTAL);
  }

  // ═══════════════════════════════════════════════════════════════════
  // Slide 14: 答辩问题预案
  // ═══════════════════════════════════════════════════════════════════
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.mint } });

    s.addText("答辩问题预案", {
      x: 0.6, y: 0.25, w: 8.8, h: 0.55,
      fontSize: 28, fontFace: FONT.header, color: C.white, bold: true, margin: 0,
    });

    const qas = [
      { q: "Q1: TP=0，这项目还有什么意义？", a: "方法链路已可工作，正样本少是数据特征而非方法失败。诚实呈现「信号不足」本身就是科学结论。" },
      { q: "Q2: 为什么不用 ML 模型？", a: "课程明确「不训练大模型」；规则评分可解释，每个维度的金融含义清晰，适合审计师/分析师场景。" },
      { q: "Q3: 问询标签怎么做的？", a: "当前是 MVP（关键词剪枝+LLM 初筛）。全文语义标签是下一步，受限于时间和 API 成本。" },
      { q: "Q4: 人工评估 46.4% 的准确率能接受吗？", a: "不能接受作为最终产品，但能接受作为 MVP。诚实标注了同源 LLM 共错风险，主要错误类型已定位。" },
      { q: "Q5: 资本化率 0% 为什么风险分满分？", a: "行业百分位的设计 bug——只度量偏离度不区分方向。已在局限中如实说明。" },
      { q: "Q6: 50 家公司怎么选的？", a: "申万一级分类（医药制造/电子设备/软件信息），crawl.yaml 显式配置。覆盖研发密集型行业。" },
    ];

    qas.forEach((qa, i) => {
      const y = 0.95 + i * 0.68;
      // Q number background
      s.addShape("rect", {
        x: 0.6, y, w: 0.5, h: 0.55,
        fill: { color: C.teal },
      });
      s.addText(`Q${i + 1}`, {
        x: 0.6, y, w: 0.5, h: 0.55,
        fontSize: 10, fontFace: FONT.body, color: C.white, bold: true,
        align: "center", valign: "middle", margin: 0,
      });
      // Question
      s.addText(qa.q, {
        x: 1.25, y, w: 3.5, h: 0.55,
        fontSize: 10, fontFace: FONT.body, color: C.seafoam, bold: true,
        valign: "middle", margin: 0,
      });
      // Answer
      s.addText(qa.a, {
        x: 4.85, y, w: 4.8, h: 0.55,
        fontSize: 9, fontFace: FONT.body, color: C.muted,
        valign: "middle", margin: 0,
      });
    });

    // Bottom note
    s.addText("优先准备 Q1-Q3（老师最可能问的三个）", {
      x: 0.6, y: 5.15, w: 8.8, h: 0.3,
      fontSize: 9, fontFace: FONT.body, color: C.muted, italic: true, align: "right", margin: 0,
    });

    s.addNotes("PPT 上只列问题关键词，不列完整答案——答案要能口头展开。如果时间紧，优先准备 Q1-Q3（老师最可能问的三个）。");
    addSlideNumber(s, 14, TOTAL);
  }

  // ── Save ──────────────────────────────────────────────────────────
  const outPath = "outputs/final_slides.pptx";
  pres.writeFile({ fileName: outPath }).then(() => {
    console.log("✓ Written:", outPath);
  }).catch(err => {
    console.error("✗ Error:", err.message);
    process.exit(1);
  });
}

buildPresentation();
