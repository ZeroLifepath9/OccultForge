/** Minimal animal silhouettes for day-branch totem (64x64 viewBox). */
const TOTEM_SVGS = {
  rat: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M20 28c0-8 6-14 14-14 4 0 8 2 10 5l6-4 4 6-5 3c2 3 3 7 3 11 0 10-8 18-18 18s-18-8-18-18c0-4 1-8 4-11z M14 42c-2 0-4 2-4 5s2 5 4 5 4-2 4-5-2-5-4-5z M50 42c-2 0-4 2-4 5s2 5 4 5 4-2 4-5-2-5-4-5z"/></svg>`,
  ox: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M12 36c0-12 10-22 22-22h4c12 0 22 10 22 22v8H12v-8zm8 4h32v4c0 6-5 10-10 10H30c-5 0-10-4-10-10v-4zm10-18c-3 0-5 2-5 5v2h10v-2c0-3-2-5-5-5z"/></svg>`,
  tiger: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M10 32c0-14 12-26 26-26 8 0 15 3 20 9l-6 6c-3-4-8-6-14-6-10 0-18 8-18 18 0 2 0 4 1 6l-9-7zm44 8c4 0 8 4 8 10s-4 10-8 10H22c-4 0-8-4-8-10s4-10 8-10h32z"/></svg>`,
  rabbit: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M22 12c0-6 4-10 10-10s10 4 10 10v8l6 20H16L22 20V12zm6 4v4h8v-4c0-2-2-4-4-4s-4 2-4 4z"/></svg>`,
  dragon: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M8 40c0-16 14-28 30-28 6 0 12 2 16 5l-4 8c-3-2-7-3-12-3-12 0-22 8-22 18 0 4 1 8 4 10l-12-10zm40-6 8 4-6 14h-14l4-18z"/></svg>`,
  snake: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M40 10c8 0 14 6 14 14 0 6-4 11-10 13l8 22H18L26 37c-6-2-10-7-10-13 0-8 6-14 14-14zm0 8c-3 0-6 3-6 6s3 6 6 6 6-3 6-6-3-6-6-6z"/></svg>`,
  horse: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M14 44l6-24c2-8 10-14 18-14 6 0 12 4 14 10l8 28H14zm20-30c-4 0-8 3-9 7l-2 8h18l-4-14c-1-1-2-1-3-1z"/></svg>`,
  goat: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M20 14c0-6 4-10 10-10 3 0 6 1 8 4l6-6 4 6-5 4c2 2 3 5 3 8v22H14V26c0-4 2-8 6-12z M48 38h12v12H48V38z"/></svg>`,
  monkey: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M32 8c-12 0-22 10-22 22 0 8 4 15 10 19l-4 9h32l-4-9c6-4 10-11 10-19 0-12-10-22-22-22zm-12 18c-3 0-5 2-5 5s2 5 5 5 5-2 5-5-2-5-5-5zm24 0c-3 0-5 2-5 5s2 5 5 5 5-2 5-5-2-5-5-5z"/></svg>`,
  rooster: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M36 8l6 10h10L42 32l4 24H18l4-24L8 18h10l6-10zm-4 20c-6 0-10 4-10 10h20c0-6-4-10-10-10z"/></svg>`,
  dog: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M16 28c0-10 8-18 18-18 6 0 11 3 14 8l10-6 4 8-8 4c2 4 3 9 3 14 0 12-10 22-22 22S8 50 8 38c0-3 1-7 3-10l5-2z"/></svg>`,
  pig: `<svg class="totem-svg" viewBox="0 0 64 64" aria-hidden="true"><path fill="currentColor" d="M32 10c-14 0-26 12-26 26 0 12 8 22 20 24l-2 8h16l-2-8c12-2 20-12 20-24 0-14-12-26-26-26zm-8 22c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4zm16 0c-2 0-4 2-4 4s2 4 4 4 4-2 4-4-2-4-4-4z"/></svg>`,
};

/** Five-element icons (24x24) for chart symbol rows */
const ELEMENT_SVGS = {
  Wood: `<svg class="el-svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2C9 8 4 10 4 14c0 3 2 6 8 8 6-2 8-5 8-8 0-4-5-6-8-12z"/></svg>`,
  Fire: `<svg class="el-svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2c-2 4-6 6-6 10 0 4 3 8 6 10 3-2 6-6 6-10 0-4-4-6-6-10zm0 14c-2-2-3-4-3-6 0-2 1-3 3-5 2 2 3 3 3 5 0 2-1 4-3 6z"/></svg>`,
  Earth: `<svg class="el-svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 14h16v6H4v-6zm2-4 4-6 4 6 4 4H6l4-4z"/></svg>`,
  Metal: `<svg class="el-svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 18l8-14 8 14H4zm8-10-4 7h8l-4-7z"/></svg>`,
  Water: `<svg class="el-svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3c-3 5-7 7-7 11a7 7 0 1014 0c0-4-4-6-7-11z"/></svg>`,
};

const ANIMAL_TOTEM_KEY = {
  Rat: "rat", Ox: "ox", Tiger: "tiger", Rabbit: "rabbit",
  Dragon: "dragon", Snake: "snake", Horse: "horse", Goat: "goat",
  Monkey: "monkey", Rooster: "rooster", Dog: "dog", Pig: "pig",
};