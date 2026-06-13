const TOKEN_KEY = "occult_access_token";
const USER_KEY = "occult_user_id";
const PREVIEW_IMPRINT_KEY = "occult_preview_imprint";
const PREVIEW_BODY_KEY = "occult_pending_seal";

const form = document.getElementById("seal-form");
const statusEl = document.getElementById("status");

const landingSection = document.getElementById("landing");
const wizardSection = document.getElementById("wizard");
const authUserEl = document.getElementById("auth-user");
const signOutBtn = document.getElementById("sign-out");
const previewSealBanner = document.getElementById("preview-seal-banner");
const sealModal = document.getElementById("seal-modal");
const sealAccountForm = document.getElementById("seal-account-form");
const sealModalStatus = document.getElementById("seal-modal-status");

let imprint = null;
let imprintOverview = null;
let userId = null;
let accessToken = null;
let previewMode = false;
let pendingSealBody = null;

function formatApiError(detail, status) {
  if (status === 404 && (detail === "Not Found" || detail === "not found")) {
    return "Auth API not available — restart the backend server (uvicorn) and hard-refresh this page.";
  }
  if (!detail) {
    if (status === 500) return "Server error — try again in a moment, or sign out and back in.";
    return "Request failed";
  }
  const text =
    typeof detail === "string"
      ? detail
      : Array.isArray(detail)
        ? detail.map((item) => item.msg || item.message || JSON.stringify(item)).join("; ")
        : String(detail);
  if (text === "Email already registered") {
    return "That email already has an account — sign in instead, or sign in and use Delete account to reuse this email.";
  }
  if (text.includes("already have a sealed imprint")) {
    return "This account already has a chart — sign in to view it, or use Reset chart to enter new birth data.";
  }
  if (text.includes("birth fingerprint already exists")) {
    return "That exact birth chart is already sealed on another account — sign in to that account, or use a new email.";
  }
  if (text === "Internal Server Error" || status === 500) {
    return "Server error while loading your chart — try Refresh, or Reset chart if you were entering a new birth story.";
  }
  return text;
}

async function parseResponse(res) {
  const text = await res.text();
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch {
    return { detail: text || res.statusText };
  }
}

function getToken() {
  return accessToken || localStorage.getItem(TOKEN_KEY);
}

function setSession(token, uid) {
  accessToken = token;
  userId = uid;
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, uid);
}

function clearSession() {
  accessToken = null;
  userId = null;
  imprint = null;
  imprintOverview = null;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  if (typeof window !== "undefined") {
    window.occultImprint = null;
    window.occultChartReadings = null;
  }
  if (typeof chartReadingCache !== "undefined") {
    Object.keys(chartReadingCache).forEach((k) => delete chartReadingCache[k]);
  }
}

function handleSessionExpired(detail) {
  clearSession();
  if (restorePreviewFromStorage()) {
    showStatusError(detail || "Session expired — preview restored.");
    return;
  }
  showLanding();
  showStatusError(detail || "Session expired — enter your story again.");
}

async function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(path, { ...options, headers });
  if (res.status === 401 && token) {
    const data = await parseResponse(res.clone());
    const detail = formatApiError(data.detail, res.status);
    if (
      detail.includes("Session expired") ||
      detail.includes("User not found") ||
      detail.includes("Invalid or expired token") ||
      detail.includes("Not authenticated")
    ) {
      handleSessionExpired(detail);
    }
  }
  return res;
}

function storeChartReadings(readings) {
  if (typeof window !== "undefined") {
    window.occultChartReadings = readings || null;
  }
  if (!readings || typeof chartReadingCache === "undefined") return;
  Object.entries(readings).forEach(([system, payload]) => {
    chartReadingCache[system] = payload;
  });
}

function setGateActive(on) {
  document.body.classList.toggle("gate-active", !!on);
}

function showLanding() {
  landingSection?.classList.remove("hidden");
  wizardSection?.classList.add("hidden");
  document.getElementById("dashboard")?.classList.add("hidden");
  previewSealBanner?.classList.add("hidden");
  authUserEl?.classList.add("hidden");
  document.getElementById("account-tools")?.classList.add("hidden");
  setGateActive(true);
}

function showWizard() {
  landingSection?.classList.add("hidden");
  wizardSection?.classList.remove("hidden");
  document.getElementById("dashboard")?.classList.add("hidden");
  previewSealBanner?.classList.add("hidden");
  authUserEl?.classList.add("hidden");
  document.getElementById("account-tools")?.classList.add("hidden");
  setGateActive(false);
}

function showDashboard() {
  landingSection?.classList.add("hidden");
  wizardSection?.classList.add("hidden");
  document.getElementById("dashboard")?.classList.remove("hidden");
  previewSealBanner?.classList.toggle("hidden", !previewMode);
  authUserEl?.classList.toggle("hidden", previewMode);
  document.getElementById("account-tools")?.classList.toggle("hidden", previewMode);
  setGateActive(false);
  if (typeof window !== "undefined") {
    window.occultImprint = imprint;
    window.apiFetch = previewMode ? null : apiFetch;
  }
  // Lens inits FIRST so window.get* functions and token label are ready before any name/daily renders pick up the current state (eastern/chaldean/western).
  // This ensures the token under Refresh is always present and functional, and first paint uses the stored lens.
  initLensToggle();
  initDailyLensToken();
  if (imprint && typeof renderDashboard === "function") {
    renderDashboard(imprint);
  }
  if (imprint && typeof renderChartForge === "function") {
    renderChartForge(imprint, previewMode ? null : apiFetch);
  }
  if (!previewMode && typeof loadImprintOverview === "function") {
    loadImprintOverview(apiFetch);
  }
  loadDailyReflection();
}

function storePreview(imprintData, sealBody, chartReadings) {
  previewMode = true;
  pendingSealBody = sealBody;
  imprint = imprintData;
  sessionStorage.setItem(PREVIEW_IMPRINT_KEY, JSON.stringify(imprintData));
  sessionStorage.setItem(PREVIEW_BODY_KEY, JSON.stringify(sealBody));
  storeChartReadings(chartReadings);
  if (typeof window !== "undefined") {
    window.occultImprint = imprint;
  }
  // Populate Full Read (combination/zero insight) for preview mode so the Zero Depth Full Read token launches with content
  if (chartReadings && chartReadings.combination) {
    const c = chartReadings.combination;
    window.occultOverviewCache = {
      narrative: c.narrative || c,
      interpretation: c.narrative || c,
      title: "Full Read",
    };
  }
}

function clearPreview() {
  previewMode = false;
  pendingSealBody = null;
  sessionStorage.removeItem(PREVIEW_IMPRINT_KEY);
  sessionStorage.removeItem(PREVIEW_BODY_KEY);
}

function restorePreviewFromStorage() {
  try {
    const rawImprint = sessionStorage.getItem(PREVIEW_IMPRINT_KEY);
    const rawBody = sessionStorage.getItem(PREVIEW_BODY_KEY);
    if (!rawImprint || !rawBody) return false;
    imprint = JSON.parse(rawImprint);
    pendingSealBody = JSON.parse(rawBody);
    previewMode = true;
    if (typeof window !== "undefined") window.occultImprint = imprint;
    showDashboard();
    return true;
  } catch {
    return false;
  }
}

function openSealModal() {
  if (!sealModal) return;
  sealModal.classList.remove("hidden");
  sealModal.setAttribute("aria-hidden", "false");
  if (sealModalStatus) {
    sealModalStatus.textContent = "";
    sealModalStatus.className = "status";
  }
}

function closeSealModal() {
  if (!sealModal) return;
  sealModal.classList.add("hidden");
  sealModal.setAttribute("aria-hidden", "true");
}

async function loadDailyReflection() {
  const meta = document.getElementById("daily-meta");
  const article = document.getElementById("daily-narrative");
  if (!meta || !article) return;
  if (!imprint) return;
  meta.textContent = "Loading today\u2019s reflection\u2026";
  article.textContent = "";
  try {
    let data;
    if (previewMode) {
      const res = await fetch("/reflection/daily/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imprint }),
      });
      data = await res.json();
      if (!res.ok) throw new Error(data.detail || res.statusText);
    } else {
      if (!userId || !getToken()) return;
      const res = await apiFetch("/reflection/daily/me");
      data = await res.json();
      if (!res.ok) throw new Error(data.detail || res.statusText);
    }
    meta.textContent = `${data.local_date || data.payload?.date || ""}${data.cached ? " (cached)" : ""}${previewMode ? " · preview" : data.model ? ` \u00b7 ${data.model}` : ""}`;
    if (data.payload && typeof renderDailyChart === "function") {
      if (typeof window !== "undefined") window.occultLastDailyPayload = data.payload;
      renderDailyChart(data.payload, imprint);
    }
    // Ensure karmic debt data is available in preview for the Call box tokens
    if (previewMode && data.payload && data.payload.saturn_karma && typeof window !== "undefined") {
      const saturn = data.payload.saturn_karma;
      window.occultDailySaturn = {
        saturn: saturn,
        saturnModalTitle: saturn.modal_title || "Your karmic debt insight",
        saturnTabLabel: saturn.tab_label || "Open your karmic debt insight"
      };
    }
    const narrative = data.narrative || "";
    article.textContent = narrative;
    article.classList.toggle("hidden", !narrative);
  } catch (err) {
    meta.textContent = `Daily read: ${err.message}`;
  }
}

document.getElementById("load-daily")?.addEventListener("click", loadDailyReflection);

async function resetChart() {
  if (!getToken()) return;
  if (!window.confirm("Clear your sealed chart so you can enter new birth data? Your account stays.")) return;
  try {
    const res = await apiFetch("/account/reset-chart", { method: "POST" });
    const data = await parseResponse(res);
    if (!res.ok) throw new Error(formatApiError(data.detail, res.status) || res.statusText);
    imprint = null;
    imprintOverview = null;
    if (statusEl) {
      statusEl.textContent = data.message || "Chart cleared.";
      statusEl.className = "status success";
    }
    showWizard();
  } catch (err) {
    showStatusError(err.message);
  }
}

async function deleteAccount() {
  if (!getToken()) return;
  if (
    !window.confirm(
      "Delete this account and all chart data? You can register again with the same email."
    )
  ) {
    return;
  }
  try {
    const res = await apiFetch("/account/delete", { method: "POST" });
    const data = await parseResponse(res);
    if (!res.ok) throw new Error(formatApiError(data.detail, res.status) || res.statusText);
    clearSession();
    clearPreview();
    showLanding();
    showStatusError(data.message || "Account deleted.");
  } catch (err) {
    showStatusError(err.message);
  }
}

function scrollToWizard() {
  showWizard();
  wizardSection?.scrollIntoView({ behavior: "smooth", block: "start" });
  const nameInput = form?.querySelector('input[name="name"]');
  if (nameInput) window.setTimeout(() => nameInput.focus(), 450);
}

document.getElementById("landing-enter")?.addEventListener("click", scrollToWizard);

function bindSealModal() {
  document.getElementById("open-seal-modal")?.addEventListener("click", openSealModal);
  document.getElementById("seal-modal-close")?.addEventListener("click", closeSealModal);
  sealModal?.querySelector("[data-close-seal-modal]")?.addEventListener("click", closeSealModal);

  sealAccountForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!pendingSealBody) {
      if (sealModalStatus) {
        sealModalStatus.textContent = "Enter your birth story first.";
        sealModalStatus.className = "status error";
      }
      closeSealModal();
      showWizard();
      return;
    }
    const email = (sealAccountForm.querySelector('input[name="email"]')?.value || "").trim();
    const password = sealAccountForm.querySelector('input[name="password"]')?.value || "";
    if (!email || password.length < 8) {
      if (sealModalStatus) {
        sealModalStatus.textContent = "Enter email and an 8+ character password.";
        sealModalStatus.className = "status error";
      }
      return;
    }
    if (sealModalStatus) {
      sealModalStatus.className = "status";
      sealModalStatus.textContent = "Creating account and sealing chart\u2026";
    }
    try {
      const regRes = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const regData = await parseResponse(regRes);
      if (!regRes.ok) {
        throw new Error(formatApiError(regData.detail, regRes.status) || regRes.statusText);
      }
      setSession(regData.access_token, regData.user_id);
      const sealRes = await apiFetch("/imprint/seal", {
        method: "POST",
        body: JSON.stringify(pendingSealBody),
      });
      const sealData = await parseResponse(sealRes);
      if (!sealRes.ok) {
        throw new Error(formatApiError(sealData.detail, sealRes.status) || sealRes.statusText);
      }
      imprint = sealData.imprint;
      imprintOverview = sealData.overview || null;
      storeChartReadings(sealData.chart_readings);
      clearPreview();
      closeSealModal();
      if (authUserEl) authUserEl.textContent = email;
      showDashboard();
    } catch (err) {
      if (sealModalStatus) {
        sealModalStatus.textContent = err.message.startsWith("Error:") ? err.message : `Error: ${err.message}`;
        sealModalStatus.className = "status error";
      }
    }
  });
}

bindSealModal();

signOutBtn?.addEventListener("click", () => {
  clearSession();
  clearPreview();
  imprint = null;
  showLanding();
});

document.getElementById("reset-chart")?.addEventListener("click", resetChart);
document.getElementById("delete-account")?.addEventListener("click", deleteAccount);

function showStatusError(message) {
  const target = statusEl || sealModalStatus;
  if (target) {
    target.textContent = message.startsWith("Error:") ? message : `Error: ${message}`;
    target.className = "status error";
  }
}

const LENS_KEY = "occultLens";
function getOccultLens() {
  try {
    const v = localStorage.getItem(LENS_KEY);
    return (v === "western" || v === "eastern") ? v : "eastern";
  } catch {
    return "eastern";
  }
}
function setOccultLens(next) {
  try { localStorage.setItem(LENS_KEY, next === "western" ? "western" : "eastern"); } catch {}
  // notify for any listeners (renders read directly but token label sync uses this)
  if (typeof window !== "undefined") window.occultLens = next;
}

const CHALDEAN_LENS_KEY = "chaldeanLens";
function getChaldeanLens() {
  try {
    return localStorage.getItem(CHALDEAN_LENS_KEY) === "chaldean" ? "chaldean" : "eastern";
  } catch {
    return "eastern";
  }
}
function setChaldeanLens(next) {
  try {
    localStorage.setItem(CHALDEAN_LENS_KEY, next === "chaldean" ? "chaldean" : "eastern");
  } catch {}
  if (typeof window !== "undefined") window.chaldeanLens = next;
}

function initDailyLensToken() {
  const token = document.getElementById("daily-lens-token");
  if (!token || token.dataset.bound) return;
  token.dataset.bound = "1";

  function sync() {
    const mode = getChaldeanLens();
    if (mode === "chaldean") {
      token.textContent = "Eastern Rising";
      token.title = "Return to current Eastern (Bazi + Vedic + numerology) name field and Today's Energy";
    } else {
      token.textContent = "Chaldean Astrology";
      token.title = "Switch name field display and daily insights to Chaldean Astrology lens";
    }
  }

  token.addEventListener("click", () => {
    const cur = getChaldeanLens();
    const next = cur === "chaldean" ? "eastern" : "chaldean";
    setChaldeanLens(next);
    sync();

    // Only name field + Today's Energy framing change (per request). Re-render the two areas.
    const imp = (typeof window !== "undefined" && window.occultImprint) || imprint;
    if (imp && typeof renderSealIdentity === "function") {
      try { renderSealIdentity(imp); } catch {}
    }
    const lastP = (typeof window !== "undefined") ? window.occultLastDailyPayload : null;
    if (lastP && typeof renderDailyChart === "function") {
      try { renderDailyChart(lastP, imp); } catch {}
    }
  });

  sync();

  // Expose
  if (typeof window !== "undefined") {
    window.getChaldeanLens = getChaldeanLens;
    window.setChaldeanLens = setChaldeanLens;
  }
}

function initLensToggle() {
  const token = document.getElementById("lens-toggle-token");
  if (!token || token.dataset.lensBound) return;
  token.dataset.lensBound = "1";

  function syncLabel() {
    const lens = getOccultLens();
    token.textContent = lens === "western" ? "W" : "E";
    token.title = lens === "western" ? "Showing Western (tropical/hermetic/planet timing) — click for Eastern" : "Showing Eastern (current) — click for Western (planets, timing)";
  }

  token.addEventListener("click", () => {
    const cur = getOccultLens();
    const next = cur === "western" ? "eastern" : "western";
    setOccultLens(next);
    syncLabel();

    // Re-render ONLY name field bits + Today's Energy framing (per spec). Everything else untouched.
    const imp = (typeof window !== "undefined" && window.occultImprint) || imprint;
    if (imp && typeof renderSealIdentity === "function") {
      try { renderSealIdentity(imp); } catch (e) { /* no-op */ }
    }
    const lastP = (typeof window !== "undefined") ? window.occultLastDailyPayload : null;
    if (lastP && typeof renderDailyChart === "function") {
      try { renderDailyChart(lastP, imp); } catch (e) { /* no-op */ }
    }
  });

  // Initial label from stored (or default eastern)
  syncLabel();

  // Expose for zodiac.js renders (they call window.getOccultLens)
  if (typeof window !== "undefined") {
    window.getOccultLens = getOccultLens;
    window.setOccultLens = setOccultLens;
  }
}

async function afterAuth() {
  const meRes = await apiFetch("/auth/me");
  const me = await parseResponse(meRes);
  if (!meRes.ok) throw new Error(formatApiError(me.detail, meRes.status) || "Session invalid");
  userId = me.user_id;
  if (authUserEl) authUserEl.textContent = me.email;

  const res = await apiFetch("/imprint/me");
  if (res.ok) {
    const data = await parseResponse(res);
    imprint = data.imprint;
    imprintOverview = data.overview || null;
    storeChartReadings(data.chart_readings);
    clearPreview();
    showDashboard();
    return;
  }
  if (res.status !== 404) {
    const data = await parseResponse(res);
    throw new Error(formatApiError(data.detail, res.status) || res.statusText);
  }
  showWizard();
}

function sealBodyFromForm(fd) {
  const alias = (fd.get("commonly_known_as") || "").trim();
  return {
    name: fd.get("name"),
    commonly_known_as: alias || null,
    birth_datetime_local: `${fd.get("birth_date")}T${fd.get("birth_time")}:00`,
    place_of_birth: fd.get("place_of_birth"),
    gender: fd.get("gender") || "male",
  };
}

form?.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusEl.className = "status";
  statusEl.textContent = "Forging your imprint from Place of Birth\u2026";
  const body = sealBodyFromForm(new FormData(form));
  try {
    if (getToken() && !previewMode) {
      const res = await apiFetch("/imprint/seal", {
        method: "POST",
        body: JSON.stringify(body),
      });
      const data = await parseResponse(res);
      if (!res.ok) {
        const msg = formatApiError(data.detail, res.status) || res.statusText;
        if (res.status === 409 && msg.includes("already has a chart")) {
          statusEl.innerHTML = `${msg} <button type="button" class="btn-ghost btn-inline" id="seal-reset-chart">Reset chart</button>`;
          statusEl.className = "status error";
          document.getElementById("seal-reset-chart")?.addEventListener("click", resetChart);
          return;
        }
        throw new Error(msg);
      }
      imprint = data.imprint;
      imprintOverview = data.overview || null;
      storeChartReadings(data.chart_readings);
      userId = data.user_id;
      selectedChartSystem = null;
      statusEl.textContent = "Your story is entered.";
      statusEl.className = "status success";
      showDashboard();
      return;
    }

    const res = await fetch("/imprint/preview", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await parseResponse(res);
    if (!res.ok) {
      throw new Error(formatApiError(data.detail, res.status) || res.statusText);
    }
    storePreview(data.imprint, body, data.chart_readings);
    // In preview mode, hide the "Seeker+ · locked" indicators and remove locked class so tokens show full results without login prompt
    document.querySelectorAll('.layer-token-lock').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.layer-token--locked').forEach(el => el.classList.remove('layer-token--locked'));
    statusEl.textContent = "Chart preview ready — seal it to save.";
    statusEl.className = "status success";
    showDashboard();
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
    statusEl.className = "status error";
  }
});

(async () => {
  try {
    const res = await fetch("/health");
    if (res.ok) {
      const data = await res.json();
      const stamp = document.getElementById("build-stamp");
      if (stamp) {
        const label = data.frontend_build && data.frontend_build !== "unknown"
          ? data.frontend_build
          : data.deploy || "unknown";
        stamp.textContent = `build ${label}`;
        stamp.hidden = false;
      }
    }
  } catch {
    /* non-fatal */
  }

  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) {
    if (!restorePreviewFromStorage()) {
      showLanding();
    }
    return;
  }
  accessToken = token;
  userId = localStorage.getItem(USER_KEY);
  try {
    await afterAuth();
  } catch (err) {
    clearSession();
    if (!restorePreviewFromStorage()) {
      showLanding();
      showStatusError(err.message || "Session expired");
    }
  }
})();