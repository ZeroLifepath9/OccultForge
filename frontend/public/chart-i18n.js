/** English labels for chart display (Hanzi kept as symbols). */

const STEM_PINYIN = {
  "甲": "Jia", "乙": "Yi", "丙": "Bing", "丁": "Ding",
  "戊": "Wu", "己": "Ji", "庚": "Geng", "辛": "Xin",
  "壬": "Ren", "癸": "Gui",
};

/** Heavenly stem — English, polarity, element (for full pillar translation). */
const STEM_META = {
  "甲": { english: "Jia", yin_yang: "Yang", element: "Wood" },
  "乙": { english: "Yi", yin_yang: "Yin", element: "Wood" },
  "丙": { english: "Bing", yin_yang: "Yang", element: "Fire" },
  "丁": { english: "Ding", yin_yang: "Yin", element: "Fire" },
  "戊": { english: "Wu", yin_yang: "Yang", element: "Earth" },
  "己": { english: "Ji", yin_yang: "Yin", element: "Earth" },
  "庚": { english: "Geng", yin_yang: "Yang", element: "Metal" },
  "辛": { english: "Xin", yin_yang: "Yin", element: "Metal" },
  "壬": { english: "Ren", yin_yang: "Yang", element: "Water" },
  "癸": { english: "Gui", yin_yang: "Yin", element: "Water" },
};

const BRANCH_ANIMAL = {
  "子": "Rat", "丑": "Ox", "寅": "Tiger", "卯": "Rabbit",
  "辰": "Dragon", "巳": "Snake", "午": "Horse", "未": "Goat",
  "申": "Monkey", "酉": "Rooster", "戌": "Dog", "亥": "Pig",
};

/** Root 本气 hidden stem per branch (藏干) — client fallback for sealed imprints. */
const BRANCH_HIDDEN_ROOT = {
  "子": { stem: "癸", element: "Water" },
  "丑": { stem: "己", element: "Earth" },
  "寅": { stem: "甲", element: "Wood" },
  "卯": { stem: "乙", element: "Wood" },
  "辰": { stem: "戊", element: "Earth" },
  "巳": { stem: "丙", element: "Fire" },
  "午": { stem: "丁", element: "Fire" },
  "未": { stem: "己", element: "Earth" },
  "申": { stem: "庚", element: "Metal" },
  "酉": { stem: "辛", element: "Metal" },
  "戌": { stem: "戊", element: "Earth" },
  "亥": { stem: "壬", element: "Water" },
};

/** Full classical 藏干 table — root, center, remnant qi. */
const BRANCH_HIDDEN_FULL = {
  "子": [{ stem: "癸", element: "Water", role: "root" }],
  "丑": [
    { stem: "己", element: "Earth", role: "root" },
    { stem: "癸", element: "Water", role: "center" },
    { stem: "辛", element: "Metal", role: "remnant" },
  ],
  "寅": [
    { stem: "甲", element: "Wood", role: "root" },
    { stem: "丙", element: "Fire", role: "center" },
    { stem: "戊", element: "Earth", role: "remnant" },
  ],
  "卯": [{ stem: "乙", element: "Wood", role: "root" }],
  "辰": [
    { stem: "戊", element: "Earth", role: "root" },
    { stem: "乙", element: "Wood", role: "center" },
    { stem: "癸", element: "Water", role: "remnant" },
  ],
  "巳": [
    { stem: "丙", element: "Fire", role: "root" },
    { stem: "戊", element: "Earth", role: "center" },
    { stem: "庚", element: "Metal", role: "remnant" },
  ],
  "午": [
    { stem: "丁", element: "Fire", role: "root" },
    { stem: "己", element: "Earth", role: "center" },
  ],
  "未": [
    { stem: "己", element: "Earth", role: "root" },
    { stem: "丁", element: "Fire", role: "center" },
    { stem: "乙", element: "Wood", role: "remnant" },
  ],
  "申": [
    { stem: "庚", element: "Metal", role: "root" },
    { stem: "壬", element: "Water", role: "center" },
    { stem: "戊", element: "Earth", role: "remnant" },
  ],
  "酉": [{ stem: "辛", element: "Metal", role: "root" }],
  "戌": [
    { stem: "戊", element: "Earth", role: "root" },
    { stem: "辛", element: "Metal", role: "center" },
    { stem: "丁", element: "Fire", role: "remnant" },
  ],
  "亥": [
    { stem: "壬", element: "Water", role: "root" },
    { stem: "甲", element: "Wood", role: "center" },
  ],
};

const ELEMENT_BADGE_CLASS = {
  Wood: "bazi-el-badge--wood",
  Fire: "bazi-el-badge--fire",
  Earth: "bazi-el-badge--earth",
  Metal: "bazi-el-badge--metal",
  Water: "bazi-el-badge--water",
};

const SIGN_GLYPH = {
  Aries: "♈", Taurus: "♉", Gemini: "♊", Cancer: "♋",
  Leo: "♌", Virgo: "♍", Libra: "♎", Scorpio: "♏",
  Sagittarius: "♐", Capricorn: "♑", Aquarius: "♒", Pisces: "♓",
};

function stemEnglish(stem) {
  return STEM_PINYIN[stem] || stem;
}

function stemMeta(stem) {
  const m = STEM_META[stem] || {};
  return {
    english: m.english || stemEnglish(stem),
    yin_yang: m.yin_yang || "",
    element: m.element || "",
  };
}

function elementClass(element) {
  return (
    { Wood: "element-wood", Fire: "element-fire", Earth: "element-earth", Metal: "element-metal", Water: "element-water" }[
      element
    ] || ""
  );
}

function elementIcon(element) {
  if (!element) return "";
  const svg = typeof ELEMENT_SVGS !== "undefined" ? ELEMENT_SVGS[element] : "";
  const cls = elementClass(element);
  if (svg) {
    return `<span class="chart-sym chart-sym--element ${cls}" title="${element}" aria-hidden="true">${svg}</span>`;
  }
  const badgeCls = ELEMENT_BADGE_CLASS[element] || "bazi-el-badge";
  return `<span class="bazi-el-badge ${badgeCls}" title="${element}">${element}</span>`;
}

function elementBadge(element) {
  return elementIcon(element);
}

function animalTotemMini(animal, element) {
  if (!animal) return "";
  const key =
    (typeof ANIMAL_TOTEM_KEY !== "undefined" && ANIMAL_TOTEM_KEY[animal]) ||
    animal.toLowerCase();
  const svg = typeof TOTEM_SVGS !== "undefined" ? TOTEM_SVGS[key] : "";
  if (!svg) return `<span class="chart-sym chart-sym--animal-fallback" title="${animal}">${animal}</span>`;
  const cls = elementClass(element);
  return `<span class="chart-sym chart-sym--animal ${cls}" title="${animal}" aria-hidden="true">${svg}</span>`;
}

function chartSymbolRow(element, animal) {
  return `<span class="chart-sym-row">${elementIcon(element)}${animal ? animalTotemMini(animal, element) : ""}</span>`;
}

function enrichPillarHidden(pillar) {
  if (!pillar) return null;
  if (pillar.hidden_stem) return pillar;
  const root = BRANCH_HIDDEN_ROOT[pillar.branch];
  if (!root) return pillar;
  return {
    ...pillar,
    hidden_stem: root.stem,
    hidden_stem_en: stemEnglish(root.stem),
    hidden_stem_element: root.element,
    hidden_role_label: "本气",
    branch_en: pillar.branch_en || branchAnimal(pillar.branch),
  };
}

const ELEMENT_GENERATES = {
  Wood: "Fire",
  Fire: "Earth",
  Earth: "Metal",
  Metal: "Water",
  Water: "Wood",
};

const ELEMENT_CONTROLS = {
  Wood: "Earth",
  Earth: "Water",
  Water: "Fire",
  Fire: "Metal",
  Metal: "Wood",
};

/** Visible stem element + branch animal — primary identity; never 藏干. */
function pillarIdentityLabel(pillar, { yearStyle = false } = {}) {
  if (!pillar) return "—";
  const animal = pillar.branch_en || branchAnimal(pillar.branch);
  const el = pillar.stem_element || stemMeta(pillar.stem).element;
  if (yearStyle) return el ? `${el} ${animal}` : animal;
  const yy = stemMeta(pillar.stem).yin_yang;
  return yy && el ? `${yy} ${el} ${animal}` : el ? `${el} ${animal}` : animal;
}

/** Supplementary branch 本气: hidden element + animal only. */
function branchHiddenIdentityLabel(pillar) {
  const p = enrichPillarHidden(pillar);
  if (!p) return "";
  const animal = p.branch_en || branchAnimal(p.branch);
  const el = p.hidden_stem_element;
  return el && animal ? `${el} ${animal}` : "";
}

/** Augmented line: visible element · hidden element · zodiac. */
function pillarDisplayLine(pillar) {
  if (!pillar) return "—";
  if (pillar.display_line) return pillar.display_line;
  const p = enrichPillarHidden(pillar);
  const visible = p.stem_element || stemMeta(p.stem).element;
  const animal = p.branch_en || branchAnimal(p.branch);
  const hidden = p.hidden_stem_element;
  const hsEn = p.hidden_stem_en || (p.hidden_stem ? stemEnglish(p.hidden_stem) : "");
  if (!animal) return visible || "—";
  if (!hidden) return visible ? `${visible} ${animal}` : animal;
  if (hidden === visible) return `${visible} ${animal}`;
  return `${visible} · hidden ${hsEn} ${hidden} · ${animal}`;
}

function pillarElementSynergy(pillar) {
  if (pillar?.synergy_note) return pillar.synergy_note;
  const p = enrichPillarHidden(pillar);
  const visible = p.stem_element || stemMeta(p.stem).element;
  const hidden = p.hidden_stem_element;
  if (!visible || !hidden) return "";
  if (visible === hidden) {
    return `Visible ${visible} and branch 本气 ${hidden} align — inner reservoir echoes the stem.`;
  }
  if (ELEMENT_GENERATES[visible] === hidden) {
    return `Visible ${visible} generates hidden ${hidden} — outward expression feeds an inner layer beneath the stem.`;
  }
  if (ELEMENT_GENERATES[hidden] === visible) {
    return `Hidden ${hidden} generates visible ${visible} — the branch supplies fuel beneath your stem.`;
  }
  if (ELEMENT_CONTROLS[visible] === hidden) {
    return `Visible ${visible} regulates hidden ${hidden} — you discipline inner drives before they surface.`;
  }
  if (ELEMENT_CONTROLS[hidden] === visible) {
    return `Hidden ${hidden} checks visible ${visible} — inner pressure refines outward expression.`;
  }
  return `Visible ${visible} and hidden ${hidden} run as parallel tracks until timing activates the branch.`;
}

/** Symbol row: visible element · 藏干 chip · hidden element · zodiac */
function pillarHiddenRow(item) {
  if (!item) return "—";
  const p = enrichPillarHidden(item);
  const visibleEl = p.stem_element || stemMeta(p.stem).element;
  const hiddenEl = p.hidden_stem_element;
  const animal = p.branch_en || branchAnimal(p.branch);
  const hs = p.hidden_stem || "";
  const hsEn = p.hidden_stem_en || (hs ? stemEnglish(hs) : "");
  const role = p.hidden_role_label || "本气";
  const parts = [];
  if (visibleEl) parts.push(elementIcon(visibleEl));
  if (hs) {
    parts.push(
      `<span class="hidden-stem-chip" title="藏干 ${role}"><span class="hanzi">${hs}</span><span class="hidden-stem-en">${hsEn}</span></span>`
    );
  }
  if (hiddenEl && hiddenEl !== visibleEl) parts.push(elementIcon(hiddenEl));
  if (animal) parts.push(animalTotemMini(animal, visibleEl));
  return `<span class="chart-sym-row pillar-hidden-row">${parts.join("")}</span>`;
}

const QI_WEIGHT_LABEL = { root: "~70%", center: "~22%", remnant: "~8%" };
const QI_ROLE_LABEL = { root: "本气", center: "中气", remnant: "余气" };

function hiddenStemsForBranch(branch) {
  const full = BRANCH_HIDDEN_FULL[branch];
  if (!full) return [];
  return full.map((hs) => ({
    ...hs,
    role_label: QI_ROLE_LABEL[hs.role] || "本气",
    weight_label: QI_WEIGHT_LABEL[hs.role] || "",
  }));
}

function hiddenStemsQiLine(pillar) {
  const stems = (pillar.all_hidden_stems && pillar.all_hidden_stems.length)
    ? pillar.all_hidden_stems
    : hiddenStemsForBranch(pillar.branch);
  if (!stems.length) return "";
  if (stems.length === 1) {
    const hs = stems[0];
    const en = hs.stem_en || stemEnglish(hs.stem);
    return `Pure branch — single 本气 ${en} ${hs.element} (${hs.weight_label || "~70%"}).`;
  }
  return stems
    .map((hs) => {
      const en = hs.stem_en || stemEnglish(hs.stem);
      const role = hs.role_label || QI_ROLE_LABEL[hs.role] || "本气";
      const wt = hs.weight_label || QI_WEIGHT_LABEL[hs.role] || "";
      return `${en} ${hs.element} ${role} (${wt})`;
    })
    .join(" · ");
}

/** @deprecated Use branchHiddenIdentityLabel — supplementary only, never primary identity. */
function hiddenPillarTextLabel(pillar) {
  return branchHiddenIdentityLabel(pillar) || pillarDisplayLine(pillar);
}

function combinedPillarLabel(pillar, { yearStyle = false } = {}) {
  return pillarIdentityLabel(pillar, { yearStyle });
}

function lensPillarCard(imprint, pillarKey) {
  const lens = imprint?.bazi?.interpretation_lens;
  return lens?.pillars?.[pillarKey] || null;
}

function baziPillarDetailHtml(label, pillar, { yearStyle = false, imprint = null, pillarKey = null } = {}) {
  if (!pillar) return "";
  const pl = pillarLabel(pillar);
  const sm = stemMeta(pillar.stem);
  const stemEl = pl.stemElement || sm.element;
  const lensCard = imprint && pillarKey ? lensPillarCard(imprint, pillarKey) : null;
  const combined = lensCard?.identity || pillarIdentityLabel(pillar, { yearStyle });
  const displayLine = lensCard?.display_line || pillarDisplayLine(pillar);
  const synergy = lensCard?.synergy_note || pillarElementSynergy(pillar);
  const adviceHook = lensCard?.advice_hook || "";
  const allHidden = hiddenStemsQiLine(pillar);
  const hiddenAug = branchHiddenIdentityLabel(pillar);
  const hookClause = adviceHook && !synergy.includes(adviceHook) ? ` ${adviceHook}` : "";
  const partVal = hiddenAug
    ? `${displayLine}. ${synergy}${hookClause} ${allHidden} <span class="hanzi">${pl.stemHanzi}${pl.branchHanzi}</span>`
    : `${sm.yin_yang} ${stemEl} stem · ${pl.branchEn} branch · ${sm.english} <span class="hanzi">${pl.stemHanzi}${pl.branchHanzi}</span>`;
  return `
    <li class="bazi-pillar-item">
      <div class="bazi-pillar-head">
        <span class="chart-k">${label}</span>
        <strong class="bazi-pillar-combined">${combined}</strong>
        <span class="bazi-pillar-gz"><span class="hanzi">${pl.ganZhi}</span></span>
      </div>
      <div class="bazi-pillar-lines bazi-pillar-lines--inline">
        <span class="bazi-part-val">${partVal}</span>
      </div>
    </li>`;
}

function dayMasterDetailHtml(dm, dayPillar) {
  if (!dm?.stem) return "";
  const sm = stemMeta(dm.stem);
  const el = dm.element || sm.element;
  const yy = dm.yin_yang || sm.yin_yang;
  const en = dm.english || sm.english;
  const dayAn = dayPillar ? branchAnimal(dayPillar.branch) : "";
  const dayCombined = dayPillar ? pillarIdentityLabel(dayPillar) : "";
  const displayLine = dayPillar ? pillarDisplayLine(dayPillar) : "";
  const synergy = dayPillar ? pillarElementSynergy(dayPillar) : "";
  return `
    <li class="bazi-pillar-item bazi-pillar-item--dm">
      <div class="bazi-pillar-head">
        <span class="chart-k">Day pillar storm</span>
        <strong class="bazi-pillar-combined">${dayCombined || `${yy} ${el} · ${en}`}</strong>
        <span class="bazi-dm-sub">${displayLine || "element · hidden · zodiac"}</span>
      </div>
      <div class="bazi-dm-body">
        <span class="bazi-part-val">Day Master: ${yy} ${el} · ${en}. ${synergy || "Branch 藏干 sits beneath the visible stem."}</span>
        <span class="hanzi bazi-dm-hz">${dm.stem}${dayPillar?.branch || ""}</span>
      </div>
    </li>`;
}

function luckPillarLens(imprint) {
  return (
    imprint?.bazi?.interpretation_lens?.luck_pillar
    || imprint?.bazi?.luck?.interpretation
    || {}
  );
}

function luckPillarDetailHtml(imprint) {
  const luck = luckPillarLens(imprint);
  const current = luck.current;
  const framework = luck.framework_insight || "";
  const future = luck.future_preview || [];
  const rawLuck = imprint?.bazi?.luck?.current;

  if (!current && !framework) return "";

  let currentHtml = "";
  if (current) {
    const gz = current.gan_zhi || "";
    const stem = gz[0] || "";
    const branch = gz[gz.length - 1] || "";
    const stemEl = current.stem_element || stemMeta(stem).element;
    const animal = current.branch_en || branchAnimal(branch);
    const years =
      current.start_year && current.end_year
        ? `${current.start_year}–${current.end_year}`
        : "";
    const decadePos =
      current.years_into_decade != null
        ? `Year ${current.years_into_decade} of this decade`
        : "";
    const phase = current.phase_label || "";
    const citation = current.advice_citation || "";
    const withYou = (current.working_with_you || []).slice(0, 2).join(" · ");
    const againstYou = (current.working_against_you || []).slice(0, 1).join(" · ");
    const stemRole = current.luck_stem_role || "";
    const branchRole = current.luck_branch_role || "";
    const hiddenEl = current.hidden_stem_element || "";
    currentHtml = `
    <li class="bazi-pillar-item bazi-pillar-item--luck">
      <div class="bazi-pillar-head">
        <span class="chart-k">Current luck pillar</span>
        <strong class="bazi-pillar-combined">${current.identity || pillarSymbolLine(current)}</strong>
        <span class="bazi-pillar-gz"><span class="hanzi">${gz}</span></span>
      </div>
      <div class="bazi-pillar-lines bazi-pillar-lines--inline">
        <span class="bazi-part-val">${current.display_line || pillarDisplayLine(rawLuck || current)}${years ? ` · ${years}` : ""}${decadePos ? ` · ${decadePos}` : ""}${phase ? ` · ${phase}` : ""}${stemRole ? ` · Stem ${stemRole}` : ""}${branchRole ? ` · Branch ${branchRole}` : ""}${hiddenEl ? ` · Hidden ${hiddenEl}` : ""}</span>
      </div>
      ${citation ? `<p class="bazi-luck-citation">${citation}</p>` : ""}
      ${withYou ? `<p class="bazi-luck-note bazi-luck-note--with">Working with you: ${withYou}</p>` : ""}
      ${againstYou ? `<p class="bazi-luck-note bazi-luck-note--against">Friction: ${againstYou}</p>` : ""}
    </li>`;
  } else if (framework) {
    currentHtml = `
    <li class="bazi-pillar-item bazi-pillar-item--luck">
      <div class="bazi-pillar-head">
        <span class="chart-k">Current luck pillar</span>
        <strong class="bazi-pillar-combined">Minor luck window</strong>
      </div>
      <p class="bazi-part-val">${framework}</p>
    </li>`;
  }

  const frameworkHtml =
    current && framework
      ? `<li class="bazi-luck-framework-block">
      <p class="chart-k chart-k--block">Luck pillar framework</p>
      <p class="bazi-luck-framework-text">${framework}</p>
    </li>`
      : "";

  const futureRows = future
    .map((fp) => {
      const years =
        fp.start_year && fp.end_year ? `${fp.start_year}–${fp.end_year}` : "";
      const until = fp.years_until != null ? `in ${fp.years_until} yr` : "";
      const teaser = fp.teaser || fp.identity || "";
      return `<li class="bazi-luck-future-row">
        <span class="bazi-luck-future-head">
          <strong>${fp.identity || ganZhiToEnglish(fp.gan_zhi)}</strong>
          <span class="hanzi">${fp.gan_zhi || ""}</span>
          ${years ? `<span class="bazi-luck-future-years">${years}</span>` : ""}
          ${until ? `<span class="bazi-luck-future-until">${until}</span>` : ""}
          <span class="seeker-teaser-badge" title="Full decade read with Seeker+">Seeker+</span>
        </span>
        <span class="seeker-teaser">${teaser}</span>
      </li>`;
    })
    .join("");

  const futureHtml = futureRows
    ? `<li class="bazi-pillar-item bazi-pillar-item--luck-future">
      <p class="chart-k chart-k--block">Upcoming luck decades <span class="seeker-teaser-badge">Preview</span></p>
      <ul class="bazi-luck-future-list">${futureRows}</ul>
    </li>`
    : "";

  return `${currentHtml}${frameworkHtml}${futureHtml}`;
}

function yearZodiacDetailHtml(imprint) {
  const yz = yearZodiacFromImprint(imprint);
  const year = imprint?.bazi?.pillars?.year;
  if (!year) return "";
  const combined = yz.label || combinedPillarLabel(year, { yearStyle: true });
  const branchHidden = year.hidden_stem_en && year.hidden_stem_element
    ? `${year.hidden_stem_en} ${year.hidden_stem_element} (branch hidden stem)`
    : "";
  return `
    <li class="bazi-pillar-item bazi-pillar-item--year">
      <div class="bazi-pillar-head">
        <span class="chart-k">Year zodiac</span>
        <strong class="bazi-pillar-combined">${combined}</strong>
        <span class="bazi-pillar-gz"><span class="hanzi">${yz.gan_zhi}</span></span>
      </div>
      <div class="bazi-pillar-lines bazi-pillar-lines--inline">
        <span class="bazi-part-val">Birth-year zodiac: ${yz.stem_english || stemEnglish(year.stem)} ${yz.stem_element} stem + ${yz.animal} branch.${branchHidden ? ` Branch also holds ${branchHidden}.` : ""}</span>
      </div>
    </li>`;
}

function branchAnimal(branch) {
  return BRANCH_ANIMAL[branch] || branch;
}

function signGlyph(sign) {
  return SIGN_GLYPH[sign] || "";
}

function pillarLabel(pillar) {
  const stem = pillar.stem || "";
  const branch = pillar.branch || "";
  return {
    ganZhi: pillar.gan_zhi || `${stem}${branch}`,
    stemEn: stemEnglish(stem),
    branchEn: branchAnimal(branch),
    stemHanzi: stem,
    branchHanzi: branch,
    stemElement: pillar.stem_element || "",
    branchElement: pillar.branch_element || "",
  };
}

function numerologyDisplay(num) {
  if (!num) return "—";
  const compound = num.compound;
  const value = num.value;
  if (compound == null || value == null) return "—";
  if (num.is_master) {
    const trail = compound === value ? "" : ` (${compound}/${value})`;
    return `Master ${value}${trail}`;
  }
  if (compound === value) return String(value);
  return `${compound}/${value}`;
}

function lifePathDisplay(imprint) {
  const lp = imprint?.numerology?.schools?.pythagorean?.life_path;
  return numerologyDisplay(lp);
}

/** Two-character pillar e.g. 辛亥 → Xin Pig */
function ganZhiToEnglish(ganZhi) {
  if (!ganZhi || typeof ganZhi !== "string") return "—";
  const gz = ganZhi.trim();
  if (gz.length < 2) return gz;
  const stem = gz[0];
  const branch = gz[gz.length - 1];
  return `${stemEnglish(stem)} ${branchAnimal(branch)}`;
}

function reduceNumerology(total) {
  let compound = total;
  let current = total;
  while (current > 9 && current !== 11 && current !== 22 && current !== 33) {
    current = String(current)
      .split("")
      .reduce((a, c) => a + parseInt(c, 10), 0);
  }
  return { compound, value: current };
}

function universalYearDisplay(year = new Date().getFullYear()) {
  const r = reduceNumerology(
    String(year)
      .split("")
      .reduce((a, c) => a + parseInt(c, 10), 0)
  );
  return r.compound === r.value ? String(r.value) : `${r.compound}/${r.value}`;
}

/**
 * Birth-year Chinese zodiac: YEAR stem element + YEAR branch animal only.
 * Never use day_master.element here — that caused "Earth Goat" when year is Metal Goat.
 */
function yearZodiacFromImprint(imprint) {
  const cached = imprint?.bazi?.year_zodiac;
  const year = imprint?.bazi?.pillars?.year;
  if (cached?.label) {
    if (!cached.hidden_stem && year) {
      const enriched = enrichPillarHidden(year);
      return {
        ...cached,
        hidden_stem: enriched.hidden_stem,
        hidden_stem_en: enriched.hidden_stem_en,
        hidden_stem_element: enriched.hidden_stem_element,
        branch_hidden_label: branchHiddenIdentityLabel(year),
      };
    }
    return cached;
  }
  if (!year) {
    return { label: "—", stem_element: "", animal: "", gan_zhi: "", stem_english: "" };
  }
  const animal = branchAnimal(year.branch);
  const element = year.stem_element || "";
  const enriched = enrichPillarHidden(year);
  return {
    gan_zhi: year.gan_zhi || `${year.stem || ""}${year.branch || ""}`,
    stem_element: element,
    animal,
    label: element ? `${element} ${animal}` : animal,
    hidden_stem: enriched.hidden_stem,
    hidden_stem_en: enriched.hidden_stem_en,
    hidden_stem_element: enriched.hidden_stem_element,
    branch_hidden_label: branchHiddenIdentityLabel(year),
    stem_english: stemEnglish(year.stem),
  };
}

function baziPillarEnglish(payload, imprint) {
  const b = payload?.bazi || {};
  let natal = b.natal_day_pillar_en;
  let current = b.current_day_pillar_en;
  let dm = b.day_master_en;
  if (!natal && imprint?.bazi?.pillars?.day) {
    const d = imprint.bazi.pillars.day;
    natal = `${stemEnglish(d.stem)} ${branchAnimal(d.branch)}`;
  }
  if (!current && b.current_day_pillar) {
    current = ganZhiToEnglish(b.current_day_pillar);
  }
  if (!dm && imprint?.bazi?.day_master?.stem) {
    dm = stemEnglish(imprint.bazi.day_master.stem);
  }
  return { natal, current, dm };
}

/** Combined English label for BaZi flow rows (no emoji — text only) */
function pillarSymbolLine(pillar) {
  if (!pillar) return "—";
  if (pillar.display_line) return pillar.display_line;
  if (pillar.label && pillar.branch_en) return pillar.label;
  if (pillar.stem && pillar.branch) {
    return pillarDisplayLine(pillar);
  }
  const animal = pillar.branch_en || branchAnimal(pillar.branch);
  const el = pillar.stem_element || stemMeta(pillar.stem).element;
  return el && animal ? `${el} ${animal}` : animal || "—";
}

function pillarFlowLine(pillar, label) {
  if (!pillar) return "";
  const gz = pillar.gan_zhi || `${pillar.stem || ""}${pillar.branch || ""}`;
  return `<div class="pillar-flow-row"><span class="pillar-flow-label">${label}</span><span class="pillar-flow-val">${pillarSymbolLine(pillar)}</span><span class="pillar-flow-hz hanzi">${gz}</span></div>`;
}

function pillarCompareLine(label, pillarOrGz, imprintPillar) {
  let pillar = pillarOrGz;
  if (typeof pillarOrGz === "string") {
    const gz = pillarOrGz.trim();
    if (gz.length >= 2) {
      pillar = {
        stem: gz[0],
        branch: gz[gz.length - 1],
        gan_zhi: gz,
        stem_en: stemEnglish(gz[0]),
        branch_en: branchAnimal(gz[gz.length - 1]),
        stem_element: imprintPillar?.stem_element || "",
      };
    }
  }
  if (!pillar && imprintPillar) {
    pillar = {
      stem: imprintPillar.stem,
      branch: imprintPillar.branch,
      gan_zhi: imprintPillar.gan_zhi,
      stem_en: stemEnglish(imprintPillar.stem),
      branch_en: branchAnimal(imprintPillar.branch),
      stem_element: imprintPillar.stem_element || "",
    };
  }
  const gz = pillar?.gan_zhi || "—";
  return `<div class="pillar-compare-row"><span class="pillar-compare-label">${label}</span><span class="pillar-compare-val">${pillar ? pillarSymbolLine(pillar) : "—"} <span class="hanzi">${gz}</span></span></div>`;
}

/** Favorability tier → bar color class (terrible/black … very-good/gold) */
function favorabilityFromPayload(payload) {
  const tier = payload?.scores?.tier || payload?.bazi?.favorability_tier;
  const score = payload?.scores?.favorability ?? 0.5;
  const clashes = payload?.bazi?.clashes?.length > 0;
  if (tier) return tier;
  if (clashes) return "terrible";
  if (score >= 0.82) return "very-good";
  if (score >= 0.62) return "good";
  if (score >= 0.45) return "neutral";
  if (score >= 0.28) return "bad";
  return "terrible";
}

const BRANCH_CHONG_PAIRS = new Set([
  "子午", "午子", "丑未", "未丑", "寅申", "申寅", "卯酉", "酉卯", "辰戌", "戌辰", "巳亥", "亥巳",
]);

function branchesClash(a, b) {
  if (!a || !b) return false;
  return BRANCH_CHONG_PAIRS.has(`${a}${b}`);
}

function baziElementRelation(a, b) {
  if (!a || !b) return "neutral";
  if (a === b) return "same";
  if (ELEMENT_GENERATES[a] === b) return "generates";
  if (ELEMENT_GENERATES[b] === a) return "generated_by";
  if (ELEMENT_CONTROLS[a] === b) return "controls";
  if (ELEMENT_CONTROLS[b] === a) return "controlled_by";
  return "neutral";
}

const TONE_FRICTION = {
  supportive: 0.06,
  neutral: 0.18,
  strained: 0.34,
  clash_muted: 0.38,
  clash_bruised: 0.52,
  clash_mixed: 0.64,
  clash_harsh: 0.78,
};

const STEM_ROOT_FRICTION = {
  same: 0.08,
  generates: 0.12,
  generated_by: 0.16,
  neutral: 0.3,
  controls: 0.38,
  controlled_by: 0.42,
};

function stemOverRootFrame(pillar) {
  const p = enrichPillarHidden(pillar);
  if (!p) return { pro: "", con: "", stem: "", rootEl: "", animal: "" };
  const stem = p.stem_element || "";
  const rootEl = p.hidden_stem_element || "";
  const animal = p.branch_en || branchAnimal(p.branch);
  const rel = baziElementRelation(stem, rootEl);
  const frames = {
    same: {
      pro: `${stem} stem echoes ${animal} root — clean resonance`,
      con: "echo chamber — blind spots repeat",
    },
    generates: {
      pro: `${stem} feeds the ${animal} root — outward element nourishes inner ground`,
      con: "over-giving drains the stem before the root answers",
    },
    generated_by: {
      pro: `${animal} root (${rootEl}) feeds ${stem} — hidden reserve backs the stem`,
      con: "waiting on the root instead of leading with the stem",
    },
    controls: {
      pro: `${stem} steadies ${rootEl} under ${animal} — structure holds the root`,
      con: "over-control — steamroll nuance the animal needs",
    },
    controlled_by: {
      pro: `${rootEl} root tempers ${stem} — ${animal} refines excess`,
      con: "inner friction if you fight the root's regulation",
    },
    neutral: {
      pro: `${stem} and ${rootEl} run parallel — ${animal} sets pace, not chemistry`,
      con: "no elemental tailwind — you supply the spark",
    },
  };
  const frame = frames[rel] || frames.neutral;
  return { pro: frame.pro, con: frame.con, stem, rootEl, animal, relation: rel };
}

function skyWeatherFromFriction(friction, ctx = {}) {
  const f = Math.max(0, Math.min(1, friction));
  const eclipse =
    f >= 0.82 &&
    (ctx.severeClash || ctx.clashCount > 0) &&
    (ctx.harshCompares >= 2 || (ctx.severeClash && ctx.clashCount > 0));
  if (eclipse) {
    return {
      weather: "Eclipse event",
      advice: "Defer bets",
      tier: "terrible",
      weatherClass: "eclipse",
    };
  }
  if (f <= 0.16) {
    return { weather: "Ideal weather", advice: "Act now", tier: "very-good", weatherClass: "ideal" };
  }
  if (f <= 0.28) {
    return { weather: "Clear skies", advice: "Move steady", tier: "good", weatherClass: "clear" };
  }
  if (f <= 0.4) {
    return { weather: "Overcast", advice: "Plan tight", tier: "good", weatherClass: "overcast" };
  }
  if (f <= 0.55) {
    return {
      weather: "Rough terrain",
      advice: "Go slow",
      tier: "neutral",
      weatherClass: "rough",
    };
  }
  if (f <= 0.68) {
    return {
      weather: "Potential rain",
      advice: "Pack patience",
      tier: "bad",
      weatherClass: "rain",
    };
  }
  if (f <= 0.82) {
    return {
      weather: "Thunder skies",
      advice: "Shelter early",
      tier: "bad",
      weatherClass: "thunder",
    };
  }
  return { weather: "Storm front", advice: "Hold still", tier: "terrible", weatherClass: "storm" };
}

/**
 * Universal sky friction — year stem (heavy) vs branch root, clashes compound.
 * Returns scale %, weather metaphor, and brief stem-over-root framing.
 */
function computeUniversalSkyWeather(payload) {
  const sky = payload?.bazi?.sky_pillars || {};
  const astro = payload?.bazi?.astrology_layer || {};
  const compares = astro.compares || {};
  const clashes = payload?.bazi?.clashes || [];
  const skyYear = sky.year || {};
  const skyDay = sky.day || {};

  const stemRoot = stemOverRootFrame(skyYear);
  const stemRootScore = STEM_ROOT_FRICTION[stemRoot.relation] ?? 0.3;

  let clashScore = 0.08;
  let harshCompares = 0;
  const compareKeys = ["day_vs_sky_day", "day_vs_sky_year", "day_vs_sky_month", "year_vs_sky_year"];
  compareKeys.forEach((key) => {
    const cmp = compares[key] || {};
    const tone = cmp.effective_tone || "neutral";
    clashScore += TONE_FRICTION[tone] ?? 0.18;
    if (tone === "clash_harsh" || tone === "clash_mixed") harshCompares += 1;
    if (cmp.branch_relation === "chong_冲") clashScore += 0.06;
  });

  if (astro.severe_clash) clashScore += 0.14;
  if (clashes.length) clashScore += 0.1;
  if (branchesClash(skyYear.branch, skyDay.branch)) clashScore += 0.07;
  if (astro.element_glitch_active) clashScore -= 0.05;

  const friction = Math.max(0.05, Math.min(0.98, stemRootScore * 0.58 + clashScore * 0.42));
  const pct = Math.round(friction * 100);
  const weather = skyWeatherFromFriction(friction, {
    severeClash: astro.severe_clash,
    clashCount: clashes.length,
    harshCompares,
  });

  const clashToken =
    weather.weatherClass === "eclipse"
      ? "Eclipse-level clash"
      : clashes.length
        ? clashes.join(" ")
        : astro.severe_clash
          ? "Branch clash live"
          : harshCompares > 0
            ? "Sky friction"
            : stemRoot.relation === "controlled_by" || stemRoot.relation === "controls"
              ? "Element strain"
              : "Calm pressure";

  return {
    friction,
    pct,
    tier: weather.tier,
    advice: weather.advice,
    weather: weather.weather,
    weatherClass: weather.weatherClass,
    stemRoot,
    pro: stemRoot.pro,
    con: stemRoot.con,
    clashToken,
    hasClash: clashes.length > 0 || astro.severe_clash || harshCompares > 0,
  };
}

const FAV_TIER_LABEL = {
  terrible: "Terrible — clash or drain",
  bad: "Bad — move slow",
  neutral: "Neutral — ordinary sky",
  good: "Good — workable flow",
  "very-good": "Very good — strong tailwind",
};

const ZODIAC_SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
];

function wholeSignHouse(ascendantSign, houseNum) {
  if (!ascendantSign) return "—";
  const start = ZODIAC_SIGNS.indexOf(ascendantSign);
  if (start < 0) return "—";
  return ZODIAC_SIGNS[(start + houseNum - 1) % 12];
}

/** Income house — sidereal Vedic 2nd (not tropical whole-sign). */
function sealHouse2(imprint) {
  return vedicHouse(imprint, 2);
}

function vedicHouse(imprint, num) {
  const row = (imprint.vedic?.houses || []).find((h) => h.house === num);
  if (!row) return { sign: "—", planets: [], theme: num === 2 ? "Wealth & values" : "Career & public path" };
  return {
    sign: row.sign,
    planets: row.planets || [],
    theme: num === 2 ? "Wealth & values (Vedic 2nd)" : "Career & public path (10th)",
  };
}