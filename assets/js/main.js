/* ==========================================================================
   Hoërskool Dinamika — site behaviour
   No dependencies. Everything degrades gracefully without JavaScript
   (Afrikaans content is shown by default).
   ========================================================================== */

/* Contact form: paste a Formspree (or similar) endpoint here to receive
   submissions by e-mail, e.g. "https://formspree.io/f/abcdwxyz".
   Left empty, the form opens the visitor's e-mail app instead. */
const FORM_ENDPOINT = "";
const SCHOOL_EMAIL = "ontvangs@namies.co.za";

(function () {
  "use strict";

  const doc = document.documentElement;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const STORAGE_KEY = "dinamika-lang";
  const LANGS = ["af", "en"];

  doc.classList.add("js");

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  /** Bilingual inline markup — CSS shows the span that matches <html lang>. */
  const bi = (af, en) => `<span lang="af">${esc(af)}</span><span lang="en">${esc(en ?? af)}</span>`;
  const lang = () => (doc.lang === "en" ? "en" : "af");

  /* ---------------------------------------------------------------------
     Language
     ------------------------------------------------------------------ */
  let storageOk = true;
  function readPref() {
    const q = new URLSearchParams(location.search).get("lang");
    if (LANGS.includes(q)) return q;
    try { const v = localStorage.getItem(STORAGE_KEY); if (LANGS.includes(v)) return v; } catch (e) { storageOk = false; }
    return "af";
  }

  const ATTRS = ["alt", "placeholder", "aria-label", "title", "content"];
  function applyLang(root = document) {
    const l = lang();
    ATTRS.forEach((attr) => {
      $$(`[data-en-${attr}]`, root).forEach((el) => {
        if (!el.hasAttribute(`data-af-${attr}`)) el.setAttribute(`data-af-${attr}`, el.getAttribute(attr) || "");
        el.setAttribute(attr, el.getAttribute(`data-${l}-${attr}`));
      });
    });
    // Plain text swaps (used for <option> and <title>, which cannot hold spans)
    $$("[data-en]", root).forEach((el) => {
      if (!el.hasAttribute("data-af")) el.setAttribute("data-af", el.textContent);
      el.textContent = el.getAttribute(`data-${l}`);
    });
  }

  function setLang(l, persist = true) {
    if (!LANGS.includes(l)) l = "af";
    doc.lang = l;
    applyLang();
    $$(".lang-switch button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === l)));
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, l); } catch (e) { storageOk = false; }
    }
    // Without storage (e.g. strict private mode) carry the choice in links instead.
    if (!storageOk) {
      $$('a[href$=".html"], a[href*=".html#"], a[href*=".html?"]').forEach((a) => {
        const url = new URL(a.getAttribute("href"), location.href);
        if (url.origin !== location.origin && url.protocol !== "file:") return;
        url.searchParams.set("lang", l);
        a.href = url.href;
      });
    }
  }

  setLang(readPref(), true);
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".lang-switch button");
    if (!btn) return;
    setLang(btn.dataset.lang);
    const live = $("#lang-status");
    if (live) live.textContent = btn.dataset.lang === "en" ? "Language changed to English" : "Taal verander na Afrikaans";
  });

  /* ---------------------------------------------------------------------
     Header: scrolled state, back-to-top
     ------------------------------------------------------------------ */
  const toTop = $(".to-top");
  let ticking = false;
  function onScroll() {
    const y = window.scrollY;
    document.body.classList.toggle("is-scrolled", y > 40);
    if (toTop) toTop.classList.toggle("is-visible", y > 700);
    ticking = false;
  }
  window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? "auto" : "smooth" });
    const main = $("#main"); if (main) main.focus({ preventScroll: true });
  });

  /* ---------------------------------------------------------------------
     Desktop dropdowns (hover via CSS; buttons for keyboard + touch)
     ------------------------------------------------------------------ */
  const subItems = $$(".nav-item.has-sub");
  function closeSubs(except) {
    subItems.forEach((li) => {
      if (li === except) return;
      li.classList.remove("is-open");
      const b = $(".sub-toggle", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  }
  subItems.forEach((li) => {
    const btn = $(".sub-toggle", li);
    if (!btn) return;
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = !li.classList.contains("is-open");
      closeSubs(li);
      li.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    li.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && li.classList.contains("is-open")) { closeSubs(); btn.focus(); }
    });
  });
  document.addEventListener("click", (e) => { if (!e.target.closest(".nav-item.has-sub")) closeSubs(); });

  /* ---------------------------------------------------------------------
     Mobile drawer (native <dialog> gives focus trapping + Esc)
     ------------------------------------------------------------------ */
  const drawer = $("#drawer");
  const drawerBtn = $(".nav-toggle");
  if (drawer && drawerBtn && typeof drawer.showModal === "function") {
    drawerBtn.addEventListener("click", () => { drawer.showModal(); drawerBtn.setAttribute("aria-expanded", "true"); });
    drawer.addEventListener("close", () => { drawerBtn.setAttribute("aria-expanded", "false"); drawerBtn.focus(); });
    $(".drawer__close", drawer).addEventListener("click", () => drawer.close());
    drawer.addEventListener("click", (e) => {
      if (e.target === drawer) drawer.close();                    // backdrop
      if (e.target.closest("a[href*='#']")) drawer.close();        // same-page anchors
    });
  }

  /* ---------------------------------------------------------------------
     Hero slider — background crossfade, text stays put.
     Auto-rotation pauses on hover/focus, with a pause button,
     and never runs when reduced motion is requested.
     ------------------------------------------------------------------ */
  const hero = $(".hero[data-slider]");
  if (hero) {
    const slides = $$(".hero__slide", hero);
    const dots = $$(".hero__dots button", hero);
    const pauseBtn = $(".hero__pause", hero);
    let i = 0, timer = null, userPaused = reduceMotion.matches;

    const show = (n) => {
      slides[i].classList.remove("is-active"); dots[i]?.removeAttribute("aria-current");
      i = (n + slides.length) % slides.length;
      slides[i].classList.add("is-active"); dots[i]?.setAttribute("aria-current", "true");
      const img = $("img", slides[i]); if (img && img.loading === "lazy") img.loading = "eager";
    };
    const stop = () => { clearInterval(timer); timer = null; };
    const start = () => { stop(); if (!userPaused && slides.length > 1) timer = setInterval(() => show(i + 1), 6500); };
    const syncPause = () => {
      pauseBtn.setAttribute("aria-pressed", String(userPaused));
      $(".icon-pause", pauseBtn).style.display = userPaused ? "none" : "";
      $(".icon-play", pauseBtn).style.display = userPaused ? "" : "none";
    };
    dots.forEach((d, n) => d.addEventListener("click", () => { show(n); start(); }));
    if (pauseBtn) { pauseBtn.addEventListener("click", () => { userPaused = !userPaused; syncPause(); start(); }); syncPause(); }
    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", start);
    hero.addEventListener("focusin", stop);
    hero.addEventListener("focusout", start);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    start();
  }

  /* ---------------------------------------------------------------------
     Reveal on scroll + number count-up
     ------------------------------------------------------------------ */
  const revealTargets = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion.matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  }

  const counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !reduceMotion.matches) {
    const run = (el) => {
      const target = parseInt(el.dataset.count, 10); const dur = 1400; const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur); const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased).toLocaleString("en-ZA").replace(/,/g, " ");
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { run(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach((c) => cio.observe(c));
  }

  /* ---------------------------------------------------------------------
     In-page tabs: highlight the section in view
     ------------------------------------------------------------------ */
  const tabLinks = $$(".page-tabs a[href^='#']");
  if (tabLinks.length && "IntersectionObserver" in window) {
    const map = new Map(tabLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        tabLinks.forEach((a) => { a.classList.remove("is-current"); a.removeAttribute("aria-current"); });
        const a = map.get(en.target.id);
        if (a) {
          a.classList.add("is-current"); a.setAttribute("aria-current", "location");
          a.scrollIntoView({ block: "nearest", inline: "center", behavior: "auto" });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) sio.observe(s); });
  }

  /* ---------------------------------------------------------------------
     Dates
     ------------------------------------------------------------------ */
  const MONTHS = {
    af: ["Januarie", "Februarie", "Maart", "April", "Mei", "Junie", "Julie", "Augustus", "September", "Oktober", "November", "Desember"],
    en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  };
  const MON_SHORT = { af: ["Jan", "Feb", "Mrt", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"], en: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] };
  const parseDate = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const fmtLong = (d, l) => `${d.getDate()} ${MONTHS[l][d.getMonth()]} ${d.getFullYear()}`;
  const biDate = (iso) => { const d = parseDate(iso); return bi(fmtLong(d, "af"), fmtLong(d, "en")); };

  /* ---------------------------------------------------------------------
     News (data in assets/js/news-data.js)
     ------------------------------------------------------------------ */
  const NEWS = (window.DINAMIKA_NEWS || []).slice().sort((a, b) => b.date.localeCompare(a.date));
  const newsModal = $("#news-modal");

  function newsCard(n) {
    return `<article class="news-card reveal is-visible" data-cat="${esc(n.category.en.toLowerCase())}">
      <div class="news-card__media">
        <img src="${esc(n.image)}" alt="${esc(n.alt.af)}" data-en-alt="${esc(n.alt.en)}" width="640" height="400" loading="lazy" decoding="async">
        <span class="tag">${bi(n.category.af, n.category.en)}</span>
      </div>
      <div class="news-card__body">
        <time datetime="${esc(n.date)}">${biDate(n.date)}</time>
        <h3>${bi(n.title.af, n.title.en)}</h3>
        <p>${bi(n.summary.af, n.summary.en)}</p>
        <button type="button" class="link-arrow news-card__btn" data-news="${esc(n.id)}">
          ${bi("Lees meer", "Read more")}
          <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </button>
      </div>
    </article>`;
  }

  $$("[data-news-list]").forEach((list) => {
    const limit = parseInt(list.dataset.limit || "0", 10);
    const cat = (list.dataset.category || "").toLowerCase();
    const pool = cat ? NEWS.filter((n) => n.category.en.toLowerCase() === cat) : NEWS;
    const items = limit ? pool.slice(0, limit) : pool;
    // Sport pages: the related-news section only appears when there is news for that sport
    const section = list.closest("[data-news-section]");
    if (section) { section.hidden = !items.length; if (!items.length) return; }
    list.innerHTML = items.length ? items.map(newsCard).join("")
      : `<p class="empty-state empty-state--light">${bi("Nog geen nuus nie — volg ons op Facebook vir die jongste nuus.", "No news yet — follow us on Facebook for the latest news.")}</p>`;
    applyLang(list);
  });

  const newsFilter = $("[data-news-filter]");
  if (newsFilter) {
    const cats = [...new Map(NEWS.map((n) => [n.category.en.toLowerCase(), n.category])).entries()];
    newsFilter.innerHTML = `<button type="button" class="chip" data-filter="all" aria-pressed="true">${bi("Alles", "All")}</button>` +
      cats.map(([key, c]) => `<button type="button" class="chip" data-filter="${esc(key)}" aria-pressed="false">${bi(c.af, c.en)}</button>`).join("");
    newsFilter.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip"); if (!chip) return;
      $$(".chip", newsFilter).forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
      const f = chip.dataset.filter;
      $$("[data-news-list] .news-card").forEach((card) => { card.hidden = f !== "all" && card.dataset.cat !== f; });
      const count = $$("[data-news-list] .news-card:not([hidden])").length;
      const live = $("#news-count"); if (live) live.textContent = lang() === "en" ? `${count} article${count === 1 ? "" : "s"} shown` : `${count} ${count === 1 ? "artikel" : "artikels"} gewys`;
    });
  }

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-news]");
    if (!btn || !newsModal) return;
    const n = NEWS.find((x) => x.id === btn.dataset.news); if (!n) return;
    const paras = (arr) => arr.map((p) => `<p>${esc(p)}</p>`).join("");
    $(".modal__content", newsModal).innerHTML = `
      <div class="modal__media"><img src="${esc(n.image)}" alt="${esc(n.alt.af)}" data-en-alt="${esc(n.alt.en)}"></div>
      <div class="modal__body">
        <span class="tag">${bi(n.category.af, n.category.en)}</span>
        <h2 id="news-modal-title" style="margin-top:12px">${bi(n.title.af, n.title.en)}</h2>
        <p style="color:var(--muted)"><time datetime="${esc(n.date)}">${biDate(n.date)}</time></p>
        <div class="prose"><div lang="af">${paras(n.body.af)}</div><div lang="en">${paras(n.body.en)}</div></div>
      </div>`;
    applyLang(newsModal);
    newsModal.showModal();
  });
  if (newsModal) {
    $(".modal__close", newsModal).addEventListener("click", () => newsModal.close());
    newsModal.addEventListener("click", (e) => { if (e.target === newsModal) newsModal.close(); });
  }

  /* ---------------------------------------------------------------------
     Calendar (data in assets/js/events-data.js) — past events hide themselves
     ------------------------------------------------------------------ */
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const EVENTS = (window.DINAMIKA_EVENTS || [])
    .filter((ev) => parseDate(ev.end || ev.date) >= today)
    .sort((a, b) => a.date.localeCompare(b.date));

  $$("[data-events]").forEach((list) => {
    const limit = parseInt(list.dataset.limit || "0", 10);
    const items = limit ? EVENTS.slice(0, limit) : EVENTS;
    if (!items.length) {
      list.outerHTML = `<p class="empty-state">${bi("Daar is tans geen komende geleenthede op die kalender nie.", "There are currently no upcoming events on the calendar.")}</p>`;
      return;
    }
    list.innerHTML = items.map((ev) => {
      const d = parseDate(ev.date);
      return `<li class="event">
        <time class="event__date" datetime="${esc(ev.date)}">
          <span class="event__day">${d.getDate()}</span>
          <span class="event__mon">${bi(MON_SHORT.af[d.getMonth()], MON_SHORT.en[d.getMonth()])}</span>
        </time>
        <div>
          <span class="event__title">${bi(ev.title.af, ev.title.en)}</span>
          <span class="event__meta">${ev.time ? esc(ev.time) + " · " : ""}${bi(ev.place.af, ev.place.en)}</span>
        </div>
      </li>`;
    }).join("");
  });

  /* ---------------------------------------------------------------------
     Staff directory (data in assets/js/staff-data.js)
     ------------------------------------------------------------------ */
  const staffRoot = $("[data-staff]");
  if (staffRoot && window.DINAMIKA_STAFF) {
    const GROUPS = [
      { key: "principal", af: "Hoof", en: "Principal" },
      { key: "deputy", af: "Adjunkhoofde", en: "Deputy Principals" },
      { key: "management", af: "Bestuur", en: "Management" },
      { key: "teaching", af: "Doserende Personeel", en: "Teaching Staff" },
    ];
    const card = (p) => `<li class="staff-card${p.group === "principal" ? " staff-card--lead" : ""}" data-group="${esc(p.group)}"
        data-search="${esc((p.name + " " + p.af.join(" ") + " " + p.en.join(" ")).toLowerCase())}">
        <div class="staff-card__photo"><img src="assets/img/staff/${esc(p.photo)}" alt="${esc(p.name)}" width="500" height="600" loading="lazy" decoding="async"></div>
        <div class="staff-card__body">
          <h3>${esc(p.name)}</h3>
          <ul lang="af">${p.af.map((r) => `<li>${esc(r)}</li>`).join("")}</ul>
          <ul lang="en">${(p.en.length ? p.en : p.af).map((r) => `<li>${esc(r)}</li>`).join("")}</ul>
          ${p.email ? `<a href="mailto:${esc(p.email)}"><svg class="icon icon--sm" viewBox="0 0 24 24" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>${esc(p.email)}</a>` : ""}
        </div>
      </li>`;
    staffRoot.innerHTML = GROUPS.map((g) => {
      const people = window.DINAMIKA_STAFF.filter((p) => p.group === g.key);
      if (!people.length) return "";
      return `<section class="staff-group" data-group-section="${g.key}" aria-labelledby="sg-${g.key}">
        <h2 id="sg-${g.key}">${bi(g.af, g.en)}</h2>
        <ul class="staff-grid">${people.map(card).join("")}</ul>
      </section>`;
    }).join("");

    const search = $("#staff-search");
    const chips = $$("[data-staff-filter] .chip");
    const status = $("#staff-count");
    let group = "all";
    const update = () => {
      const q = (search?.value || "").trim().toLowerCase();
      let shown = 0;
      $$(".staff-card", staffRoot).forEach((c) => {
        const inGroup = group === "all" || (group === "management" ? c.dataset.group !== "teaching" : c.dataset.group === group);
        const match = !q || c.dataset.search.includes(q);
        c.hidden = !(inGroup && match);
        if (!c.hidden) shown++;
      });
      $$("[data-group-section]", staffRoot).forEach((s) => { s.hidden = !$(".staff-card:not([hidden])", s); });
      $("#staff-empty").hidden = shown > 0;
      if (status) status.textContent = lang() === "en" ? `${shown} staff member${shown === 1 ? "" : "s"} shown` : `${shown} ${shown === 1 ? "personeellid" : "personeellede"} gewys`;
    };
    search?.addEventListener("input", update);
    chips.forEach((c) => c.addEventListener("click", () => {
      group = c.dataset.filter; chips.forEach((x) => x.setAttribute("aria-pressed", String(x === c))); update();
    }));
    update();
  }

  /* ---------------------------------------------------------------------
     Gallery lightbox
     ------------------------------------------------------------------ */
  const lightbox = $("#lightbox");
  const galleryBtns = $$(".gallery__btn");
  if (lightbox && galleryBtns.length) {
    const img = $("img", lightbox), cap = $("figcaption", lightbox);
    let idx = 0;
    const open = (n) => {
      idx = (n + galleryBtns.length) % galleryBtns.length;
      const src = galleryBtns[idx].querySelector("img");
      img.src = galleryBtns[idx].dataset.full || src.src;
      img.alt = src.alt;
      cap.textContent = src.alt;
      if (!lightbox.open) lightbox.showModal();
    };
    galleryBtns.forEach((b, n) => b.addEventListener("click", () => open(n)));
    $(".lightbox__prev", lightbox).addEventListener("click", () => open(idx - 1));
    $(".lightbox__next", lightbox).addEventListener("click", () => open(idx + 1));
    $(".lightbox__close", lightbox).addEventListener("click", () => lightbox.close());
    lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });
    lightbox.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") open(idx + 1);
      if (e.key === "ArrowLeft") open(idx - 1);
    });
    lightbox.addEventListener("close", () => galleryBtns[idx].focus());
  }

  /* ---------------------------------------------------------------------
     Contact form — validate on blur, summary on submit
     ------------------------------------------------------------------ */
  const MSG = {
    required: { af: "Hierdie veld is verpligtend.", en: "This field is required." },
    name: { af: "Vul asseblief u naam en van in.", en: "Please enter your name and surname." },
    email: { af: "Vul 'n geldige e-posadres in, bv. naam@voorbeeld.co.za.", en: "Enter a valid e-mail address, e.g. name@example.co.za." },
    phone: { af: "Vul 'n geldige telefoonnommer in (minstens 10 syfers).", en: "Enter a valid phone number (at least 10 digits)." },
    message: { af: "Skryf asseblief 'n boodskap van minstens 10 karakters.", en: "Please write a message of at least 10 characters." },
    consent: { af: "Bevestig asseblief dat ons u mag kontak.", en: "Please confirm that we may contact you." },
  };
  const form = $("#contact-form");
  if (form) {
    form.noValidate = true;
    const fields = $$("[data-validate]", form);
    const validate = (el) => {
      const type = el.dataset.validate; const v = (el.type === "checkbox" ? el.checked : el.value.trim());
      let err = "";
      if (type === "consent") { if (!v) err = "consent"; }
      else if (el.required && !v) err = type === "name" ? "name" : "required";
      else if (v && type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) err = "email";
      else if (v && type === "phone" && v.replace(/\D/g, "").length < 10) err = "phone";
      else if (type === "message" && v.length < 10) err = "message";
      const box = $(`#${el.id}-error`);
      el.setAttribute("aria-invalid", String(!!err));
      if (box) box.innerHTML = err ? `<svg class="icon icon--sm" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>${bi(MSG[err].af, MSG[err].en)}` : "";
      return !err;
    };
    fields.forEach((el) => {
      el.addEventListener("blur", () => { if (el.value || el.dataset.touched) validate(el); el.dataset.touched = "1"; });
      el.addEventListener("input", () => { if (el.getAttribute("aria-invalid") === "true") validate(el); });
      el.addEventListener("change", () => { if (el.type === "checkbox") validate(el); });
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const summary = $("#form-summary"), status = $("#form-status");
      status.hidden = true;
      const bad = fields.filter((el) => !validate(el));
      if (bad.length) {
        summary.innerHTML = `<h3 tabindex="-1">${bi("Kontroleer asseblief die volgende:", "Please check the following:")}</h3>
          <ul>${bad.map((el) => `<li><a href="#${el.id}">${$(`label[for="${el.id}"]`, form).innerHTML.replace(/<span class="req"[^>]*>.*?<\/span>/, "")}</a></li>`).join("")}</ul>`;
        summary.hidden = false;
        $("h3", summary).focus();
        return;
      }
      summary.hidden = true;
      const data = new FormData(form);
      const btn = $("button[type=submit]", form);
      btn.setAttribute("aria-busy", "true"); btn.disabled = true;
      try {
        if (FORM_ENDPOINT) {
          const res = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
          if (!res.ok) throw new Error("send failed");
          status.innerHTML = bi("Dankie! U boodskap is gestuur. Ons kontak u so gou moontlik.", "Thank you! Your message has been sent. We will contact you as soon as possible.");
          form.reset();
        } else {
          const subject = `${data.get("subject") || "Navraag"} — ${data.get("name")}`;
          const body = `${data.get("message")}\n\n${data.get("name")}\n${data.get("phone") || ""}\n${data.get("email")}`;
          window.location.href = `mailto:${SCHOOL_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
          status.innerHTML = bi(`U e-posprogram is oopgemaak met u boodskap. Stuur dit daarvandaan, of e-pos ons direk by ${SCHOOL_EMAIL}.`,
            `Your e-mail app has been opened with your message. Send it from there, or e-mail us directly at ${SCHOOL_EMAIL}.`);
        }
        status.className = "form-status"; status.hidden = false;
      } catch (err) {
        status.className = "form-summary";
        status.innerHTML = bi(`Die boodskap kon nie gestuur word nie. Probeer weer, of bel ons by 011 867 5986.`, `The message could not be sent. Please try again, or call us on 011 867 5986.`);
        status.hidden = false;
      } finally {
        btn.removeAttribute("aria-busy"); btn.disabled = false;
      }
    });
  }

  /* Footer year */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
