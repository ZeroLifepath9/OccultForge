/** Occult Forge — permanent natal chart boxes, modal deep-reads, combined panels. */

const NUMEROLOGY_BOX = { id: "numerology", label: "Occult Numerology" };
const BAZI_BOX = { id: "bazi", label: "BaZi Pillars" };

const TRADITION_TOKEN_LABELS = {
  vedic: "Vedic",
  hellenistic: "Hellenistic",
  financial: "Financial/Mundane",
};

const CHART_SELECTABLE = [
  {
    id: "vedic",
    label: "Vedic / Jyotish (Sidereal)",
    wide: false,
    blurb:
      "Indian system, tied to Vedic texts. Emphasizes karma, dashas (planetary periods for precise timing), nakshatras (lunar mansions), and divisional charts. Strong in prediction, compatibility, and remedial measures (mantras, gems). Often seen as more event-oriented than psychological.",
  },
  {
    id: "hellenistic",
    label: "Hellenistic Astrology",
    wide: false,
    blurb:
      "Ancient Greco-Egyptian (roots of Western). Predictive, fate-focused, uses whole-sign houses and lots. Shares similarities with Vedic.",
  },
  {
    id: "financial",
    label: "Financial / Mundane",
    wide: false,
    blurb:
      "Overlaps with all, using planetary cycles for markets (e.g., Jupiter–Saturn for economic waves). Modern hybrids: Cosmobiology, Uranian, Harmonic.",
  },
];

const COMBINED_BOXES = [{ id: "relationships", label: "Relationships", wide: true }];

const ALL_CHART_BOXES = [...CHART_SELECTABLE, ...COMBINED_BOXES, BAZI_BOX, NUMEROLOGY_BOX];



let selectedChartSystem = null;
const chartReadingCache = {};

function escapeChartText(text) {
  const div = document.createElement("div");
  div.textContent = text || "";
  return div.innerHTML;
}

function formatMatrixNarrative(text) {
  const raw = (text || "").trim();
  const labels = [
    ["Direct Answer", "matrix-section--direct"],
    ["Decoded Insight", "matrix-section--decoded"],
    ["Action", "matrix-section--action"],
  ];
  let rest = raw;
  const blocks = [];
  for (const [label, cls] of labels) {
    const marker = `**${label}**`;
    const idx = rest.indexOf(marker);
    if (idx === -1) continue;
    const after = rest.slice(idx + marker.length).trim();
    const nextIdx = labels
      .map(([l]) => after.indexOf(`**${l}**`))
      .filter((i) => i >= 0)
      .sort((a, b) => a - b)[0];
    const body = (nextIdx != null && nextIdx >= 0 ? after.slice(0, nextIdx) : after)
      .replace(/\n{3,}/g, "\n\n")
      .trim();
    blocks.push(
      `<section class="matrix-section ${cls}"><h5 class="matrix-section-label">${label}</h5><div class="matrix-section-body">${formatMatrixBody(body)}</div></section>`
    );
    rest = nextIdx != null && nextIdx >= 0 ? after.slice(nextIdx) : "";
  }
  const tail = rest.replace(/^\*\*[^*]+\*\*/, "").trim();
  const close =
    tail && /matrix decoded\.?$/i.test(tail)
      ? `<p class="matrix-close">${escapeChartText(tail)}</p>`
      : raw.includes("Matrix decoded.")
        ? `<p class="matrix-close">Matrix decoded.</p>`
        : "";
  if (!blocks.length) return formatFlowNarrativeLegacy(raw);
  return `<div class="flow-read flow-read--matrix">${blocks.join("")}${close}</div>`;
}

function formatMatrixBody(body) {
  const chunks = body.split(/\n\n+/).map((p) => p.replace(/\n/g, " ").trim()).filter(Boolean);
  if (!chunks.length) return `<p class="flow-para">${escapeChartText(body)}</p>`;
  return chunks.map((p) => `<p class="flow-para">${escapeChartText(p)}</p>`).join("");
}

function formatFlowNarrativeLegacy(text) {
  const raw = (text || "").trim();
  if (!raw) return "";
  const paras = raw.split(/\n\n+/).map((p) => p.replace(/\n/g, " ").trim()).filter(Boolean);
  if (!paras.length) paras.push(raw);
  return `<div class="flow-read">${paras.map((p) => `<p class="flow-para">${escapeChartText(p)}</p>`).join("")}</div>`;
}

function formatFlowNarrative(text) {
  const raw = (text || "").trim();
  if (!raw) return "";
  if (raw.includes("**Direct Answer**")) return formatMatrixNarrative(raw);
  return formatFlowNarrativeLegacy(raw);
}

function formatNumerologyPanels(panels) {
  if (!panels) return "";
  const lp = panels.life_path || {};
  const pi = panels.path_insight || {};
  const compound = lp.compound;
  const final = lp.value;
  const lpHtml =
    compound != null && final != null && compound !== final
      ? `<span class="num-lp-compound">${escapeChartText(String(compound))}</span><span class="num-lp-sep">/</span><span class="num-lp-final">${escapeChartText(String(final))}</span>`
      : `<span class="num-lp-single">${escapeChartText(lp.display || "—")}</span>`;

  const friends = (panels.friend_numbers || []).join(", ");
  const enemies = (panels.enemy_numbers || []).join(", ");

  const totals = (panels.other_totals || [])
    .map(
      (row) => `
      <li class="num-total-row">
        <div class="num-total-head">
          <span class="num-total-label">${escapeChartText(row.label)}</span>
          <strong class="num-total-display">${escapeChartText(row.display)}</strong>
        </div>
        <p class="num-total-advice">${escapeChartText(row.advice)}</p>
        <p class="num-total-path">${escapeChartText(row.path)}</p>
      </li>`
    )
    .join("");

  const subtitleHtml = panels.compound_subtitle
    ? `<p class="num-compound-subtitle">${escapeChartText(panels.compound_subtitle)}</p>`
    : "";

  return `
    <div class="num-read">
      <section class="num-hero-centered">
        <p class="num-birth">${escapeChartText(panels.birth_date)}</p>
        <div class="num-hero-row">
          <p class="num-digit-sum">${escapeChartText(panels.birth_digit_sum || "—")}</p>
          <div class="num-allies">
            <p class="num-allies-line"><span class="num-allies-label">Friend number</span> ${escapeChartText(friends || "—")}</p>
            <p class="num-allies-line"><span class="num-allies-label">Enemy number</span> ${escapeChartText(enemies || "—")}</p>
          </div>
        </div>
        <p class="num-lp num-lp-centered" aria-label="Life path">${lpHtml}</p>
        <h4 class="num-compound-title num-compound-title-centered">${escapeChartText(panels.compound_title)}</h4>
        ${subtitleHtml}
      </section>
      <section class="num-path-insight">
        <dl class="num-insight-grid">
          <div class="num-insight-avatar">
            <dt>Your avatar</dt>
            <dd>${escapeChartText(pi.avatar)}</dd>
          </div>
        </dl>
      </section>
      <section class="num-other-totals">
        <h4 class="num-section-label">Other totals shaping your path</h4>
        <ul class="num-totals-list">${totals}</ul>
      </section>
    </div>`;
}

if (typeof window !== "undefined") {
  window.formatFlowNarrative = formatFlowNarrative;
  window.formatNumerologyPanels = formatNumerologyPanels;
}

function compoundNameFor(imprint) {
  const lp = imprint?.numerology?.schools?.pythagorean?.life_path;
  return lp ? numerologyDisplay(lp) : "—";
}

function birthDayNumber(imprint) {
  const b = imprint?.numerology?.schools?.pythagorean?.birthday;
  return b ? numerologyDisplay(b) : "—";
}

function numerologySummaryHtml(imprint) {
  const py = imprint.numerology.schools.pythagorean;
  const ch = imprint.numerology.schools.chaldean;
  const fields = [
    ["Life path (birth date vow)", py.life_path],
    ["Expression (public name-field)", py.expression],
    ["Soul urge (vowels)", py.soul_urge],
    ["Personality (consonants)", py.personality],
    ["Birth day number (lane)", py.birthday],
    ["Chaldean expression", ch.expression],
    ["Chaldean birth day", ch.birthday],
  ];
  const aka = imprint.numerology.commonly_known_as;
  if (aka) {
    fields.push(["Known-as expression", aka.expression]);
    fields.push(["Known-as soul urge", aka.soul_urge]);
  }
  return `
    <ul class="chart-summary-list">
      ${fields
        .map(
          ([label, n]) =>
            `<li><span class="chart-k">${label}</span> <span class="chart-sym-row"><span class="chart-sym chart-sym--num" aria-hidden="true">${numerologyDisplay(n)}</span></span> <strong>${numerologyDisplay(n)}</strong></li>`
        )
        .join("")}
    </ul>`;
}

const BAZI_HANZI = /[\u4e00-\u9fff]/g;
const BAZI_GANZHI_TOKEN = /\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b/g;

function stripBaziCitationNoise(text) {
  let t = String(text || "").trim();
  if (!t) return "";
  t = t.replace(BAZI_HANZI, "");
  t = t.replace(/\b[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\b/g, "");
  t = t.replace(BAZI_GANZHI_TOKEN, "");
  t = t.replace(/\b(day|year|month|hour)\s+pillar\b/gi, "this lane");
  t = t.replace(/\bDay Master\b/gi, "your core");
  t = t.replace(/\b\d{4}–\d{4}\b/g, "");
  t = t.replace(/\s{2,}/g, " ").replace(/\s+([,.;])/g, "$1").trim();
  if (t.endsWith(",") || t.endsWith(";")) t = t.slice(0, -1).trim();
  if (t && !/[.!?]$/.test(t)) t += ".";
  return t;
}

function extractConversationalInsight(line) {
  const raw = String(line || "").trim();
  if (!raw) return "";
  let t = raw;
  if (t.includes("—")) t = t.split("—").pop().trim();
  else if (/\s-\s/.test(t)) t = t.split(/\s-\s/).pop().trim();
  t = t.replace(/^Your current luck pillar suggests\s*/i, "");
  t = t.replace(/^(Year|Month|Day|Hour) pillar[^:]*:\s*/i, "");
  t = t.replace(/^[A-Za-z ]+ pillar \([^)]+\):\s*/i, "");
  t = t.replace(/^(Public inheritance|Working-years season|Daily self|Private engine)[^:]*:\s*/i, "");
  return stripBaziCitationNoise(t);
}

function baziConversationalSynopsisLines(imprint) {
  const lens = imprint?.bazi?.interpretation_lens || {};
  const luck = lens.luck_pillar || imprint?.bazi?.luck?.interpretation || {};
  const parts = [];

  (lens.advice_directives || []).forEach((line) => {
    const cleaned = extractConversationalInsight(line);
    if (cleaned.length >= 15) parts.push(cleaned);
  });

  const latent = lens.balance?.latent_insight || "";
  latent.split(/(?<=[.!?])\s+/).forEach((sentence) => {
    const cleaned = extractConversationalInsight(sentence);
    if (cleaned) parts.push(cleaned);
  });

  const alignSummary = luck.alignment_with_natal?.summary;
  if (alignSummary) {
    const cleaned = extractConversationalInsight(alignSummary);
    if (cleaned) parts.push(cleaned);
  }

  (luck.alignment_with_natal?.expands || []).forEach((line) => {
    const cleaned = extractConversationalInsight(line);
    if (cleaned) parts.push(cleaned);
  });

  if (!parts.length) {
    const fallback = extractConversationalInsight(baziBriefAssessment(imprint));
    if (fallback) parts.push(fallback);
  }

  const seen = new Set();
  return parts
    .filter((line) => {
      const key = line.toLowerCase().replace(/\s+/g, " ");
      if (!key || seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 6);
}

function filterSynopsisAgainstNarrative(lines, narrative) {
  const norm = String(narrative || "").toLowerCase();
  if (!norm) return lines;
  return lines.filter((line) => {
    const words = line.toLowerCase().split(/\s+/).filter((w) => w.length > 4);
    if (!words.length) return true;
    const hits = words.filter((w) => norm.includes(w)).length;
    return hits / words.length < 0.55;
  });
}

function baziSynopsisHtml(imprint, narrative) {
  const lines = filterSynopsisAgainstNarrative(baziConversationalSynopsisLines(imprint), narrative);
  const use = lines.length ? lines : baziConversationalSynopsisLines(imprint);
  return use
    .map((line) => `<p class="bazi-modal-synopsis-line">${escapeChartText(line)}</p>`)
    .join("");
}

function baziBriefAssessment(imprint) {
  const lens = imprint?.bazi?.interpretation_lens;
  const luck = lens?.luck_pillar || imprint?.bazi?.luck?.interpretation || {};
  const balance = lens?.balance?.balance_insight || lens?.balance?.latent_insight;
  const directive = lens?.advice_directives?.[0];
  const interaction = lens?.chart_interactions?.[0];
  const luckLine = luck.framework_insight || luck.current?.display_line;
  const dm = imprint?.bazi?.day_master;
  const dmLead =
    dm?.element && dm?.english
      ? `${dm.yin_yang || ""} ${dm.element} day master ${dm.english} leads the chart`
      : "";
  const raw =
    balance || directive || interaction || luckLine || dmLead || "Four pillars and luck decades seal your eastern astrology read.";
  const sentence = String(raw).split(/(?<=[.!?])\s+/)[0].trim();
  return sentence.endsWith(".") ? sentence : `${sentence}.`;
}

function baziCompactPillarRow(label, pillar, imprint, pillarKey, { yearStyle = false } = {}) {
  if (!pillar) return "";
  const lensCard = typeof lensPillarCard === "function" ? lensPillarCard(imprint, pillarKey) : null;
  const combined =
    lensCard?.identity || (typeof pillarIdentityLabel === "function" ? pillarIdentityLabel(pillar, { yearStyle }) : pillar.gan_zhi);
  const gz = pillar.gan_zhi || "";
  const el = pillar.stem_element || (typeof stemMeta === "function" ? stemMeta(pillar.stem).element : "");
  const elementLine =
    el && yearStyle
      ? `<span class="bazi-compact-el" title="Year stem element">${el}</span>`
      : el
        ? `<span class="bazi-compact-el bazi-compact-el--sub">${el}</span>`
        : "";
  return `
    <div class="bazi-compact-row">
      <span class="bazi-compact-k">${label}</span>
      <div class="bazi-compact-val">
        ${elementLine}
        <strong class="bazi-compact-identity">${combined}</strong>
        <span class="hanzi bazi-compact-hz">${gz}</span>
      </div>
    </div>`;
}

function baziCompactLuckHtml(imprint) {
  const luck = typeof luckPillarLens === "function" ? luckPillarLens(imprint) : {};
  const current = luck.current;
  const rawLuck = imprint?.bazi?.luck?.current;
  if (!current && !luck.framework_insight) {
    return `<p class="bazi-compact-empty">Luck pillars unavailable.</p>`;
  }
  if (!current) {
    const note = luck.framework_insight || luck.matrix_insight || "";
    if (note.includes("**Direct Answer**") && typeof formatFlowNarrative === "function") {
      return `<div class="bazi-compact-luck-note matrix-luck-read">${formatFlowNarrative(note)}</div>`;
    }
    return `<p class="bazi-compact-luck-note">${escapeChartText(note)}</p>`;
  }
  const gz = current.gan_zhi || rawLuck?.gan_zhi || "";
  const years =
    current.start_year && current.end_year ? `${current.start_year}–${current.end_year}` : "";
  const identity = current.identity || (typeof pillarSymbolLine === "function" ? pillarSymbolLine(current) : gz);
  const future = (luck.future_preview || []).slice(0, 2);
  const futureHtml = future.length
    ? `<ul class="bazi-compact-luck-future">${future
        .map((fp) => {
          const yrs = fp.start_year && fp.end_year ? `${fp.start_year}–${fp.end_year}` : "";
          const teaser = fp.teaser || fp.identity || "";
          return `<li class="bazi-compact-luck-future-item">
            <span class="bazi-compact-luck-future-head">
              <strong>${escapeChartText(fp.identity || fp.gan_zhi || "")}</strong>
              <span class="hanzi">${escapeChartText(fp.gan_zhi || "")}</span>
              ${yrs ? `<span class="bazi-compact-years">${yrs}</span>` : ""}
              <span class="seeker-teaser-badge" title="Full decade read with Seeker+">Seeker+</span>
            </span>
            ${teaser ? `<span class="seeker-teaser">${escapeChartText(teaser)}</span>` : ""}
          </li>`;
        })
        .join("")}</ul>`
    : "";
  const premiumNote = future.length
    ? `<p class="bazi-luck-premium-note">Upcoming decades <span class="seeker-teaser-badge">Preview</span></p>`
    : "";
  return `
    <div class="bazi-compact-luck-current">
      <span class="bazi-compact-k">Luck pillar</span>
      <div class="bazi-compact-val">
        <strong>${escapeChartText(identity)}</strong>
        <span class="hanzi bazi-compact-hz">${escapeChartText(gz)}</span>
        ${years ? `<span class="bazi-compact-years">${years}</span>` : ""}
      </div>
    </div>
    ${premiumNote}
    ${futureHtml}`;
}

function baziSummaryHtml(imprint) {
  const p = imprint.bazi.pillars;
  const dm = imprint.bazi.day_master;
  const lensOpts = { imprint };
  return `
    <ul class="chart-summary-list chart-summary-list--bazi">
      ${yearZodiacDetailHtml(imprint)}
      ${dayMasterDetailHtml(dm, p.day)}
      ${baziPillarDetailHtml("Year pillar", p.year, { yearStyle: true, ...lensOpts, pillarKey: "year" })}
      ${baziPillarDetailHtml("Month pillar", p.month, { ...lensOpts, pillarKey: "month" })}
      ${baziPillarDetailHtml("Hour pillar", p.hour, { ...lensOpts, pillarKey: "hour" })}
      ${luckPillarDetailHtml(imprint)}
    </ul>`;
}

function vedicSummaryHtml(imprint) {
  const v = imprint.vedic;
  const houses = (v.houses || [])
    .map((h) => {
      const pl = h.planets?.length ? h.planets.join(", ") : "—";
      return `<li><span class="chart-k">${h.house}th</span> <strong>${signGlyph(h.sign)} ${h.sign}</strong> · ${pl}</li>`;
    })
    .join("");
  return `
    <ul class="chart-summary-list">
      <li><span class="chart-k">Lagna</span> <span class="chart-sym-row"><span class="chart-sym chart-sym--sign" aria-hidden="true">${signGlyph(v.lagna.sign)}</span></span> <strong>${v.lagna.sign}</strong> ${v.lagna.degree}°</li>
      <li><span class="chart-k">Moon nakshatra</span> <strong>${v.moon_nakshatra.name}</strong> pada ${v.moon_nakshatra.pada}</li>
      <li><span class="chart-k">Mahadasha</span> <strong>${v.dasha.active_mahadasha.lord}</strong></li>
    </ul>
    <p class="chart-k chart-k--block">All sidereal houses</p>
    <ul class="chart-summary-list chart-summary-list--compact">${houses}</ul>`;
}

function hellenisticSummaryHtml(imprint) {
  const w = imprint.western;
  const asc = w.angles.ascendant.sign;
  const mc = w.angles.midheaven.sign;
  const SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
  ];
  const start = SIGNS.indexOf(asc);
  const houseRows =
    start >= 0
      ? Array.from({ length: 12 }, (_, i) => {
          const n = i + 1;
          const sign = SIGNS[(start + i) % 12];
          const inHouse = Object.entries(w.planets)
            .filter(([, b]) => b.sign === sign)
            .map(([name]) => name);
          return `<li><span class="chart-k">${n}th</span> <strong>${signGlyph(sign)} ${sign}</strong> · ${inHouse.join(", ") || "—"}</li>`;
        }).join("")
      : "";
  const planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"];
  const pl = planets
    .map((n) => {
      const b = w.planets[n];
      return b ? `<li><span class="chart-k">${n}</span> <strong>${signGlyph(b.sign)} ${b.sign}</strong> ${b.degree}°</li>` : "";
    })
    .join("");
  return `
    <ul class="chart-summary-list">
      <li><span class="chart-k">Ascendant</span> <strong>${signGlyph(asc)} ${asc}</strong></li>
      <li><span class="chart-k">Midheaven</span> <strong>${signGlyph(mc)} ${mc}</strong></li>
      ${pl}
    </ul>
    <p class="chart-k chart-k--block">Whole-sign houses</p>
    <ul class="chart-summary-list chart-summary-list--compact">${houseRows}</ul>`;
}

function financialSummaryHtml(imprint) {
  const w = imprint.western.planets;
  return `
    <ul class="chart-summary-list">
      <li><span class="chart-k">Jupiter</span> <strong>${signGlyph(w.Jupiter.sign)} ${w.Jupiter.sign}</strong></li>
      <li><span class="chart-k">Saturn</span> <strong>${signGlyph(w.Saturn.sign)} ${w.Saturn.sign}</strong></li>
      <li><span class="chart-k">Uranus</span> <strong>${signGlyph(w.Uranus.sign)} ${w.Uranus.sign}</strong></li>
      <li><span class="chart-k">Neptune</span> <strong>${signGlyph(w.Neptune.sign)} ${w.Neptune.sign}</strong></li>
      <li><span class="chart-k">Pluto</span> <strong>${signGlyph(w.Pluto.sign)} ${w.Pluto.sign}</strong></li>
    </ul>`;
}

function wealthSummaryHtml(imprint) {
  const wc = imprint.wealth_chart || {};
  const climate = wc.year_climate || {};
  const animal = wc.day_pillar_animal || {};
  const dmLens = wc.day_master || {};
  const profile = wc.day_pillar_profile || {};
  const dm = imprint.bazi?.day_master;
  const sm = dm?.stem ? stemMeta(dm.stem) : {};
  const el = dmLens.element || dm?.element || sm.element || "—";
  const yy = dmLens.yin_yang || dm?.yin_yang || sm.yin_yang || "";
  const dayPillar = imprint.bazi?.pillars?.day;
  const pillarLine = dayPillar ? pillarHiddenRow(dayPillar) : "";
  const pillarId = dayPillar ? pillarIdentityLabel(dayPillar) : animal.animal || "—";
  const climateInsight = wc.element_climate_insight || climate.climate_insight || "";
  const mission = wc.mission_sentence || "";
  const primary = wc.primary_insight || wc.condensed || "";
  const incomeCrown = wc.income_crown_synthesis || "";
  const rootClause = profile.root_clause || "";
  return `
    <ul class="chart-summary-list chart-summary-list--wealth">
      <li><span class="chart-k">Day Master</span> <strong>${yy} ${el}</strong>
        <span class="chart-k">· modality leads seasons</span></li>
      <li><span class="chart-k">Day pillar</span> ${pillarLine} <strong>${pillarId}</strong>
        ${profile.display_line ? `<span class="wealth-summary-note">${profile.display_line}</span>` : ""}</li>
      ${climateInsight ? `<li><span class="chart-k">Sky climate</span> <span class="wealth-summary-note">${climateInsight}</span></li>` : ""}
      ${rootClause ? `<li><span class="chart-k">Branch root</span> <span class="wealth-summary-note">${rootClause}</span></li>` : ""}
      ${incomeCrown ? `<li><span class="chart-k">Income & crown</span> <span class="wealth-summary-note">${incomeCrown}</span></li>` : ""}
      <li><span class="chart-k">Mission</span> <strong>${mission || "—"}</strong></li>
    </ul>
    ${primary ? `<p class="wealth-summary-condensed">${primary}</p>` : ""}`;
}

function relationshipsSummaryHtml(imprint) {
  const h7 = (imprint.vedic?.houses || []).find((h) => h.house === 7);
  const h10 = (imprint.vedic?.houses || []).find((h) => h.house === 10);
  const v = imprint.vedic;
  const soul = imprint.numerology?.schools?.pythagorean?.soul_urge;
  const dayAn = imprint.bazi?.pillars?.day ? branchAnimal(imprint.bazi.pillars.day.branch) : "—";
  const yz = yearZodiacFromImprint(imprint);
  return `
    <ul class="chart-summary-list">
      <li><span class="chart-k">7th house</span> <strong>${signGlyph(h7?.sign)} ${h7?.sign || "—"}</strong></li>
      <li><span class="chart-k">10th house</span> <strong>${signGlyph(h10?.sign)} ${h10?.sign || "—"}</strong></li>
      <li><span class="chart-k">Moon nakshatra</span> <strong>${v?.moon_nakshatra?.name || "—"}</strong></li>
      <li><span class="chart-k">Soul urge</span> <strong>${soul ? numerologyDisplay(soul) : "—"}</strong></li>
      <li><span class="chart-k">Year zodiac</span> <strong>${yz.label || yz.animal || "—"}</strong></li>
      <li><span class="chart-k">Day pillar</span> ${imprint.bazi?.pillars?.day ? pillarHiddenRow(imprint.bazi.pillars.day) : ""} <strong>${imprint.bazi?.pillars?.day ? pillarIdentityLabel(imprint.bazi.pillars.day) : dayAn}</strong> · ${imprint.bazi?.pillars?.day ? pillarDisplayLine(imprint.bazi.pillars.day) : ""}</li>
    </ul>`;
}

function summaryForSystem(system, imprint) {
  const map = {
    numerology: numerologySummaryHtml,
    bazi: baziSummaryHtml,
    vedic: vedicSummaryHtml,
    hellenistic: hellenisticSummaryHtml,
    financial: financialSummaryHtml,
    wealth: wealthSummaryHtml,
    relationships: relationshipsSummaryHtml,
  };
  return map[system] ? map[system](imprint) : "";
}

function sealNumerologyLabels(imprint) {
  const cached = imprint?.numerology_seal_labels;
  if (cached) return cached;
  const py = imprint?.numerology?.schools?.pythagorean || {};
  const aka = imprint?.numerology?.commonly_known_as || {};
  const bornExpr = py.expression;
  const akaExpr = aka.expression;
  return {
    life_path_display: lifePathDisplay(imprint),
    compound_title: "—",
    final_title: "—",
    final_value: null,
    seal_insight: "—",
    soul_contract_title: "—",
    born_expression: {
      display: bornExpr ? numerologyDisplay(bornExpr) : "—",
      title: "—",
    },
    daily_walk: akaExpr
      ? { display: numerologyDisplay(akaExpr), title: "—" }
      : null,
  };
}

function renderSealNumerologyFrame(imprint) {
  const host = document.getElementById("seal-numerology-body");
  if (!host || !imprint) return;
  const labels = sealNumerologyLabels(imprint);
  const lp = labels.life_path_display || lifePathDisplay(imprint);
  const compoundName = labels.compound_title || "—";
  const finalVal = labels.final_value ?? imprint.numerology?.schools?.pythagorean?.life_path?.value;
  const insight = labels.seal_insight || "—";
  host.innerHTML = `
    <button type="button" class="seal-numerology-open" id="seal-numerology-open" aria-haspopup="dialog">
      <span class="seal-panel-label">Occult Numerology</span>
      <div class="seal-numerology-compact">
        <p class="seal-numerology-lp"><span class="seal-numerology-lp-label">Life path</span> <strong>${escapeChartText(lp)}</strong></p>
        <p class="seal-numerology-compound-name">${escapeChartText(compoundName)}</p>
        <p class="seal-numerology-insight">${escapeChartText(insight)}</p>
        ${
          finalVal != null
            ? `<p class="seal-numerology-final-dir">Final <strong>${escapeChartText(String(finalVal))}</strong> — ultimate direction</p>`
            : ""
        }
      </div>
      <span class="chart-box-hint">Open full read →</span>
    </button>`;
}

function renderSealLayerTitles(imprint) {
  const wealthBtn = document.getElementById("seal-wealth-layer");
  const relBtn = document.getElementById("seal-relationships-layer");
  const karmaBtn = document.getElementById("seal-karma-layer");
  if (wealthBtn && imprint) {
    wealthBtn.title = imprint.wealth_chart?.mission_sentence || "Wealth daily counsel — Seeker+";
  }
  if (relBtn && imprint) {
    relBtn.title = relationshipsExteriorLine(imprint);
  }
  if (karmaBtn) {
    const pack = typeof window !== "undefined" ? window.occultDailySaturn : null;
    karmaBtn.title =
      pack?.saturnTabLabel || pack?.saturn?.tab_label || "Open your karmic debt insight";
  }
}

function renderSealLifeTokens(imprint) {
  if (!imprint) return;
  renderSealLayerTitles(imprint);
}

function renderTraditionTokens(imprint) {
  const host = document.getElementById("seal-tradition-tokens");
  if (!host || !imprint) return;
  host.innerHTML = CHART_SELECTABLE.map(
    (s) =>
      `<button type="button" class="layer-token layer-token--square seal-token seal-token--tradition" data-tradition-token="${s.id}" title="${escapeChartText(s.blurb)}"><span class="layer-token-name">${TRADITION_TOKEN_LABELS[s.id] || s.label}</span></button>`
  ).join("");
}

function renderSealStack(imprint) {
  if (!imprint) return;
  renderSealNumerologyFrame(imprint);
  renderSealLifeTokens(imprint);
  renderSealLayerTitles(imprint);
  renderTraditionTokens(imprint);
  renderSealRelationships(imprint);
  renderWealthFrame(imprint);
}

function relationshipsExteriorLine(imprint) {
  const framing = imprint?.relationships_framing || {};
  if (framing.exterior_line) return framing.exterior_line;
  const signs = framing.signs_to_avoid || [];
  if (signs.length) return `Signs to lean away from: ${signs.join(", ")}.`;
  return "Tap to open your relationship read — fairness before romance deepens.";
}

function closeRelationshipsFrameTab() {
  const tab = document.getElementById("relationships-frame-tab");
  if (tab) {
    tab.classList.add("hidden");
    tab.hidden = true;
  }
}

async function openRelationshipsFrameTab() {
  const base = document.getElementById("relationships-frame-base");
  const tab = document.getElementById("relationships-frame-tab");
  const body = document.getElementById("relationships-frame-body");
  const openBtn = document.getElementById("relationships-frame-open");
  if (!tab || !body) return;
  base?.classList.add("hidden");
  tab.classList.remove("hidden");
  tab.hidden = false;
  if (openBtn) openBtn.setAttribute("aria-expanded", "true");
  body.innerHTML = `<p class="status">Loading relationship insight…</p>`;

  const fetchFn = typeof window.apiFetch === "function" ? window.apiFetch : null;
  try {
    const data = await fetchChartReading("relationships", fetchFn);
    const verifiedNote =
      data.verified && data.reading_engine
        ? `<p class="chart-modal-note chart-modal-note--verified">Self-checked against your sealed chart (${escapeChartText(data.reading_engine)}).</p>`
        : "";
    // Frame the relationship insight like the expanded Karmic Debt: direct, full, common English, with numerology overlay intact, actionable.
    const coreNarrative = formatFlowNarrative(data.narrative);
    const richRelationships = `
      <div class="karmic-debt-read relationships-rich">
        <p class="karmic-intro"><strong>Your relationship imprint:</strong> This token shows how your birth chart and numerology shape bonds, legacy, and mirrored growth. The numerology overlay reveals the life-path rhythm that colors every partnership and collaboration.</p>
        ${coreNarrative}
        <div class="karmic-allegory">
          <h5>How it plays out</h5>
          <p>Relationships act as the clearest mirror for your karmic and numerological lessons. Patterns repeat with partners, family, or collaborators until the exact dynamic (from your pillars and numbers) is integrated. It feels fated because the chart pulls the right people to teach the lesson.</p>
          <p>Simple allegory: Like two rivers meeting — your numerology is the current, the chart is the riverbed. When they clash, the banks erode until a new, stronger channel forms. Dodge the lesson and the same flood keeps returning; meet it and the relationship (or your capacity for it) becomes a source of power and legacy.</p>
        </div>
        <div class="karmic-actions">
          <h5>Actionable steps</h5>
          <p>Look at the core narrative above for your specific read. Pick one phrase that lands and ask: "Where is this showing up with one key person right now?" Name the pattern out loud or in writing. Then take the smallest action the narrative suggests (a boundary, a conversation, a release). Do it today. The overlay with your life path number shows the long game — this bond is shaping the person you become.</p>
        </div>
      </div>
    `;
    body.innerHTML = `${verifiedNote}${richRelationships}`;
  } catch (err) {
    const msg = err.message || "Could not load relationship insight.";
    if (msg.toLowerCase().includes("sign in") || msg.toLowerCase().includes("sealed chart")) {
      body.innerHTML = `<p class="status error">Sign in to load live relationship insight for a sealed chart. Core results available in the birth preview for testing.</p>`;
      return;
    }
    body.innerHTML = `<p class="status error">${escapeChartText(msg)}</p>`;
  }
}

function bindRelationshipsFrame() {
  initChartForgeUI();
}

function renderSealRelationships(imprint) {
  const lineEl = document.getElementById("relationships-exterior-line");
  if (lineEl && imprint) lineEl.textContent = relationshipsExteriorLine(imprint);
  closeRelationshipsFrameTab();
  initChartForgeUI();
}

function chartBoxHtml(system, imprint) {
  const meta = ALL_CHART_BOXES.find((s) => s.id === system);
  if (!meta) return "";
  const selected = selectedChartSystem === system ? " chart-box--selected" : "";
  const tone =
    system === "wealth"
      ? " chart-box--wealth"
      : system === "relationships"
        ? " chart-box--relationships"
        : "";
  return `
    <button type="button" class="chart-box${selected}${tone}" data-chart-system="${system}" aria-pressed="${selectedChartSystem === system}">
      <h4>${meta.label}</h4>
      ${summaryForSystem(system, imprint)}
      <span class="chart-box-hint">Open episode read →</span>
    </button>`;
}

function renderChartBoxes(imprint) {
  const stack = document.getElementById("chart-boxes");
  if (!stack || !imprint) return;

  stack.innerHTML = CHART_SELECTABLE.map((s) => chartBoxHtml(s.id, imprint)).join("");

  stack.querySelectorAll("[data-chart-system]").forEach((btn) => {
    btn.addEventListener("click", () => openChartDeepRead(btn.dataset.chartSystem));
  });
}

function bindChartModal() {
  const modal = document.getElementById("chart-modal");
  if (!modal || modal.dataset.bound) return;
  modal.dataset.bound = "1";

  const close = () => closeChartModal();
  document.getElementById("chart-modal-close")?.addEventListener("click", close);
  modal.querySelectorAll("[data-close-modal]").forEach((el) => el.addEventListener("click", close));
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const insight = document.getElementById("bazi-insight-modal");
    if (insight && !insight.classList.contains("hidden")) {
      closeBaziInsightModal();
      return;
    }
    if (!modal.classList.contains("hidden")) close();
  });
}

function openChartModal(title, bodyHtml) {
  if (typeof window !== "undefined") window.openChartModal = openChartModal;
  bindChartModal();
  const modal = document.getElementById("chart-modal");
  const titleEl = document.getElementById("chart-modal-title");
  const bodyEl = document.getElementById("chart-modal-body");
  if (!modal || !titleEl || !bodyEl) return;
  titleEl.textContent = title;
  bodyEl.innerHTML = bodyHtml;
  modal.classList.remove("hidden");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("chart-modal-open");
}

function closeChartModal() {
  closeBaziInsightModal();
  const modal = document.getElementById("chart-modal");
  if (!modal) return;
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("chart-modal-open");
  selectedChartSystem = null;
  if (window.occultImprint && typeof renderTraditionTokens === "function") {
    renderTraditionTokens(window.occultImprint);
  }
}

async function fetchChartReading(system, apiFetch) {
  if (chartReadingCache[system]) return chartReadingCache[system];
  const preloaded =
    typeof window !== "undefined" && window.occultChartReadings
      ? window.occultChartReadings[system]
      : null;
  const needsPanels = system === "numerology" && !preloaded?.panels;
  if (preloaded?.narrative && !needsPanels) {
    chartReadingCache[system] = preloaded;
    return preloaded;
  }
  // Preview / unauthenticated mode: use only the data that came back from the initial public /imprint/preview
  // (which already includes full chart_readings for all systems). Never hit the auth-only /me endpoint.
  if (!apiFetch || typeof apiFetch !== "function") {
    if (preloaded) {
      chartReadingCache[system] = preloaded;
      return preloaded;
    }
    throw new Error("Sign in to load your sealed chart.");
  }
  const res = await apiFetch(`/imprint/chart-reading/me?system=${encodeURIComponent(system)}`);
  let data = {};
  try {
    data = await res.json();
  } catch {
    data = { detail: res.statusText || "Invalid response" };
  }
  if (!res.ok) {
    const detail = data.detail;
    const msg =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg || d.message || String(d)).join("; ")
          : res.statusText || "Request failed";
    throw new Error(msg);
  }
  chartReadingCache[system] = data;
  return data;
}

function chartSummaryBlock(system, imprint) {
  if (!imprint || !summaryForSystem(system, imprint)) return "";
  return `<div class="chart-modal-chart">${summaryForSystem(system, imprint)}</div>`;
}

function openKarmicDebtToken() {
  const pack = typeof window !== "undefined" ? window.occultDailySaturn : null;
  const title = pack?.saturnModalTitle || "Your karmic debt insight";
  const formatBody =
    typeof formatKarmicDebtModalBody === "function"
      ? formatKarmicDebtModalBody
      : typeof window.formatKarmicDebtModalBody === "function"
        ? window.formatKarmicDebtModalBody
        : null;
  if (!pack?.saturn || !formatBody) {
    openChartModal(
      title,
      `<p class="status">Refresh daily expression to load Saturn karmic debt insight.</p>`
    );
    return;
  }
  openChartModal(title, formatBody(pack.saturn));
}

function compoundReadForField(imprint, field) {
  const labels = imprint?.numerology_seal_labels || {};
  const key = `${field}_compound_read`;
  if (labels[key]?.body) return labels[key];
  if (field === "life_path" && labels.life_path_compound_read?.body) {
    return labels.life_path_compound_read;
  }
  return null;
}

function formatCompoundFrameworkModal(read) {
  if (!read?.body) {
    return `<p class="status">Compound framework read not available for this field.</p>`;
  }
  const title = read.glyph || read.display || "Compound";
  const placement = read.placement
    ? `<p class="chart-modal-note">${escapeChartText(read.placement)} — general chart framework, not a personal verdict.</p>`
    : `<p class="chart-modal-note">General compound framework — not applied to you as a personal verdict.</p>`;
  const body =
    typeof formatFlowNarrative === "function"
      ? formatFlowNarrative(read.body)
      : `<p>${escapeChartText(read.body)}</p>`;
  return `${placement}${body}`;
}

function westernSettingListItems(text) {
  return (text || "")
    .split(/\n+/)
    .map((line) => line.replace(/^\s*[-•]\s*/, "").replace(/^\d+\.\s*/, "").trim())
    .filter(Boolean);
}

function formatWesternSettingSectionBody(label, body) {
  const raw = (body || "").trim();
  if (!raw) return "";

  if (label === "Direct Answer") {
    const paras = raw.split(/\n\n+/).map((p) => p.replace(/\n/g, " ").trim()).filter(Boolean);
    return paras
      .map((p) => `<p class="flow-para western-setting-prose">${escapeChartText(p)}</p>`)
      .join("");
  }

  if (label === "Decoded Insight") {
    const items = westernSettingListItems(raw);
    if (!items.length) return `<p class="flow-para">${escapeChartText(raw)}</p>`;
    return `<ul class="western-setting-list western-setting-list--pulse">${items
      .map((item) => `<li class="western-setting-list-item">${escapeChartText(item)}</li>`)
      .join("")}</ul>`;
  }

  if (label === "Action") {
    const forgeMatch = raw.match(/(?:Actionable Blades|Forge now|Do this now):\s*([\s\S]*?)(?:\n\nWatch out:|$)/i);
    const watchMatch = raw.match(
      /Watch out:\s*([\s\S]*?)(?:\n\n(?:Daily Matrix|Matrix decoded|Take the blade|walk this path)|$)/i
    );
    const tailMatch = raw.match(
      /(?:Daily Matrix read[\s\S]*|Matrix decoded\.?|Take the blade\. Become Zero\.?|walk this path\.?)\s*$/i
    );
    const forgeItems = westernSettingListItems(forgeMatch ? forgeMatch[1] : raw);
    const watchItems = westernSettingListItems(watchMatch ? watchMatch[1] : "");
    const forgeHead = /(?:Do this now|Actionable Blades):/i.test(raw) ? "" : "Forge now";
    let html = "";
    if (forgeItems.length) {
      html += `${forgeHead ? `<p class="western-setting-subhead">${forgeHead}</p>` : ""}<ol class="western-setting-list western-setting-list--forge">${forgeItems
        .map((item) => `<li class="western-setting-list-item">${escapeChartText(item)}</li>`)
        .join("")}</ol>`;
    }
    if (watchItems.length) {
      html += `<p class="western-setting-subhead western-setting-subhead--watch">Watch out</p><ul class="western-setting-list western-setting-list--watch">${watchItems
        .map((item) => `<li class="western-setting-list-item">${escapeChartText(item)}</li>`)
        .join("")}</ul>`;
    }
    if (tailMatch) {
      html += `<p class="flow-para zero-insight-close">${escapeChartText(tailMatch[0].trim())}</p>`;
    }
    if (!html) return `<p class="flow-para">${escapeChartText(raw)}</p>`;
    return html;
  }

  return formatMatrixBody(raw);
}

function formatForgeLensNarrative(text, { labels, flowClass, sectionClass }) {
  const raw = (text || "").trim();
  if (!raw) return "";
  let rest = raw;
  const blocks = [];
  for (const [label, cls, displayLabel] of labels) {
    const marker = `**${label}**`;
    const idx = rest.indexOf(marker);
    if (idx === -1) continue;
    const after = rest.slice(idx + marker.length).trim();
    const nextIdx = labels
      .map(([l]) => after.indexOf(`**${l}**`))
      .filter((i) => i >= 0)
      .sort((a, b) => a - b)[0];
    const body = (nextIdx != null && nextIdx >= 0 ? after.slice(0, nextIdx) : after).trim();
    blocks.push(
      `<section class="matrix-section ${cls} ${sectionClass}"><h5 class="matrix-section-label">${displayLabel}</h5><div class="matrix-section-body">${formatWesternSettingSectionBody(label, body)}</div></section>`
    );
    rest = nextIdx != null && nextIdx >= 0 ? after.slice(nextIdx) : "";
  }
  if (!blocks.length) return formatFlowNarrative(raw);
  return `<div class="flow-read flow-read--matrix ${flowClass}">${blocks.join("")}</div>`;
}

function formatHellenisticNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "How you move"],
      ["Decoded Insight", "matrix-section--decoded", "Life weather"],
      ["Action", "matrix-section--action", "Forge now"],
    ],
    flowClass: "flow-read--hellenistic",
    sectionClass: "hellenistic-section",
  });
}

function formatFinancialNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "Money weather"],
      ["Decoded Insight", "matrix-section--decoded", "Ledger pulse"],
      ["Action", "matrix-section--action", "Forge now"],
    ],
    flowClass: "flow-read--financial",
    sectionClass: "financial-section",
  });
}

function formatZeroInsightNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "Direct Mirror"],
      ["Decoded Insight", "matrix-section--decoded", "Decoded Layers"],
      ["Action", "matrix-section--action", "Actionable Blades"],
    ],
    flowClass: "flow-read--zero-insight",
    sectionClass: "zero-insight-section",
  });
}

function formatBaziPillarsNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "Your pillars"],
      ["Decoded Insight", "matrix-section--decoded", "How they move"],
      ["Action", "matrix-section--action", "Forge now"],
    ],
    flowClass: "flow-read--bazi-pillars",
    sectionClass: "bazi-pillars-section",
  });
}

function formatAncientsWisdomNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "The truth"],
      ["Decoded Insight", "matrix-section--decoded", "Forbidden frames"],
      ["Action", "matrix-section--action", "Forge now"],
    ],
    flowClass: "flow-read--ancients-wisdom",
    sectionClass: "ancients-wisdom-section",
  });
}

async function fetchAncientsWisdom(fetchFn) {
  const res = await fetchFn("/imprint/ancients-wisdom/me");
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || "Could not load Ancient's Wisdom.");
  }
  return data;
}

async function openAncientsWisdomModal() {
  const title = "Ancient's Wisdom";
  const modal = document.getElementById("chart-modal");
  const bodyEl = document.getElementById("chart-modal-body");
  const titleEl = document.getElementById("chart-modal-title");
  if (!modal || !titleEl || !bodyEl) return;
  titleEl.textContent = title;
  bodyEl.innerHTML = `<p class="status">Opening the gate…</p>`;
  modal.classList.remove("hidden");
  const fetchFn = typeof window.apiFetch === "function" ? window.apiFetch : null;
  if (!fetchFn) {
    // Preview mode: show the structured narrative so the token returns content (matching other preview tokens).
    // Full sealed version + premium transmission after chart is sealed.
    const note = `<p class="chart-modal-note">Zero's deepest layer — Ethiopian canon and Gnostic exit codes. No chart callouts; truth to power.</p>`;
    const demoNarrative = "Preview transmission active. The ancient layers mirror your sealed imprint. Ethiopian canon and Gnostic frames surface the exit codes hidden in plain sight.\n\nThe core aligns with your zero matrix and daily sky friction. Hidden power structures become visible.\n\nApply one frame today: observe without reaction and note the pattern that repeats across your pillars.";
    const body = typeof formatAncientsWisdomNarrative === "function"
      ? formatAncientsWisdomNarrative(demoNarrative)
      : demoNarrative;
    const lock = `<p class="ancients-wisdom-premium-lock"><strong>Seeker+</strong> — Full transmission after you seal your chart. (Rituals and advanced Zero features coming; this preview shows the structure.)</p>`;
    bodyEl.innerHTML = `${note}${body}${lock}`;
    return;
  }
  try {
    const data = await fetchAncientsWisdom(fetchFn);
    const body =
      typeof formatAncientsWisdomNarrative === "function"
        ? formatAncientsWisdomNarrative(data.narrative)
        : data.narrative;
    const note = `<p class="chart-modal-note">Zero's deepest layer — Ethiopian canon and Gnostic exit codes. No chart callouts; truth to power.</p>`;
    const lock = data.premium_locked
      ? `<p class="ancients-wisdom-premium-lock"><strong>Seeker+</strong> — ${escapeChartText(data.premium_teaser || "Premium unlocks the full transmission.")}</p>`
      : "";
    bodyEl.innerHTML = `${note}${body}${lock}`;
  } catch (err) {
    bodyEl.innerHTML = `<p class="status error">${escapeChartText(err.message || "Could not load Ancient's Wisdom.")}</p>`;
  }
}

function formatVedicForgeNarrative(text) {
  return formatForgeLensNarrative(text, {
    labels: [
      ["Direct Answer", "matrix-section--direct", "Body truth"],
      ["Decoded Insight", "matrix-section--decoded", "Where it lives"],
      ["Action", "matrix-section--action", "Forge now"],
    ],
    flowClass: "flow-read--vedic-forge",
    sectionClass: "vedic-forge-section",
  });
}



function openCompoundFrameworkModal(field) {
  const imprint = typeof window !== "undefined" ? window.occultImprint : null;
  const read = imprint ? compoundReadForField(imprint, field) : null;
  const title = read?.glyph ? `${read.glyph} · compound` : "Compound framework";
  const open =
    typeof openChartModal === "function"
      ? openChartModal
      : typeof window.openChartModal === "function"
        ? window.openChartModal
        : null;
  if (!open) return;
  open(title, formatCompoundFrameworkModal(read));
}

async function openChartDeepRead(system, options = {}) {
  const showChart =
    options.showChart ??
    (CHART_SELECTABLE.some((s) => s.id === system) ||
      system === "wealth" ||
      system === "relationships");
  selectedChartSystem = system;
  if (window.occultImprint) renderTraditionTokens(window.occultImprint);

  const meta = ALL_CHART_BOXES.find((s) => s.id === system);
  const title = meta?.label || system;

  // For preview mode (and sealed), prefer any preloaded data from the initial birth preview response.
  // This lets unauthenticated users see the full tab results without signing in.
  const cached = (typeof chartReadingCache !== "undefined" ? chartReadingCache[system] : null) ||
                 (typeof window !== "undefined" && window.occultChartReadings ? window.occultChartReadings[system] : null);
  if (cached) {
    openChartModal(title, `<p class="status">Forging episode read…</p>`);
    const data = cached;
    const verifiedNote =
      data.verified && data.reading_engine
        ? `<p class="chart-modal-note chart-modal-note--verified">Self-checked against your sealed chart (${data.reading_engine}).</p>`
        : "";
    const chartBlock =
      showChart && window.occultImprint ? chartSummaryBlock(system, window.occultImprint) : "";
    let body =
      system === "numerology" && data.panels
        ? formatNumerologyPanels(data.panels)
        : formatFlowNarrative(data.narrative);
    if (system === "vedic" && typeof formatVedicForgeNarrative === "function") {
      body = formatVedicForgeNarrative(data.narrative);
    } else if (system === "hellenistic" && typeof formatHellenisticNarrative === "function") {
      body = formatHellenisticNarrative(data.narrative);
    } else if (system === "financial" && typeof formatFinancialNarrative === "function") {
      body = formatFinancialNarrative(data.narrative);
    }
    const note =
      system === "vedic"
        ? `<p class="chart-modal-note">Pure Vedic / Jyotish — sidereal body, mood, and chapter. No Western overlay.</p>`
        : `<p class="chart-modal-note">Sealed insight from your chart — one read for this block.</p>`;
    openChartModal(data.title || title, `${verifiedNote}${chartBlock}${note}${body}`);
    return;
  }

  openChartModal(title, `<p class="status">Forging episode read…</p>`);

  const fetchFn = typeof window.apiFetch === "function" ? window.apiFetch : null;
  try {
    const data = await fetchChartReading(system, fetchFn);
    const verifiedNote =
      data.verified && data.reading_engine
        ? `<p class="chart-modal-note chart-modal-note--verified">Self-checked against your sealed chart (${data.reading_engine}).</p>`
        : "";
    const chartBlock =
      showChart && window.occultImprint ? chartSummaryBlock(system, window.occultImprint) : "";
    let body =
      system === "numerology" && data.panels
        ? formatNumerologyPanels(data.panels)
        : formatFlowNarrative(data.narrative);
    if (system === "vedic" && typeof formatVedicForgeNarrative === "function") {
      body = formatVedicForgeNarrative(data.narrative);
    } else if (system === "hellenistic" && typeof formatHellenisticNarrative === "function") {
      body = formatHellenisticNarrative(data.narrative);
    } else if (system === "financial" && typeof formatFinancialNarrative === "function") {
      body = formatFinancialNarrative(data.narrative);
    }
    const note =
      system === "vedic"
        ? `<p class="chart-modal-note">Pure Vedic / Jyotish — sidereal body, mood, and chapter. No Western overlay.</p>`
        : `<p class="chart-modal-note">Sealed insight from your chart — one read for this block.</p>`;
    openChartModal(data.title || title, `${verifiedNote}${chartBlock}${note}${body}`);
  } catch (err) {
    const msg = err.message || "Could not load reading.";
    if (
      msg.includes("Session expired") ||
      msg.includes("User not found") ||
      msg.includes("sign in again")
    ) {
      if (typeof handleSessionExpired === "function") handleSessionExpired(msg);
      return;
    }
    if (msg.toLowerCase().includes("sign in") || msg.toLowerCase().includes("sealed chart")) {
      openChartModal(title, `<p class="status error">Sign in to load live/personalized reads for a sealed chart. The birth preview above contains the core results for testing.</p>`);
      return;
    }
    openChartModal(title, `<p class="status error">${escapeChartText(msg)}</p>`);
  }
}

function canAccessZeroWealthInsight() {
  return true;
}

function closeWealthFrameTabs() {
  const base = document.getElementById("wealth-frame-base");
  const chartTab = document.getElementById("wealth-frame-chart");
  const zeroTab = document.getElementById("wealth-frame-zero");
  base?.classList.remove("hidden");
  if (chartTab) {
    chartTab.classList.add("hidden");
    chartTab.hidden = true;
  }
  if (zeroTab) {
    zeroTab.classList.add("hidden");
    zeroTab.hidden = true;
  }
}

function pulseWealthFrame() {
  const frame = document.getElementById("wealth-frame");
  if (!frame) return;
  frame.classList.remove("wealth-frame--pulse");
  void frame.offsetWidth;
  frame.classList.add("wealth-frame--pulse");
  frame.scrollIntoView({ behavior: "smooth", block: "start" });
}

function openWealthChartTab() {
  const base = document.getElementById("wealth-frame-base");
  const chartTab = document.getElementById("wealth-frame-chart");
  const zeroTab = document.getElementById("wealth-frame-zero");
  if (!chartTab) return;
  base?.classList.add("hidden");
  zeroTab?.classList.add("hidden");
  if (zeroTab) zeroTab.hidden = true;
  chartTab.classList.remove("hidden");
  chartTab.hidden = false;
  pulseWealthFrame();
}

function openWealthHub() {
  openWealthChartTab();
}

async function openZeroWealthInsight() {
  if (!canAccessZeroWealthInsight()) {
    openChartModal(
      "Zero Insight",
      `<p class="wealth-paywall-teaser">Zero Insight is a premium unified wealth read. Subscribe to unlock the full episode.</p>`
    );
    return;
  }
  const base = document.getElementById("wealth-frame-base");
  const chartTab = document.getElementById("wealth-frame-chart");
  const zeroTab = document.getElementById("wealth-frame-zero");
  const body = document.getElementById("wealth-frame-zero-body");
  if (!zeroTab || !body) {
    openChartDeepRead("wealth");
    return;
  }
  base?.classList.add("hidden");
  chartTab?.classList.add("hidden");
  if (chartTab) chartTab.hidden = true;
  zeroTab.classList.remove("hidden");
  zeroTab.hidden = false;
  body.innerHTML = `<p class="status">Forging Zero Insight…</p>`;
  pulseWealthFrame();

  const fetchFn = typeof window.apiFetch === "function" ? window.apiFetch : null;
  try {
    const data = await fetchChartReading("wealth", fetchFn);
    const verifiedNote =
      data.verified && data.reading_engine
        ? `<p class="chart-modal-note chart-modal-note--verified">Self-checked against your sealed chart (${escapeChartText(data.reading_engine)}).</p>`
        : "";
    body.innerHTML = `${verifiedNote}${formatFlowNarrative(data.narrative)}`;
  } catch (err) {
    const msg = err.message || "Could not load Zero Insight.";
    if (msg.toLowerCase().includes("sign in") || msg.toLowerCase().includes("sealed chart")) {
      body.innerHTML = `<p class="status error">Sign in to load live Zero Insight for a sealed chart. The birth preview contains core chart results for the main tokens.</p>`;
      return;
    }
    body.innerHTML = `<p class="status error">${escapeChartText(msg)}</p>`;
  }
}

function bindBaziInsightModal() {
  const modal = document.getElementById("bazi-insight-modal");
  if (!modal || modal.dataset.bound) return;
  modal.dataset.bound = "1";
  const close = () => closeBaziInsightModal();
  document.getElementById("bazi-insight-close")?.addEventListener("click", close);
  document.getElementById("bazi-insight-back")?.addEventListener("click", close);
  modal.querySelectorAll("[data-close-bazi-insight]").forEach((el) => el.addEventListener("click", close));
}

function openBaziInsightModal() {
  bindBaziInsightModal();
  const modal = document.getElementById("bazi-insight-modal");
  const body = document.getElementById("bazi-insight-body");
  if (!modal || !body) return;
  modal.classList.remove("hidden");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("bazi-insight-modal-open");
  body.innerHTML = `<p class="status">Forging full BaZi insight…</p>`;
}

function closeBaziInsightModal() {
  const modal = document.getElementById("bazi-insight-modal");
  if (!modal) return;
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("bazi-insight-modal-open");
}

function expandBaziFullChart() {
  const panel = document.getElementById("bazi-modal-chart-panel");
  const btn = document.getElementById("bazi-modal-expand-chart");
  if (!panel) return;
  const opening = panel.classList.contains("hidden") || panel.classList.contains("bazi-modal-chart--collapsed");
  panel.classList.toggle("hidden", !opening);
  panel.classList.toggle("bazi-modal-chart--collapsed", !opening);
  panel.classList.toggle("bazi-modal-chart--expanded", opening);
  panel.setAttribute("aria-hidden", opening ? "false" : "true");
  if (btn) {
    btn.textContent = opening ? "Collapse chart" : "Expand full chart";
    btn.setAttribute("aria-expanded", opening ? "true" : "false");
  }
  if (opening) panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function hydrateBaziModalInsight(imprint) {
  const insightHost = document.getElementById("bazi-modal-insight-body");
  const synopsisHost = document.getElementById("bazi-modal-synopsis-text");
  const fetchFn = typeof window.apiFetch === "function" ? window.apiFetch : null;
  if (!insightHost) return;
  insightHost.innerHTML = `<p class="status">Forging full BaZi insight…</p>`;
  try {
    const data = await fetchChartReading("bazi", fetchFn);
    if (synopsisHost && imprint) {
      synopsisHost.innerHTML = baziSynopsisHtml(imprint, data.narrative);
    }
    insightHost.innerHTML =
      typeof formatBaziPillarsNarrative === "function"
        ? formatBaziPillarsNarrative(data.narrative)
        : formatFlowNarrative(data.narrative);
  } catch (err) {
    const msg = err.message || "Could not load BaZi insight.";
    if (
      msg.includes("Session expired") ||
      msg.includes("User not found") ||
      msg.includes("sign in again")
    ) {
      if (typeof handleSessionExpired === "function") handleSessionExpired(msg);
      closeChartModal();
      return;
    }
    if (msg.toLowerCase().includes("sign in") || msg.toLowerCase().includes("sealed chart")) {
      insightHost.innerHTML = `<p class="status error">Sign in to load live BaZi insight for a sealed chart. The birth preview contains core results.</p>`;
      return;
    }
    insightHost.innerHTML = `<p class="status error">${escapeChartText(msg)}</p>`;
  }
}

async function openBaziFullInsightTab() {
  expandBaziFullChart();
}

function openBaziChartModal() {
  const imprint = typeof window !== "undefined" ? window.occultImprint : null;
  if (!imprint?.bazi) return;
  const title = BAZI_BOX.label;
  openChartModal(
    title,
    `<div class="bazi-modal-layout">
      <section class="bazi-modal-synopsis" aria-label="BaZi synopsis">
        <h4 class="bazi-modal-synopsis-label">Synopsis</h4>
        <div id="bazi-modal-synopsis-text" class="bazi-modal-synopsis-text">${baziSynopsisHtml(imprint)}</div>
      </section>
      <section class="bazi-modal-insight-block" aria-label="BaZi full chart insight">
        <h4 class="bazi-modal-insight-label">Full chart insight</h4>
        <div id="bazi-modal-insight-body" class="bazi-modal-insight-body"><p class="status">Forging full BaZi insight…</p></div>
      </section>
      <div class="bazi-modal-expand-row">
        <button
          type="button"
          class="bazi-modal-insight-token bazi-modal-expand-token"
          id="bazi-modal-expand-chart"
          aria-expanded="false"
          aria-controls="bazi-modal-chart-panel"
          aria-label="Expand full BaZi chart with pillar and hidden stem detail"
        >Expand full chart</button>
      </div>
      <div
        id="bazi-modal-chart-panel"
        class="bazi-modal-chart chart-modal-chart bazi-modal-chart--collapsed hidden"
        aria-hidden="true"
      >${baziSummaryHtml(imprint)}</div>
    </div>`
  );
  hydrateBaziModalInsight(imprint);
}

function bindBaziFrame() {
  initChartForgeUI();
}

function renderBaziFrame(imprint) {
  initChartForgeUI();
  const pillarsHost = document.getElementById("bazi-compact-pillars");
  const luckHost = document.getElementById("bazi-compact-luck");
  if (!imprint || !pillarsHost) return;
  try {
    const p = imprint.bazi?.pillars || {};
    pillarsHost.innerHTML = [
      baziCompactPillarRow("Year", p.year, imprint, "year", { yearStyle: true }),
      baziCompactPillarRow("Day", p.day, imprint, "day"),
      baziCompactPillarRow("Month", p.month, imprint, "month"),
      baziCompactPillarRow("Hour", p.hour, imprint, "hour"),
    ].join("");
    if (luckHost) luckHost.innerHTML = baziCompactLuckHtml(imprint);
  } catch (err) {
    console.error("renderBaziFrame", err);
    pillarsHost.innerHTML = `<p class="bazi-compact-empty">BaZi summary unavailable.</p>`;
  }
}

function bindWealthFrame() {
  const frame = document.getElementById("wealth-frame");
  if (!frame || frame.dataset.bound) return;
  frame.dataset.bound = "1";
  document.getElementById("wealth-frame-open-chart")?.addEventListener("click", openWealthChartTab);
  document.getElementById("wealth-frame-open-zero")?.addEventListener("click", openZeroWealthInsight);
  document.getElementById("wealth-frame-close-chart")?.addEventListener("click", closeWealthFrameTabs);
  document.getElementById("wealth-frame-close-zero")?.addEventListener("click", closeWealthFrameTabs);
}

function renderWealthFrame(imprint) {
  const panel = document.getElementById("wealth-hub-panel-chart");
  const missionEl = document.getElementById("wealth-frame-mission");
  if (!imprint) return;
  if (panel) panel.innerHTML = wealthSummaryHtml(imprint);
  const mission = imprint.wealth_chart?.mission_sentence || "";
  if (missionEl) {
    missionEl.textContent = mission;
    missionEl.classList.toggle("hidden", !mission);
  }
  closeWealthFrameTabs();
  bindWealthFrame();
}

function renderChartForge(imprint, apiFetch) {
  if (!imprint) return;
  window.apiFetch = apiFetch;
  try {
    renderBaziFrame(imprint);
    renderSealStack(imprint);
    bindChartModal();
    bindBaziInsightModal();
  } catch (err) {
    console.error("renderChartForge", err);
  }
}

function initChartForgeUI() {
  if (typeof window !== "undefined" && window.__chartForgeUIInit) return;
  if (typeof window !== "undefined") window.__chartForgeUIInit = true;

  document.addEventListener("click", (e) => {
    const el = e.target;
    if (!(el instanceof Element)) return;

    const sealToken = el.closest("[data-seal-token]");
    if (sealToken) {
      e.preventDefault();
      const token = sealToken.dataset.sealToken;
      if (token === "karma") openKarmicDebtToken();
      else openChartDeepRead(token, { showChart: token === "wealth" });
      return;
    }
    const traditionToken = el.closest("[data-tradition-token]");
    if (traditionToken) {
      e.preventDefault();
      openChartDeepRead(traditionToken.dataset.traditionToken, { showChart: true });
      return;
    }
    if (el.closest("#seal-numerology-open")) {
      e.preventDefault();
      openChartDeepRead("numerology");
      return;
    }
    if (el.closest("#relationships-frame-close")) {
      e.preventDefault();
      closeRelationshipsFrameTab();
      return;
    }
    if (el.closest("#bazi-modal-expand-chart")) {
      e.preventDefault();
      expandBaziFullChart();
      return;
    }
    if (el.closest("#bazi-frame-open-pillars")) {
      e.preventDefault();
      openBaziChartModal();
      return;
    }
    if (el.closest("[data-zero-insight-token]")) {
      e.preventDefault();
      const openZero =
        typeof openZeroInsightModal === "function"
          ? openZeroInsightModal
          : typeof window.openZeroInsightModal === "function"
            ? window.openZeroInsightModal
            : null;
      if (openZero) openZero();
      return;
    }
    const compoundBtn = el.closest("[data-compound-field]");
    if (compoundBtn) {
      e.preventDefault();
      openCompoundFrameworkModal(compoundBtn.dataset.compoundField);
      return;
    }

    if (el.closest("[data-ancients-wisdom-token]")) {
      e.preventDefault();
      openAncientsWisdomModal();
      return;
    }
  });
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChartForgeUI);
  } else {
    initChartForgeUI();
  }
}

if (typeof window !== "undefined") {
  window.initChartForgeUI = initChartForgeUI;
  window.renderSealRelationships = renderSealRelationships;
  window.renderSealStack = renderSealStack;
  window.renderSealLifeTokens = renderSealLifeTokens;
  window.renderChartForge = renderChartForge;
  window.renderWealthFrame = renderWealthFrame;
  window.openKarmicDebtToken = openKarmicDebtToken;
  window.openRelationshipsFrameTab = openRelationshipsFrameTab;
  window.closeRelationshipsFrameTab = closeRelationshipsFrameTab;
  window.openChartDeepRead = openChartDeepRead;
  window.openCompoundFrameworkModal = openCompoundFrameworkModal;
  window.formatHellenisticNarrative = formatHellenisticNarrative;
  window.formatFinancialNarrative = formatFinancialNarrative;
  window.formatZeroInsightNarrative = formatZeroInsightNarrative;
  window.formatBaziPillarsNarrative = formatBaziPillarsNarrative;
  window.formatAncientsWisdomNarrative = formatAncientsWisdomNarrative;
  window.openAncientsWisdomModal = openAncientsWisdomModal;
  window.formatVedicForgeNarrative = formatVedicForgeNarrative;
  window.openBaziChartModal = openBaziChartModal;
  window.openBaziFullInsightTab = openBaziFullInsightTab;
  window.expandBaziFullChart = expandBaziFullChart;
  window.closeBaziInsightModal = closeBaziInsightModal;
  window.openWealthHub = openWealthHub;
  window.openWealthChartTab = openWealthChartTab;
  window.openZeroWealthInsight = openZeroWealthInsight;
  window.closeWealthFrameTabs = closeWealthFrameTabs;
  window.canAccessZeroWealthInsight = canAccessZeroWealthInsight;
}

// ============================================================
// Consolidated Zero Depth token (replaces old Zero box + Karmic/Call)
// Short (quarter size), full width same as Challenge/Num/Bazi below.
// Click opens tab selector for Full Read, Wealth, Relationships, Karmic Debt.
// From tabs, expand individually (calls existing open functions).
// ============================================================

function openZeroDepthSelector() {
  const modal = document.getElementById('chart-modal');
  const titleEl = document.getElementById('chart-modal-title');
  const bodyEl = document.getElementById('chart-modal-body');
  if (!modal || !titleEl || !bodyEl) return;

  titleEl.textContent = 'Zero Depth';
  bodyEl.innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; margin-bottom: 0.5rem;">
      <button class="zero-tab-btn" data-open="full-read">Full Read</button>
      <button class="zero-tab-btn" data-open="wealth">Wealth</button>
      <button class="zero-tab-btn" data-open="relationships">Relationships</button>
      <button class="zero-tab-btn" data-open="karmic">Karmic Debt</button>
    </div>
    <p class="status" style="font-size: 0.72rem;">Select a tab above to open the individual read. Each can be expanded further from there.</p>
  `;
  modal.classList.remove('hidden');

  bodyEl.querySelectorAll('.zero-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      modal.classList.add('hidden');
      const openType = btn.dataset.open;
      try {
        if (openType === 'full-read') {
          if (typeof openZeroInsightModal === 'function') {
            openZeroInsightModal();
          } else {
            const el = document.getElementById('zero-insight-token');
            if (el) el.click();
          }
        } else if (openType === 'wealth') {
          const el = document.getElementById('seal-wealth-layer');
          if (el) el.click();
          else if (typeof openChartDeepRead === 'function') openChartDeepRead('wealth');
        } else if (openType === 'relationships') {
          const el = document.getElementById('seal-relationships-layer');
          if (el) el.click();
          else if (typeof openChartDeepRead === 'function') openChartDeepRead('relationships');
        } else if (openType === 'karmic') {
          if (typeof openKarmicDebtToken === 'function') {
            openKarmicDebtToken();
          } else {
            const el = document.getElementById('seal-karma-layer');
            if (el) el.click();
          }
        }
      } catch (e) {
        console.warn('Error opening Zero Depth tab:', e);
      }
    });
  });
}

function initZeroDepthToken() {
  const btn = document.getElementById('zero-depth-token');
  if (btn) {
    btn.addEventListener('click', openZeroDepthSelector);
  }
}

// Extend the existing init timeout to also init the consolidated token
if (typeof window !== 'undefined') {
  setTimeout(() => {
    try { initZeroPastEventTest(); } catch (e) { /* non fatal */ }
    try { initZeroDepthToken(); } catch (e) { /* non fatal */ }
  }, 1200);
}

// ============================================================
// Zero Past Event Challenge (the free "selling factor" test)
// Placed above Numerology. Removes The Call box (Karmic Debt token kept standalone).
// Offers test, runs personalized Zero reconstruction for the date + event,
// presents plain-English results in the chart modal, up to 3 refinement rounds.
// On 3rd decline/failure: apologize + log via /account/zero-test-failure for premium notes.
// Test is free; full power is premium only.
// ============================================================

let zeroTestCurrentRound = 0;
const ZERO_TEST_MAX_ROUNDS = 3;

function initZeroPastEventTest() {
  const runBtn = document.getElementById('zero-test-run');
  if (!runBtn) return;

  runBtn.addEventListener('click', async () => {
    const dateEl = document.getElementById('zero-test-date');
    const eventEl = document.getElementById('zero-test-event');
    const pastDate = dateEl ? dateEl.value : '';
    const eventDesc = eventEl ? eventEl.value.trim() : '';

    if (!pastDate || !eventDesc || eventDesc.length < 10) {
      alert('Please enter a valid date and a meaningful description of the past event (at least 10 characters).');
      return;
    }

    // Initial approval before consuming the free test
    const approveFirst = confirm(
      `FREE ZERO PAST EVENT TEST\n\n` +
      `Date: ${pastDate}\n` +
      `Event: ${eventDesc.substring(0, 120)}...\n\n` +
      `This will reconstruct your full chart for that exact date using your imprint (bazi, numerology, sky, Zero framework) and explain in plain English how the occult dynamics explain what happened.\n\n` +
      `You get up to 3 honest rounds of refinement if it doesn't land.\n\n` +
      `Approve to run the free test now?`
    );

    if (!approveFirst) {
      // First decline — offer follow up seeking deeper insight
      const why = prompt('What made you decline the test? (optional but helps the system learn — we log it only if you purchase later)');
      if (why) {
        // second follow up prompt
        const deeper = prompt('To give you the best free feedback possible: what specific part of the idea of this test feels off or untrustworthy to you?');
        if (deeper) {
          alert('Thank you for the honest feedback. The system has noted your concerns for future improvement. You can still try the test later with a different event.');
        }
      }
      return;
    }

    zeroTestCurrentRound = 1;
    await executeZeroPastTest(pastDate, eventDesc, null, null, zeroTestCurrentRound);
  });
}

async function executeZeroPastTest(pastDate, eventDesc, previousAnalysis, feedback, round) {
  const modal = document.getElementById('chart-modal');
  const titleEl = document.getElementById('chart-modal-title');
  const bodyEl = document.getElementById('chart-modal-body');
  if (!modal || !titleEl || !bodyEl) return;

  titleEl.textContent = `Zero Past Event Test — Round ${round}/3`;
  bodyEl.innerHTML = `<p class="status">Zero is reconstructing your chart for ${pastDate} and running the analysis against the event...<br>This is a deep, personalized stress-test of the full system. Please wait.</p>`;
  modal.classList.remove('hidden');

  try {
    const payload = {
      past_date: pastDate,
      event_description: eventDesc,
      previous_analysis: previousAnalysis,
      feedback: feedback,
      round: round
    };

    const isPreview = (typeof window !== 'undefined' && window.occultImprint && typeof window.apiFetch !== 'function');

    let res, data;
    if (isPreview) {
      payload.imprint = window.occultImprint;
      res = await fetch('/reflection/zero/past-test/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } else {
      res = await window.apiFetch('/reflection/zero/past-test', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
    }
    data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'The test could not be completed.');

    renderZeroTestResults(data, pastDate, eventDesc, round);
  } catch (err) {
    bodyEl.innerHTML = `<p class="status error">Zero encountered an issue with this test round: ${err.message}<br>Please try a different event or date, or come back later.</p>`;
  }
}

function renderZeroTestResults(data, pastDate, eventDesc, round) {
  const bodyEl = document.getElementById('chart-modal-body');
  const titleEl = document.getElementById('chart-modal-title');
  if (!bodyEl || !titleEl) return;

  titleEl.textContent = `Zero Past Event Test Results — Round ${round}`;

  const analysisText = data.analysis || 'No detailed analysis was returned. The system may need more specific event details.';

  let processed = analysisText.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');

  // Replace token markers with buttons (populated from referenced_charts if present)
  if (data.referenced_charts) {
    processed = processed.replace(/\[\[NATAL_CHART\]\]/g, '<button class="chart-token-btn" data-type="natal">View Full Natal Chart</button>');
    processed = processed.replace(/\[\[DAY_CHART:([^\]]+)\]\]/g, (m, d) => `<button class="chart-token-btn" data-type="day" data-date="${d}">View Full Chart for ${d}</button>`);
  }

  let html = `
    <div class="zero-test-results-wrap">
      <p class="zero-test-context"><strong>Date tested:</strong> ${pastDate}<br>
      <strong>Your event:</strong> ${eventDesc.substring(0, 140)}${eventDesc.length > 140 ? '...' : ''}</p>
      <div class="zero-test-analysis">
        ${processed}
      </div>
    </div>
  `;

  if (round < ZERO_TEST_MAX_ROUNDS) {
    html += `
      <div class="zero-test-actions" style="margin-top:1rem; border-top:1px solid rgba(255,215,0,0.2); padding-top:0.75rem;">
        <button id="zt-approve" class="btn" style="margin-right:0.5rem;">This resonates — I'm satisfied</button>
        <div style="margin-top:0.75rem;">
          <p style="margin:0 0 0.25rem; font-size:0.85rem;">Doesn't fully land? Give honest feedback for a refinement round (${round+1}/${ZERO_TEST_MAX_ROUNDS}). Be specific about what felt off.</p>
          <textarea id="zt-feedback" rows="2" style="width:100%; box-sizing:border-box;" placeholder="What part didn't match your memory or felt wrong?"></textarea>
          <button id="zt-refine" class="btn" style="margin-top:0.4rem;">Submit Feedback &amp; Refine</button>
        </div>
      </div>
    `;
  } else {
    html += `
      <p style="margin-top:1rem; font-size:0.9rem; color:#c9a227;">This was round 3. If it still doesn't resonate, the system will document this as a failure for your record (in case you later purchase premium service).</p>
      <button id="zt-final-close" class="btn">Close &amp; Log for Record</button>
    `;
  }

  bodyEl.innerHTML = html;

  // Wire actions
  const approve = document.getElementById('zt-approve');
  if (approve) {
    approve.onclick = () => {
      document.getElementById('chart-modal').classList.add('hidden');
    };
  }

  const refine = document.getElementById('zt-refine');
  if (refine) {
    refine.onclick = () => {
      const fb = (document.getElementById('zt-feedback') || {}).value || '';
      if (!fb.trim()) {
        alert('Please enter specific feedback so Zero can refine the analysis.');
        return;
      }
      document.getElementById('chart-modal').classList.add('hidden');
      zeroTestCurrentRound = round + 1;
      const date = document.getElementById('zero-test-date').value;
      const ev = document.getElementById('zero-test-event').value;
      executeZeroPastTest(date, ev, analysisText, fb.trim(), zeroTestCurrentRound);
    };
  }

  const finalClose = document.getElementById('zt-final-close');
  if (finalClose) {
    finalClose.onclick = () => {
      document.getElementById('chart-modal').classList.add('hidden');
      logZeroTestFailure(pastDate, eventDesc, round, 'user declined after maximum rounds');
    };
  }

  // Attach chart token buttons from the analysis text
  const tokenBtns = bodyEl.querySelectorAll('.chart-token-btn');
  tokenBtns.forEach(btn => {
    btn.onclick = () => {
      const type = btn.dataset.type;
      const date = btn.dataset.date;
      showReferencedChart(type, date, data.referenced_charts || {});
    };
  });
}

function showReferencedChart(type, date, charts) {
  const modal = document.getElementById('chart-modal');
  const titleEl = document.getElementById('chart-modal-title');
  const bodyEl = document.getElementById('chart-modal-body');
  if (!modal || !titleEl || !bodyEl) return;

  if (type === 'natal') {
    titleEl.textContent = 'Natal / Previous Chart';
    const natal = charts.natal || {};
    bodyEl.innerHTML = `
      <p>This is the natal (previous) chart referenced in the analysis. Select the token for that day's read to see the full chart for the event date.</p>
      <pre style="white-space: pre-wrap; font-size: 0.75rem; background: #111; padding: 0.5rem; border-radius: 4px; max-height: 400px; overflow: auto;">${JSON.stringify(natal, null, 2)}</pre>
      <button onclick="document.getElementById('chart-modal').classList.add('hidden');" style="margin-top: 0.5rem;">Close</button>
    `;
  } else if (type === 'day') {
    titleEl.textContent = `Full Chart for ${date}`;
    const day = charts.day || {};
    bodyEl.innerHTML = `
      <p>This is the full reconstructed chart for the event date ${date} referenced above. Select the token to view it and see how the occult factors applied to your event.</p>
      <pre style="white-space: pre-wrap; font-size: 0.75rem; background: #111; padding: 0.5rem; border-radius: 4px; max-height: 400px; overflow: auto;">${JSON.stringify(day, null, 2)}</pre>
      <button onclick="document.getElementById('chart-modal').classList.add('hidden');" style="margin-top: 0.5rem;">Close</button>
    `;
  }
}

async function logZeroTestFailure(pastDate, eventDesc, rounds, reason) {
  try {
    const payload = {
      past_date: pastDate,
      event_description: eventDesc,
      rounds: rounds,
      reason: reason
    };
    const isPreview = (typeof window !== 'undefined' && window.occultImprint && typeof window.apiFetch !== 'function');
    if (isPreview) {
      console.info('[Zero Test] Preview failure logged (would save to notes on purchase):', payload);
      return;
    }
    await window.apiFetch('/account/zero-test-failure', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  } catch (e) {
    console.warn('Failed to log zero test failure (non-critical):', e);
  }
}

// Auto-init when the page/dashboard loads
if (typeof window !== 'undefined') {
  // Run after other inits
  setTimeout(() => {
    try { initZeroPastEventTest(); } catch (e) { /* non fatal */ }
  }, 1200);
}
