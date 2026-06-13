/** Dashboard rendering — overview always reconciled with server version. */

function elementClass(element) {
  const e = (element || "").toLowerCase();
  if (e.includes("wood")) return "element-wood";
  if (e.includes("fire")) return "element-fire";
  if (e.includes("earth")) return "element-earth";
  if (e.includes("metal")) return "element-metal";
  if (e.includes("water")) return "element-water";
  return "element-earth";
}

const WEALTH_HOUSE_STEPS = {
  Aries: ["Send one offer you would sign yourself.", "Track spend against your Vedic income sign — cut one impulse line."],
  Taurus: ["Move one asset or invoice today; slow is the edge.", "No comfort spend until the 10th-house task is visible."],
  Gemini: ["Close one revenue tab; pick a single stream.", "Publish or pitch once, then stop splitting focus."],
  Cancer: ["Feed home/nest revenue — meal, care, or shelter offer.", "Protect reserves; one family-linked cost only."],
  Leo: ["Put your name on one deliverable in public.", "Let applause wait until the invoice is sent."],
  Virgo: ["Ship a detail fix someone will pay for.", "Audit one line item before you scale anything."],
  Libra: ["Sign or counter-sign the fair deal today.", "Balance the books before you balance the room."],
  Scorpio: ["Move stalled money or cut the grudge cost.", "One leverage conversation — terms on paper."],
  Sagittarius: ["Teach or sell with proof attached.", "Book travel or growth spend only after ROI named."],
  Capricorn: ["One brick on the long career wall.", "Defer prestige buys until ops is funded."],
  Aquarius: ["Update a system that pays you back.", "Skip hype tools — one tested channel only."],
  Pisces: ["Set a boundary on sympathy spending.", "Price the creative/healing offer in writing."],
};

const RELATION_HOUSE_STEPS = {
  Aries: ["Say the direct need once; no chase games.", "Cool heat before replying to a trigger text."],
  Taurus: ["Show loyalty in matter — time, gift, or task.", "Don't buy peace; name the material ask."],
  Gemini: ["Listen fully, then one clear reply.", "No story-spinning — ask the plain question."],
  Cancer: ["Protect the nest; one boundary at home.", "Feed belonging, not fixing adults."],
  Leo: ["Praise must be mutual — share the stage.", "Reject drama that steals your dignity."],
  Virgo: ["Offer help as craft, not critique.", "Repair with one kind act, not a lecture."],
  Libra: ["Speak the fair sentence you've delayed.", "Document the agreement — charm isn't contract."],
  Scorpio: ["Full truth in one vault; no tests.", "Release resentment or name the exit."],
  Sagittarius: ["Promise only what you'll calendar.", "Give freedom with a check-in date."],
  Capricorn: ["Respect time — yours and theirs.", "Love through reliability, not grand gestures."],
  Aquarius: ["Friendship first — space plus check-in.", "Don't intellectualize away feeling."],
  Pisces: ["Clarity beats fog — write the no.", "Solitude after absorbing others' moods."],
};

const DAILY_PILLAR_STEPS = {
  Wood: ["Morning: one growth metric with a deadline.", "Evening: prune one dead project line."],
  Fire: ["Morning: one pitch or publish.", "Evening: rest — no heat arguments."],
  Earth: ["Morning: invoice, meal prep, or property tick.", "Evening: sleep on time; no revenge spend."],
  Metal: ["Morning: one contract read or cut.", "Evening: declutter one physical drawer."],
  Water: ["Morning: research block before deciding.", "Evening: walk before replying."],
};

function pillarShort(pillar) {
  if (!pillar) return "—";
  const animal = branchAnimal(pillar.branch);
  return `${stemEnglish(pillar.stem)} ${animal}`;
}

function westernPlanetsSkyHtml(payload, imp) {
  // Used only in Western lens for Today's Energy. Shows tropical planets for the day + minimal timing note.
  const w = (payload && payload.western) || {};
  const today = w.planets_today || {};
  const natalW = (imp && imp.western && imp.western.planets) || {};
  const keys = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Saturn"];
  const rows = [];
  keys.forEach((k) => {
    const t = today[k];
    if (!t || !t.sign) return;
    const n = natalW[k] || {};
    const vs = (n.sign && n.sign !== t.sign) ? ` <span class="relation-badge relation-badge--neutral">vs natal ${n.sign}</span>` : "";
    rows.push(`<div class="bazi-energy-row"><span class="bazi-energy-label">${k}</span><span class="bazi-energy-val">${t.sign} ${t.degree != null ? t.degree + "°" : ""}${vs}</span></div>`);
  });
  if (!rows.length) {
    // graceful fallback if no planets_today in payload yet
    const ns = w.natal_sun || (natalW.Sun && natalW.Sun.sign) || "—";
    rows.push(`<div class="bazi-energy-row"><span class="bazi-energy-label">Sun (natal)</span><span class="bazi-energy-val">${ns}</span></div>`);
  }
  // Simple hermetic/planet timing note (no new backend data required)
  const moon = today.Moon || {};
  const timingNote = moon.sign
    ? `Moon in ${moon.sign} — emotional timing & pace for the day.`
    : "Planetary positions set the Western timing frame.";
  return `${rows.join("")}<div class="sky-friction-block" style="margin-top:0.15rem"><p class="sky-element-advice" style="font-size:0.62rem;margin:0.15rem 0 0;">${timingNote}</p></div>`;
}

function chaldeanHermeticTimingHtml(payload, imp) {
  // When Chaldean Astrology lens is selected: replace Bazi insight (sky friction / Eastern Zodiac pillars advice)
  // with Chaldean + Hermetic timing. Keep numerology in the left cell.
  // Pros/cons in footer will be annotated as measured against Chaldean principles.
  const ch = (imp && imp.numerology && imp.numerology.schools && imp.numerology.schools.chaldean) || {};
  const chExpr = ch.expression ? numerologyDisplay(ch.expression) : "—";
  const chBday = ch.birthday ? numerologyDisplay(ch.birthday) : "—";

  let html = `
    <div class="bazi-energy-row"><span class="bazi-energy-label">Chaldean</span><span class="bazi-energy-val">Vibration <strong>${chExpr}</strong></span></div>
    <div class="bazi-energy-row"><span class="bazi-energy-label">Chaldean day</span><span class="bazi-energy-val">Key <strong>${chBday}</strong></span></div>
  `;

  // Hermetic timing insight using available western planets_today (tropical) for the day.
  const w = (payload && payload.western) || {};
  const today = w.planets_today || {};
  const keyPlanets = ["Sun", "Moon", "Mercury", "Saturn"];
  const hermRows = [];
  keyPlanets.forEach((k) => {
    const t = today[k];
    if (t && t.sign) {
      hermRows.push(`<div class="bazi-energy-row"><span class="bazi-energy-label">Hermetic ${k}</span><span class="bazi-energy-val">${t.sign}${t.degree != null ? " " + t.degree + "°" : ""}</span></div>`);
    }
  });

  if (hermRows.length) {
    html += hermRows.join("");
  } else {
    html += `<div class="bazi-energy-row"><span class="bazi-energy-label">Hermetic</span><span class="bazi-energy-val">Timing via planetary positions</span></div>`;
  }

  html += `<div class="sky-friction-block" style="margin-top:0.2rem"><p class="sky-element-advice" style="font-size:0.62rem;margin:0.1rem 0 0;">Chaldean principles guide the vibration. Hermetic timing: act when the current planetary signs support your name number. Pro's and cons below are measured against Chaldean Astrology principles and Hermetic timing.</p></div>`;

  return html;
}

function buildChaldeanPromote(imp, payload) {
  // Chaldean Astrology focused promote for timing (used when lens under Refresh is Chaldean).
  // Based on Chaldean name vibration + Hermetic planetary timing (no Bazi language).
  const ch = (imp && imp.numerology && imp.numerology.schools && imp.numerology.schools.chaldean) || {};
  const chExpr = ch.expression ? numerologyDisplay(ch.expression) : "your key";
  const chBday = ch.birthday ? numerologyDisplay(ch.birthday) : chExpr;
  const w = (payload && payload.western) || {};
  const today = w.planets_today || {};
  const moon = today.Moon || {};
  const merc = today.Mercury || {};
  const items = [
    `Time one key action to your Chaldean ${chBday} vibration today — align with current Moon in ${moon.sign || "supportive sign"} for best results.`,
    `Use your Chaldean expression ${chExpr} for offers or communications; Hermetic Mercury in ${merc.sign || "favorable position"} favors clear timing.`,
    `Make a decision that matches your Chaldean day vibration — Hermetic timing supports building lasting structure now.`
  ];
  return items;
}

function buildChaldeanAvoid(imp, payload) {
  const ch = (imp && imp.numerology && imp.numerology.schools && imp.numerology.schools.chaldean) || {};
  const chExpr = ch.expression ? numerologyDisplay(ch.expression) : "your vibration";
  const chBday = ch.birthday ? numerologyDisplay(ch.birthday) : chExpr;
  const w = (payload && payload.western) || {};
  const today = w.planets_today || {};
  const moon = today.Moon || {};
  const items = [
    `Do not force timing against your Chaldean ${chBday} — if the vibration number resists, wait for better Hermetic alignment.`,
    `Avoid communications or deals that clash with your Chaldean expression ${chExpr}; current Moon in ${moon.sign || "this position"} warns against it.`,
    `Skip actions that ignore the day's Chaldean key — follow the Hermetic planets for the correct timing now.`
  ];
  return items;
}

function numerologyCycles(imprint) {
  return imprint?.numerology?.cycles?.reference_today || {};
}

function renderYearTotem(imprint) {
  const el = document.getElementById("year-totem");
  if (!el) return;
  const yz = yearZodiacFromImprint(imprint);
  const year = imprint?.bazi?.pillars?.year;
  const animal = yz.animal;
  const element = yz.stem_element;
  const animalKey = {
    Rat: "rat", Ox: "ox", Tiger: "tiger", Rabbit: "rabbit",
    Dragon: "dragon", Snake: "snake", Horse: "horse", Goat: "goat",
    Monkey: "monkey", Rooster: "rooster", Dog: "dog", Pig: "pig",
  }[animal] || "dragon";
  const svg = typeof TOTEM_SVGS !== "undefined" ? TOTEM_SVGS[animalKey] : "";
  el.className = `totem-wrap totem-wrap--outline ${elementClass(element)}`;
  el.innerHTML = `
    <div class="totem-glow" aria-hidden="true"></div>
    <div class="totem-ring" aria-hidden="true"></div>
    <div class="totem-animal">${svg}</div>
    <span class="totem-being">${yz.label}</span>
  `;
}

function houseKey(num, house) {
  return `<li>${num}th house · ${signGlyph(house.sign)} ${house.sign}</li>`;
}

function pillarKey(label, pillar) {
  if (!pillar) return `<li>${label} · —</li>`;
  const gz = pillar.gan_zhi || `${pillar.stem || ""}${pillar.branch || ""}`;
  const yearStyle = /year pillar/i.test(label);
  const identity = pillarIdentityLabel(pillar, { yearStyle });
  return `<li class="seal-pillar-key">${label} · <strong>${identity}</strong> ${pillarHiddenRow(pillar)} <span class="hanzi">${gz}</span></li>`;
}

function wealthAdvice(imprint) {
  const h2 = vedicHouse(imprint, 2).sign;
  const h10 = vedicHouse(imprint, 10).sign;
  const steps = WEALTH_HOUSE_STEPS[h10] || WEALTH_HOUSE_STEPS[h2];
  if (steps) return steps;
  const el = imprint.bazi.day_master.element;
  return DAILY_PILLAR_STEPS[el] || [
    "Name one income action from your Vedic 2nd sign.",
    "Place one 10th-house win where your reputation can see it.",
  ];
}

function relationshipAdvice(imprint) {
  const h7 = vedicHouse(imprint, 7).sign;
  const h4 = vedicHouse(imprint, 4).sign;
  const yearAn = branchAnimal(imprint.bazi.pillars.year.branch);
  const dayAn = branchAnimal(imprint.bazi.pillars.day.branch);
  const steps = [...(RELATION_HOUSE_STEPS[h7] || RELATION_HOUSE_STEPS[h4] || [])];
  if (yearAn !== dayAn && steps.length > 1) {
    steps[1] = `Year ${yearAn} / day ${dayAn}: say the need plainly — no performance.`;
  } else if (yearAn !== dayAn) {
    steps.push(`Year ${yearAn} / day ${dayAn}: say the need plainly — no performance.`);
  }
  if (steps.length >= 2) return steps.slice(0, 2);
  return [
    "State one boundary the 7th house would call fair.",
    "Honor lineage (4th) without carrying someone else's unfinished story.",
  ];
}

function dailyAdvice(imprint) {
  const day = imprint.bazi.pillars.day;
  const hour = imprint.bazi.pillars.hour;
  const dm = imprint.bazi.day_master.element;
  const dayEl = day.stem_element || dm;
  const steps = [...(DAILY_PILLAR_STEPS[dayEl] || DAILY_PILLAR_STEPS[dm] || DAILY_PILLAR_STEPS.Wood)];
  const hourAn = branchAnimal(hour?.branch);
  if (hourAn) {
    steps[0] = `${steps[0]} Hour ${hourAn}: guard evening rhythm.`;
  }
  return steps.slice(0, 2);
}

function dayPillarDmSealLabel(day, dm) {
  if (!day) return "—";
  const p = typeof enrichPillarHidden === "function" ? enrichPillarHidden(day) : day;
  const visible = (p.stem_element || dm?.element || "").toLowerCase();
  const animal = (p.branch_en || branchAnimal(p.branch) || "").toLowerCase();
  const hidden = (p.hidden_stem_element || "").toLowerCase();
  const pillarPart = hidden ? `${visible} ${animal} hidden ${hidden}` : `${visible} ${animal}`;
  const dmPart = dm
    ? `${(dm.yin_yang || "").toLowerCase()} ${(dm.element || "").toLowerCase()} day master`.trim()
    : "";
  return dmPart ? `${pillarPart} · ${dmPart}` : pillarPart;
}

function renderSealIdentity(imprint) {
  if (!imprint?.numerology?.schools?.pythagorean || !imprint?.bazi) return;
  const py = imprint.numerology.schools.pythagorean;
  const dm = imprint.bazi.day_master;
  const yz = yearZodiacFromImprint(imprint);
  const day = imprint.bazi.pillars?.day;
  const sun = imprint.western?.planets?.Sun?.sign || "—";
  const lp =
    typeof lifePathDisplay === "function" ? lifePathDisplay(imprint) : numerologyDisplay(py.life_path);
  const h2 = vedicHouse(imprint, 2);
  const labels = imprint.numerology_seal_labels || {};
  const born = labels.born_expression || {};
  const daily = labels.daily_walk || null;

  const compoundTitle = labels.compound_title || "—";
  const being = document.getElementById("seal-being-line");

  const lens = (typeof window !== "undefined" && typeof window.getOccultLens === "function")
    ? window.getOccultLens()
    : "eastern";
  const chaldeanMode = (typeof window !== "undefined" && typeof window.getChaldeanLens === "function")
    ? window.getChaldeanLens() === "chaldean"
    : false;
  if (being) {
    const compoundToken =
      compoundTitle && compoundTitle !== "—"
        ? ` · <button type="button" class="seal-title-chip seal-compound-token" data-compound-field="life_path" title="Life path compound — framework read">${compoundTitle}</button>`
        : "";
    if (chaldeanMode) {
      const ch = imprint.numerology && imprint.numerology.schools && imprint.numerology.schools.chaldean;
      const chExpr = ch && ch.expression ? numerologyDisplay(ch.expression) : lp;
      being.innerHTML =
        `Chaldean Astrology · vibration <strong>${chExpr}</strong> · path <strong>${lp}</strong>${compoundToken}`;
    } else if (lens === "western") {
      being.innerHTML =
        `Western <strong>${sun}</strong> (tropical) · <strong>${yz.label}</strong> year · path <strong>${lp}</strong>${compoundToken}`;
    } else {
      being.innerHTML =
        `A <strong>${yz.label}</strong> · <strong>${sun}</strong> · path <strong>${lp}</strong>${compoundToken}`;
    }
  }

  const numTitles = document.getElementById("seal-num-titles");
  if (numTitles) numTitles.innerHTML = "";

  const bornEl = document.getElementById("welcome-born-energy");
  if (bornEl) {
    if (chaldeanMode) {
      const ch = imprint.numerology && imprint.numerology.schools && imprint.numerology.schools.chaldean;
      const chExpr = ch && ch.expression ? numerologyDisplay(ch.expression) : (born.display || "—");
      bornEl.innerHTML = `Chaldean <strong>${chExpr}</strong>`;
      bornEl.classList.remove("hidden");
    } else if (born.display && born.display !== "—") {
      const bornTitle = born.title && born.title !== "—" 
        ? ` <button type="button" class="seal-title-chip seal-title-chip--inline seal-compound-token" data-compound-field="born_expression" title="Birth expression compound — framework read">${born.title}</button>` 
        : "";
      bornEl.innerHTML = `born <strong>${born.display}</strong>${bornTitle}`;
      bornEl.classList.remove("hidden");
    } else {
      bornEl.classList.add("hidden");
    }
  }

  const tags = document.getElementById("seal-core-tags");
  if (tags && day) {
    if (chaldeanMode) {
      // Chaldean Astrology lens for name field (user request: everything in name field becomes Chaldean focused)
      const ch = imprint.numerology && imprint.numerology.schools && imprint.numerology.schools.chaldean;
      const chExpr = ch && ch.expression ? numerologyDisplay(ch.expression) : "—";
      const chBday = ch && ch.birthday ? numerologyDisplay(ch.birthday) : "—";
      tags.innerHTML = `
        <span class="seal-tag">Chaldean Astrology</span>
        <span class="seal-tag">Expression <strong>${chExpr}</strong></span>
        <span class="seal-tag">Day vibration <strong>${chBday}</strong></span>
      `;
    } else if (lens === "western") {
      tags.innerHTML = `
        <span class="seal-tag">Western Sun · <strong>${sun}</strong></span>
        <span class="seal-tag">Vedic 2nd · <strong>${h2.sign}</strong></span>
      `;
    } else {
      tags.innerHTML = `
        <span class="seal-tag">Day pillar · <strong>${dayPillarDmSealLabel(day, dm)}</strong> <span class="hanzi">${day.gan_zhi || ""}</span></span>
        <span class="seal-tag">Vedic 2nd · <strong>${h2.sign}</strong></span>
      `;
    }
  }

  if (chaldeanMode) {
    // Replace Chinese zodiac totem with Chaldean Astrology display (no Eastern/Chinese animal image)
    const totemEl = document.getElementById("year-totem");
    if (totemEl) {
      const ch = imprint.numerology?.schools?.chaldean || {};
      const chDisp = ch.expression ? numerologyDisplay(ch.expression) : "—";
      totemEl.className = `totem-wrap totem-wrap--outline chaldean-totem`;
      totemEl.innerHTML = `
        <div class="totem-glow" aria-hidden="true"></div>
        <div class="totem-ring" aria-hidden="true"></div>
        <span class="totem-being">Chaldean<br>${chDisp}</span>
      `;
    }
  } else {
    renderYearTotem(imprint);
  }
  try {
    if (typeof renderSealStack === "function") renderSealStack(imprint);
  } catch (err) {
    console.error("renderSealStack", err);
  }
}

function formatDailyDateLabel(isoDate) {
  if (!isoDate) return "";
  const parts = String(isoDate).split("-");
  if (parts.length !== 3) return isoDate;
  const y = Number(parts[0]);
  const m = Number(parts[1]) - 1;
  const d = Number(parts[2]);
  const dt = new Date(y, m, d);
  if (Number.isNaN(dt.getTime())) return isoDate;
  return dt.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

function renderDailyChart(payload, imprintRef) {
  const grid = document.getElementById("daily-chart-grid");
  if (!grid || !payload) return;

  if (typeof window !== "undefined") window.occultLastDailyPayload = payload;

  const lens = (typeof window !== "undefined" && typeof window.getOccultLens === "function")
    ? window.getOccultLens()
    : "eastern";
  const chaldeanMode = (typeof window !== "undefined" && typeof window.getChaldeanLens === "function")
    ? window.getChaldeanLens() === "chaldean"
    : false;

  const imp =
    imprintRef ||
    (typeof window !== "undefined" && window.occultImprint) ||
    (typeof imprint !== "undefined" ? imprint : null);
  const baziEn = baziPillarEnglish(payload, imp);

  const skyFriction = payload.bazi?.sky_friction || {};
  const skyWeather =
    skyFriction.natal_line
      ? {
          pct: skyFriction.friction_pct ?? 50,
          tier: skyFriction.tier || favorabilityFromPayload(payload),
          advice: skyFriction.advice || "Lead with your core element today.",
          weather: skyFriction.weather || "Mixed sky",
          weatherClass: skyFriction.weather_class || "overcast",
          signal: skyFriction.signal || "Steady air",
          natalLine: skyFriction.natal_line,
          skyLine: skyFriction.sky_line,
          hasClash: skyFriction.has_clash || (payload.bazi?.clashes || []).length > 0,
        }
      : typeof computeUniversalSkyWeather === "function"
        ? computeUniversalSkyWeather(payload)
        : {
            pct: Math.round((1 - (payload.scores?.favorability ?? 0.5)) * 100),
            tier: favorabilityFromPayload(payload),
            advice: "Move steady",
            weather: "Overcast",
            weatherClass: "overcast",
            signal: "Steady air",
            hasClash: (payload.bazi?.clashes || []).length > 0,
          };
  const pd = payload.numerology?.personal_day;
  const uy = payload.numerology?.universal_year;
  const lpDay = payload.numerology?.life_path_day;
  const userLp = payload.numerology?.user_life_path;
  const numCompat = payload.numerology?.compat || {};
  const dayFieldPayload = payload.day_field || {};
  const lpVsLpd = numCompat.user_life_path_vs_life_path_day || {};
  const pdVsCal = numCompat.personal_day_vs_calendar_day || {};
  const lpGateRel = lpVsLpd.relation || dayFieldPayload.life_path_gate_relation || "neutral";
  const personalVsUnivRel =
    dayFieldPayload.personal_vs_universal_relation ||
    dayFieldPayload.personal_day_relation ||
    "neutral";
  const personalCalRel =
    dayFieldPayload.personal_vs_calendar_relation || pdVsCal.relation || dayFieldPayload.user_day_relation || "neutral";
  const numGateLine = payload.numerology?.gate_line || "";
  const dailyFraming = payload.daily_framing || {};
  const clashes = payload.bazi?.clashes || [];
  const saturn = payload.saturn_karma || {};
  const saturnTabLabel = saturn.tab_label || "Karmic Debt Insight · Saturn";
  const saturnModalTitle = saturn.modal_title || "Your karmic debt insight";
  const wealth = payload.wealth_chart || {};
  const relationships = payload.relationships_chart || {};
  const wealthClimate = wealth.year_climate || {};
  const wealthSky = wealthClimate.sky_year || {};
  const uyDisp = uy ? numerologyDisplay(uy) : universalYearDisplay(new Date().getFullYear());
  const pdDisp = pd ? numerologyDisplay(pd) : "—";
  const lpDayDisp =
    dayFieldPayload.life_path_day_display ||
    (lpDay ? numerologyDisplay(lpDay) : "—");
  const lpDayIsMaster = Boolean(
    dayFieldPayload.life_path_day_is_master ||
      dayFieldPayload.calendar_gate_is_master ||
      lpDay?.is_master ||
      payload.numerology?.calendar_day?.is_master ||
      lpVsLpd.life_path_day_is_master
  );
  const lpDayChipClass = lpDayIsMaster ? " flow-num-chip--master" : "";
  const pdPersonalDisp =
    dayFieldPayload.personal_day_display ||
    (pd ? numerologyDisplay(pd) : "—");
  const dailyDateLabel = formatDailyDateLabel(payload.date);
  const lpSealDisp =
    imp && typeof lifePathDisplay === "function"
      ? lifePathDisplay(imp)
      : userLp != null
        ? String(userLp)
        : "—";
  const dayFieldCompat = numCompat.day_field || {};
  const universalRel =
    dayFieldPayload.universal_relation ?? dayFieldCompat.relation ?? "neutral";
  const territoryRead =
    dayFieldPayload.territory_read ||
    dayFieldPayload.territory_lead ||
    dayFieldPayload.universal_interpretation ||
    "";
  const universalInterpretation = dayFieldPayload.universal_interpretation || "";
  const dayFieldPremiumTeaser =
    dayFieldPayload.premium_teaser ||
    "Seeker+ Daily Overlay — how your sealed life path, personal day, and natal sky compound or strain today's universal field. Premium — opening soon.";
  const lpGatePremiumTeaser =
    dayFieldPayload.life_path_gate_premium_teaser ||
    "Seeker+ — how your sealed life path meets today's universal day. Full gate read — premium, opening soon.";

  function relationToken(rel, title) {
    if (!rel) return "";
    const labels = { friend: "friendly", enemy: "foe", neutral: "neutral" };
    const label = labels[rel] || rel;
    const tip = title ? ` title="${String(title).replace(/"/g, "&quot;")}"` : "";
    return `<span class="relation-badge relation-badge--${rel}"${tip}>${label}</span>`;
  }

  const sky = payload.bazi?.sky_pillars || {};
  const astro = payload.bazi?.astrology_layer || {};
  const skyDisp = astro.sky || {};
  const natalDisp = astro.natal || {};
  const skyYear = sky.year || null;
  const skyMonth = sky.month || null;
  const skyDay = sky.day || {
    stem_en: baziEn.current?.split(" ")[0],
    branch_en: baziEn.current?.split(" ")[1],
    gan_zhi: payload.bazi?.current_day_pillar,
    stem: "",
    branch: "",
  };

  const natalYearPillar = imp?.bazi?.pillars?.year;
  const natalDayPillar = imp?.bazi?.pillars?.day;
  function baziEnergyRow(label, item) {
    if (!item) return "";
    const text =
      item.display_line || item.label || pillarDisplayLine(item) || pillarSymbolLine(item) || "—";
    return `<div class="bazi-energy-row"><span class="bazi-energy-label">${label}</span><span class="bazi-energy-val">${text}</span></div>`;
  }

  let promoteItems = dailyFraming.promote || [];
  let avoidItems = dailyFraming.avoid || [];
  if (chaldeanMode) {
    // Switch promote/avoid to Chaldean Astrology focused on timing (Hermetic + Chaldean vibration/number cycles), not Bazi/Eastern.
    promoteItems = buildChaldeanPromote(imp, payload);
    avoidItems = buildChaldeanAvoid(imp, payload);
  }
  const promoteK = chaldeanMode ? "Chaldean Promote (Timing)" : "Promote";
  const avoidK = chaldeanMode ? "Chaldean Avoid (Timing)" : "Avoid";
  const promoteHtml = promoteItems.length
    ? `<div class="daily-framing daily-framing--promote"><span class="daily-framing-k">${promoteK}</span><ul class="daily-promote">${promoteItems.map((p) => `<li>${p}</li>`).join("")}</ul></div>`
    : "";
  const avoidHtml = avoidItems.length
    ? `<div class="daily-framing daily-framing--avoid"><span class="daily-framing-k">${avoidK}</span><ul class="daily-avoid">${avoidItems.map((a) => `<li>${a}</li>`).join("")}</ul></div>`
    : "";

  const adviceClass =
    skyWeather.tier === "terrible" || skyWeather.tier === "bad"
      ? "sky-element-advice--bad"
      : skyWeather.tier === "neutral"
        ? "sky-element-advice--neutral"
        : "sky-element-advice--good";
  const elementLines =
    skyWeather.natalLine && skyWeather.skyLine
      ? `<p class="sky-element-row"><span class="sky-element-k">You</span> ${skyWeather.natalLine}</p>
            <p class="sky-element-row"><span class="sky-element-k">Sky</span> ${skyWeather.skyLine}</p>`
      : "";
  const signalLabel = skyWeather.signal || skyWeather.weather || "Steady air";
  const ritualsTokenHtml = `
            <div class="daily-rituals-slot daily-rituals-slot--sky">
              <button type="button" class="layer-token layer-token--square layer-token--rituals layer-token--locked seal-token seal-token--rituals" data-rituals-token title="Daily rituals — premium, locked">
                <span class="layer-token-name">Rituals</span>
                <span class="layer-token-lock">Seeker+ · locked</span>
              </button>
            </div>`;
  const skyFrictionBlock = `
          <div class="sky-friction-block">
            <div class="sky-friction-head">
              <span class="sky-friction-label">Sky friction</span>
              <span class="sky-weather-token sky-weather-token--${skyWeather.weatherClass}${skyWeather.hasClash ? " sky-weather-token--clash" : ""}">${signalLabel}</span>
            </div>
            ${elementLines}
            <p class="sky-element-advice ${adviceClass}">${skyWeather.advice}</p>
            <div class="sky-friction-scale fav-bar" title="${skyWeather.weather}">
              <div class="fav-fill fav-fill--${skyWeather.tier}" style="width:${skyWeather.pct}%"></div>
            </div>
            ${ritualsTokenHtml}
          </div>`;

  const chaldeanDayHtml = chaldeanMode
    ? (() => {
        const ch = imp && imp.numerology && imp.numerology.schools && imp.numerology.schools.chaldean;
        const chDay = ch && ch.birthday ? numerologyDisplay(ch.birthday) : pdPersonalDisp;
        return `<span class="flow-num-chip flow-num-chip--seal">Chaldean vibration <strong>${chDay}</strong></span>`;
      })()
    : `<span class="flow-num-chip flow-num-chip--seal">Your day <strong>${pdPersonalDisp}</strong>${relationToken(personalVsUnivRel)}</span>`;

  // When Chaldean lens active we completely replace the Bazi/Eastern Zodiac insight area (pillars + sky friction)
  // with Chaldean + Hermetic timing. The left Numbers cell keeps numerology (augmented).

  grid.className = "chart-grid chart-grid--seal-daily";
  grid.innerHTML = `
    <div class="chart-card chart-flow chart-flow-merged chart-flow--seal-daily">
      ${dailyDateLabel ? `<p class="daily-energy-date-line">${dailyDateLabel}</p>` : ""}
      <div class="daily-energy-board daily-energy-board--seal-square">
        <div class="daily-energy-cell daily-energy-cell--nums">
          <span class="daily-energy-cell-label">${chaldeanMode ? "Chaldean Numbers" : "Numbers"}</span>
          <div class="daily-energy-numbers">
            <div class="daily-num-stack">
              <div class="daily-universal-territory">
                <span class="flow-num-chip flow-num-chip--primary flow-num-chip--territory${lpDayChipClass}">Territory <strong>${lpDayDisp}</strong>${relationToken(universalRel)}</span>
                ${territoryRead ? `<p class="universal-territory-read">${territoryRead}</p>` : ""}
              </div>
              ${chaldeanDayHtml}
            </div>
            <span class="flow-num-chip">Universal year <strong>${uyDisp}</strong></span>
          </div>
        </div>
        <div class="daily-energy-cell daily-energy-cell--sky">
          <span class="daily-energy-cell-label">${chaldeanMode ? "Chaldean Astrology" : (lens === "western" ? "Planetary timing (tropical)" : "Universal sky (Eastern Zodiac)")}</span>
          <div class="daily-energy-sky">
            ${chaldeanMode ? chaldeanHermeticTimingHtml(payload, imp) : (lens === "western" ? westernPlanetsSkyHtml(payload, imp) : `
            ${baziEnergyRow("Year", skyDisp.year || { label: pillarSymbolLine(skyYear), gan_zhi: skyYear?.gan_zhi })}
            ${baziEnergyRow("Month", skyDisp.month || { label: pillarSymbolLine(skyMonth), gan_zhi: skyMonth?.gan_zhi })}
            ${baziEnergyRow("Day", skyDisp.day || { label: pillarSymbolLine(skyDay), gan_zhi: skyDay?.gan_zhi })}
            ${skyFrictionBlock}
            `)}
          </div>
        </div>
        <div class="daily-energy-day-field day-field-callout day-field-callout--${universalRel}">
          <span class="day-field-label">${chaldeanMode ? "Chaldean name cycles × territory" : (lens === "western" ? "Western lens · planets & timing" : `Calendar × territory ${relationToken(universalRel)}`)}</span>
          ${universalInterpretation ? `<p class="day-field-note">${universalInterpretation}</p>` : ""}
        </div>
      </div>
      <div class="daily-energy-footer">
        ${chaldeanMode 
          ? `<div class="daily-framing-wrap chaldean-framing"><div class="chaldean-framing-note">Pro's & cons measured against Chaldean Astrology principles (name vibrations & cycles) and Hermetic timing.</div>${promoteHtml}${avoidHtml}</div>`
          : `<div class="daily-framing-wrap">${promoteHtml}${avoidHtml}</div>`}
      </div>
    </div>
  `;

  if (typeof window !== "undefined") {
    window.occultDailySaturn = { saturn, saturnModalTitle, saturnTabLabel };
  }
  if (typeof renderSealLifeTokens === "function" && imp) {
    renderSealLifeTokens(imp);
  }
  grid.querySelector("[data-rituals-token]")?.addEventListener("click", () => {
    if (typeof openChartModal === "function") {
      openChartModal(
        "Rituals",
        `<p class="wealth-paywall-teaser">Daily ritual prescriptions matched to your seal and today's sky — <strong>Seeker+</strong> premium, opening soon.</p>`
      );
    }
  });
}

function bindDailySealedRead(buttonId, system, title) {
  const btn = document.getElementById(buttonId);
  if (!btn || btn.dataset.bound) return;
  btn.dataset.bound = "1";
  btn.addEventListener("click", () => {
    if (typeof openChartDeepRead === "function") {
      openChartDeepRead(system);
      return;
    }
    const modal = document.getElementById("chart-modal");
    const titleEl = document.getElementById("chart-modal-title");
    const bodyEl = document.getElementById("chart-modal-body");
    if (modal && titleEl && bodyEl) {
      titleEl.textContent = title;
      bodyEl.innerHTML = `<p class="status">Open your sealed chart to load the ${title} read.</p>`;
      modal.classList.remove("hidden");
    }
  });
}

function formatKarmicDebtModalBody(saturn) {
  if (!saturn?.insight) {
    return `<p class="status">Karmic debt insight not available for this chart. Load or refresh your daily reflection to surface it.</p>`;
  }

  let html = `<div class="karmic-debt-read">`;

  if (saturn.placement_label) {
    html += `<p class="karmic-intro"><strong>Your karmic debt focus:</strong> ${saturn.placement_label}. Saturn is the strict, patient teacher who withholds ease until the exact lesson is embodied. It doesn't punish — it applies steady pressure exactly where your chart is weakest, turning that pressure into lasting structure if you work with it.</p>`;
  }

  // Core layers expanded conversationally
  const layers = [
    { label: "Where the debt lands", key: "house_debt", explain: "This life territory is where the lesson keeps showing up until mastered. It's the arena Saturn uses to get your attention." },
    { label: "What Saturn teaches", key: "sign_lesson", explain: "The core curriculum. This is the attitude or skill Saturn demands you develop the hard way." },
    { label: "How the sign plays in", key: "zodiac_manifestation", explain: "The flavor and style of the pressure. The sign colors how the debt expresses itself in daily life." },
  ];

  layers.forEach((layer) => {
    const text = saturn[layer.key];
    if (text) {
      html += `<div class="karmic-layer"><h5>${layer.label}</h5><p class="karmic-layer-text">${text}</p><p class="karmic-layer-explain">${layer.explain}</p></div>`;
    }
  });

  if (saturn.insight) {
    html += `<div class="karmic-insight"><h5>The direct influence</h5><p>${saturn.insight}</p>`;
    html += `<p class="karmic-playout">How this plays out in real life: Saturn here creates repeating situations that feel like "this again?" — the same obstacle, the same person, the same internal block — until you stop dodging and start building the quality it wants. It feels heavy because it is heavy; the gift is that once integrated, that area of life becomes unusually solid and reliable.</p>`;
    html += `<p class="karmic-allegory">Simple allegory: Imagine Saturn as the old master blacksmith. He hands you raw iron (your chart weakness) and says "Hammer it straight or the sword will break in your hand when you need it most." In this sign and house, the iron is shaped by [the specific pressure above]. Meet it daily in small ways and the blade becomes unbreakable. Dodge it and every test just reheats the same flawed metal.</p></div>`;
  }

  if (saturn.numerology_karma_note) {
    html += `<div class="karmic-num"><h5>How your life path tunes this</h5><p>${saturn.numerology_karma_note}</p></div>`;
  }

  if (saturn.actions && saturn.actions.length) {
    html += `<div class="karmic-actions"><h5>Simple, actionable ways to work with it</h5><ul class="karmic-action-list">`;
    saturn.actions.forEach((a) => {
      html += `<li>${a} — do this one small version today and watch the pressure ease a notch.</li>`;
    });
    html += `</ul><p class="karmic-note">Saturn rewards consistency over drama. One deliberate act in the right direction compounds faster than big gestures that fizzle.</p></div>`;
  }

  html += `</div>`;
  return html;
}

if (typeof window !== "undefined") {
  window.formatKarmicDebtModalBody = formatKarmicDebtModalBody;
}

function bindKarmicDebtModal(saturn, title) {
  const btn = document.getElementById("karmic-debt-open");
  if (!btn || btn.dataset.bound) return;
  btn.dataset.bound = "1";
  btn.addEventListener("click", () => {
    const open =
      typeof openChartModal === "function"
        ? openChartModal
        : typeof window.openChartModal === "function"
          ? window.openChartModal
          : null;
    if (open) {
      open(title, formatKarmicDebtModalBody(saturn));
      return;
    }
    const modal = document.getElementById("chart-modal");
    const titleEl = document.getElementById("chart-modal-title");
    const bodyEl = document.getElementById("chart-modal-body");
    if (!modal || !titleEl || !bodyEl) return;
    titleEl.textContent = title;
    bodyEl.innerHTML = formatKarmicDebtModalBody(saturn);
    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("chart-modal-open");
  });
}

const PRIEST_CHART_FORMAT = "priest-chart";
const ZERO_READ_MARKER = "ZERO'S READ";

function overviewMetaLine(overview) {
  if (!overview) return "";
  const parts = [];
  if (overview.template_signature === "zero-overview") {
    parts.push("Zero combined read");
  } else if (overview.overview_format === PRIEST_CHART_FORMAT) {
    parts.push("sealed chart");
  }
  if (overview.ai_used && overview.model) {
    parts.push(overview.model);
  } else if (overview.ai_error) {
    parts.push(overview.ai_error);
  }
  if (overview.cached) parts.push("saved");
  else parts.push("new");
  if (overview.content_version) parts.push(`v${overview.content_version}`);
  if (overview.template_signature) {
    parts.push(overview.template_signature.split("-").pop());
  }
  if (overview.reading_kind === "threshold_seal") parts.push("threshold seal");
  return parts.join(" · ");
}

function renderChartAnchorStrip(facts) {
  const strip = document.getElementById("chart-anchor-strip");
  if (!strip || !facts?.chart_anchor) return;
  const a = facts.chart_anchor;
  const dm = a.day_master || facts.day_master;
  const day = a.day_pillar || {};
  strip.classList.remove("hidden");
  const dayPillar = a.day_pillar || day;
  const dayHidden = dayPillar.branch
    ? pillarHiddenRow(enrichPillarHidden({ ...dayPillar, branch_en: day.branch_animal || branchAnimal(dayPillar.branch) }))
    : "";
  strip.innerHTML = `
    <strong>Verified chart</strong> · Day master <span class="hanzi">${dm.hanzi || ""}</span>
    ${dm.english} (${dm.yin_yang} ${dm.element}) · Day ${dayHidden} <span class="hanzi">${day.gan_zhi || ""}</span>
    · Year 藏干 ${a.year_pillar?.branch ? pillarHiddenRow(enrichPillarHidden({ ...a.year_pillar, branch_en: a.year_zodiac_popular })) : a.year_zodiac_popular || ""}
    ${a.verified ? " · checks passed" : " · verify birth time"}
  `;
}

function formatZeroInsightModalBody(overview) {
  if (!overview) {
    return `<p class="status">Forging your threshold seal…</p>`;
  }
  const interp =
    overview.interpretation ||
    (overview.narrative || "").split("\n\n---\n\n")[1] ||
    overview.narrative ||
    overview.deterministic_fallback ||
    "";
  const text = interp || overview.interpretation || overview.narrative || "";
  const meta = overviewMetaLine(overview);
  let narrative =
    text.includes("**Direct Answer**") && typeof window.formatZeroInsightNarrative === "function"
      ? window.formatZeroInsightNarrative(text)
      : typeof window.formatFlowNarrative === "function"
        ? window.formatFlowNarrative(text)
        : text;
  const paywall =
    `<p class="zero-paywall-teaser">Daily Matrix read — full sky overlay on your seal — premium access opening soon.</p>`;
  return `${meta ? `<p class="chart-modal-note">${meta}</p>` : ""}<div class="zero-overview-text">${narrative || "<p class=\"status\">No insight yet.</p>"}</div>${paywall}`;
}

async function openZeroInsightModal() {
  if (typeof window !== "undefined") window.openZeroInsightModal = openZeroInsightModal;
  const title = "Full Read";
  const open =
    typeof openChartModal === "function"
      ? openChartModal
      : typeof window.openChartModal === "function"
        ? window.openChartModal
        : null;
  if (!open) return;
  open(title, formatZeroInsightModalBody(window.occultOverviewCache));
  let overview = typeof window !== "undefined" ? window.occultOverviewCache : null;
  const hasText =
    overview?.interpretation ||
    overview?.narrative ||
    overview?.deterministic_fallback;
  if (!hasText && typeof loadImprintOverview === "function" && typeof window.apiFetch === "function") {
    await loadImprintOverview(window.apiFetch);
    overview = window.occultOverviewCache;
    open(title, formatZeroInsightModalBody(overview));
  }
}

function renderOverview(overview) {
  const article = document.getElementById("overview-narrative");
  const meta = document.getElementById("overview-meta");
  if (!article) return;
  if (!overview) {
    if (meta) meta.textContent = "No overview yet";
    article.textContent = "";
    return;
  }
  if (typeof window !== "undefined" && overview?.facts) {
    window.occultOverviewFacts = overview.facts;
    renderChartAnchorStrip(overview.facts);
  }
  if (meta) meta.textContent = overviewMetaLine(overview);

  const interp =
    overview.interpretation ||
    (overview.narrative || "").split("\n\n---\n\n")[1] ||
    overview.narrative ||
    overview.deterministic_fallback ||
    "";

  const text = interp || overview.interpretation || overview.narrative || "";
  if (text.includes("**Direct Answer**") && typeof window.formatZeroInsightNarrative === "function") {
    article.innerHTML = window.formatZeroInsightNarrative(text);
  } else if (typeof window.formatFlowNarrative === "function") {
    article.innerHTML = window.formatFlowNarrative(text);
  } else {
    article.textContent = text;
  }
}

const THRESHOLD_READING_MARKER = "take the blade";

async function fetchOverviewRelease(apiFetch) {
  try {
    const res = await apiFetch("/imprint/overview/version");
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

function overviewNeedsRegenerate(release, cachedOverview, forceRefresh) {
  if (forceRefresh) return true;
  if (!release) return true;
  const storedVer = sessionStorage.getItem("occult_overview_version");
  const storedSig = sessionStorage.getItem("occult_overview_signature");
  if (String(release.content_version) !== storedVer) return true;
  if (release.template_signature && release.template_signature !== storedSig) {
    return true;
  }
  const interp =
    cachedOverview?.interpretation ||
    (cachedOverview?.narrative || "").split("\n\n---\n\n")[1] ||
    cachedOverview?.narrative ||
    "";
  const low = interp.toLowerCase();
  if (!low.includes("you are") && !low.includes("you're")) return true;
  if (!low.includes(THRESHOLD_READING_MARKER)) return true;
  if (release?.reading_engine && cachedOverview?.reading_engine !== release.reading_engine) {
    return true;
  }
  if (/PICTURE THIS|ZERO'S READ|THE SCENE|WALK THIS NOW|THE INITIATION|THE SKY PRESSED|book report|Act I|look up|investigate/i.test(interp)) {
    return true;
  }
  const words = interp.split(/\s+/).filter(Boolean).length;
  if (words > 900 || words < 80) return true;
  return false;
}

async function loadImprintOverview(apiFetch, options = {}) {
  const article = document.getElementById("overview-narrative");
  const meta = document.getElementById("overview-meta");
  if (!article) return;

  const forceRefresh = options.force === true;
  const release = await fetchOverviewRelease(apiFetch);
  const cached =
    typeof window !== "undefined" ? window.occultOverviewCache : null;
  const needsRefresh = overviewNeedsRegenerate(release, cached, forceRefresh);

  if (meta) meta.textContent = "Forging your threshold seal…";
  article.textContent = "";

  try {
    const q = needsRefresh ? "?refresh=true" : "";
    const bust = `_=${Date.now()}`;
    const path = `/imprint/overview/me${q}${q ? "&" : "?"}${bust}`;
    const res = await apiFetch(path);
    const text = await res.text();
    let data = {};
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { detail: text || res.statusText };
    }
    if (!res.ok) {
      throw new Error(
        typeof data.detail === "string" ? data.detail : res.statusText
      );
    }
    if (!data.narrative?.includes(THRESHOLD_READING_MARKER) && !forceRefresh) {
      const retry = await apiFetch(
        `/imprint/overview/me?refresh=true&_=${Date.now()}`
      );
      const retryText = await retry.text();
      const retryData = retryText ? JSON.parse(retryText) : {};
      if (retry.ok) data = retryData;
    }
    if (typeof window !== "undefined") {
      window.occultOverviewCache = data;
      if (data.content_version) {
        sessionStorage.setItem(
          "occult_overview_version",
          String(data.content_version)
        );
      } else if (release?.content_version) {
        sessionStorage.setItem(
          "occult_overview_version",
          String(release.content_version)
        );
      }
      const sig = data.template_signature || release?.template_signature;
      if (sig) sessionStorage.setItem("occult_overview_signature", sig);
    }
    renderOverview(data);
    if (typeof renderSealIdentity === "function" && window.occultImprint) {
      renderSealIdentity(window.occultImprint);
    }
  } catch (err) {
    if (meta) meta.textContent = "Overview unavailable";
    article.textContent =
      err.message === "Not Found"
        ? "Restart the backend, then hard-refresh (Ctrl+F5)."
        : err.message || "Could not load overview.";
  }
}

function renderDashboard(imprint) {
  const name = imprint.birth?.name || imprint.birth?.display_name || "Seeker";
  const alias = (imprint.birth?.commonly_known_as || "").trim();
  const daily = imprint.numerology_seal_labels?.daily_walk;
  const welcome = document.getElementById("welcome-name");
  const aliasEl = document.getElementById("welcome-alias");
  if (welcome) welcome.textContent = name;

  const chaldeanMode = (typeof window !== "undefined" && typeof window.getChaldeanLens === "function")
    ? window.getChaldeanLens() === "chaldean"
    : false;

  if (aliasEl) {
    if (alias) {
      if (chaldeanMode) {
        const ch = imprint.numerology && imprint.numerology.schools && imprint.numerology.schools.chaldean;
        const chExpr = ch && ch.expression ? numerologyDisplay(ch.expression) : (daily && daily.display) || "—";
        aliasEl.innerHTML = `Chaldean name: <strong>${alias}</strong> · vibration <strong>${chExpr}</strong>`;
      } else {
        const walk =
          daily?.display && daily.display !== "—"
            ? ` · walks <strong>${daily.display}</strong>${daily.title ? ` <button type="button" class="seal-title-chip seal-title-chip--inline seal-compound-token" data-compound-field="daily_walk" title="Expression compound — framework read">${daily.title}</button>` : ""}`
            : "";
        aliasEl.innerHTML = `or: ${alias}${walk}`;
      }
      aliasEl.classList.remove("hidden");
    } else {
      aliasEl.textContent = "";
      aliasEl.classList.add("hidden");
    }
  }
  if (typeof window !== "undefined") window.occultImprint = imprint;
  renderSealIdentity(imprint);
}