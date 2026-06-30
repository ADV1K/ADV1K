// ==UserScript==
// @name         XPath Copy Button
// @namespace    https://violentmonkey.github.io/
// @version      1.1.0
// @description  Adds a copy button at the top of /html/body/div[5]/…/div[2] and copies its text content
// @author       Advik
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  const TARGET_XPATH = '/html/body/div[5]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]';
  const INJECTED_ATTR = 'data-copy-btn-injected';

  function resolveXPath(xpath) {
    return document.evaluate(
      xpath,
      document,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null
    ).singleNodeValue;
  }

  function buildButton(target) {
    const btn = document.createElement('button');
    btn.textContent = 'Copy';
    btn.title = 'Copy all text content';
    btn.setAttribute('aria-label', 'Copy section text content');
    Object.assign(btn.style, {
      display: 'block',
      marginBottom: '8px',
      padding: '5px 14px',
      fontSize: '13px',
      fontFamily: 'inherit',
      lineHeight: '1.4',
      cursor: 'pointer',
      background: '#2563eb',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      zIndex: '9999',
      flexShrink: '0',
    });

    let resetTimer = null;

    const resetBtn = () => {
      btn.textContent = 'Copy';
      btn.style.background = '#2563eb';
      btn.disabled = false;
    };

    const succeed = () => {
      btn.textContent = '✓ Copied';
      btn.style.background = '#16a34a';
      clearTimeout(resetTimer);
      resetTimer = setTimeout(resetBtn, 2000);
    };

    const fail = () => {
      btn.textContent = '✗ Failed';
      btn.style.background = '#dc2626';
      clearTimeout(resetTimer);
      resetTimer = setTimeout(resetBtn, 2000);
    };

    btn.addEventListener('click', async () => {
      if (btn.disabled) return;
      btn.disabled = true;

      // Clone the target so we can strip the button node without touching the live DOM
      const clone = target.cloneNode(true);
      const cloneBtn = clone.querySelector(`[${INJECTED_ATTR}] button`) || clone.querySelector('button');
      if (cloneBtn) cloneBtn.remove();
      const text = (clone.innerText || clone.textContent || '').trim();

      try {
        await navigator.clipboard.writeText(text);
        succeed();
      } catch {
        // Fallback for browsers/pages that block the Clipboard API
        try {
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
          document.body.appendChild(ta);
          ta.focus();
          ta.select();
          const ok = document.execCommand('copy');
          ta.remove();
          ok ? succeed() : fail();
        } catch {
          fail();
        }
      }
    });

    return btn;
  }

  let observer = null;

  function inject() {
    const target = resolveXPath(TARGET_XPATH);
    if (!target || target.hasAttribute(INJECTED_ATTR)) return;
    target.setAttribute(INJECTED_ATTR, '1');
    target.prepend(buildButton(target));
    // Stop watching once injected — element is marked, no further work needed
    if (observer) observer.disconnect();
  }

  // Immediate attempt (page already parsed)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }

  // SPA safety: coalesced re-check via rAF to avoid per-mutation XPath cost
  let rafId = null;
  observer = new MutationObserver(() => {
    if (rafId) return;
    rafId = requestAnimationFrame(() => {
      rafId = null;
      const target = resolveXPath(TARGET_XPATH);
      if (target && !target.hasAttribute(INJECTED_ATTR)) inject();
    });
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
})();
