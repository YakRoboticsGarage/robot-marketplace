# Construction Industry Visual Language Research

Research date: 2026-03-27. Analyzed websites and brand systems of 17 companies across
construction tech platforms, survey/geospatial, major GCs, and drone operators.

## Company-by-Company Findings

### Construction Tech Platforms

**Procore** — Orange (#F47E20) as primary accent on white, with dark navy text. Uses Inter
as their system typeface (CORE Design System). Orange hexagon logo motif. Cards have
moderate radius (~8px). Buttons are solid-fill rounded rectangles. Tone: corporate-tech
with construction warmth via the orange. All-caps sparingly (nav labels). HSL-based color
system with blue progressions for UI states.

**OpenSpace.ai** — Refreshed brand (2025): vibrant blues with warmer neutrals. Textures
and patterns inspired by construction materials add grit. Photography-forward with real
jobsite imagery. Sans-serif headers at heavy weight. Dark overlays on hero photography.
Tone: tech-forward but grounded in construction reality.

**DroneDeploy** — Blue-dominant palette (#4CA3F3 primary, #1C0E4E dark accent, #094F8F
mid-blue). Light feel, generous whitespace. Aerial/drone imagery as hero content. Clean
sans-serif. Cards with soft shadows, moderate corner radius. Tone: approachable tech,
nature-meets-precision.

**Propeller.aero** — Blue primary with orange-amber accents. Survey/earthworks imagery.
Bold sans-serif headings, clean body copy. Data visualization emphasis with topographic
map aesthetics. Tone: precision-engineering with startup energy.

**Skydio** — Dark theme dominant (black/charcoal backgrounds, white text). Blue accent for
CTAs. Product photography on dark backgrounds. Heavy-weight sans-serif headings, often
all-caps for category labels. Minimal card UI, full-bleed imagery. Tone: premium defense/
enterprise hardware. The most "industrial-tech" of the group.

**Pix4D** — Blue and green palette (updated 2021 rebrand). Clean Swiss-influenced typography.
White backgrounds with colored section breaks. Photogrammetry/3D model imagery. Moderate
shadows, rounded buttons. Tone: scientific precision, European clean.

### Survey/Geospatial Companies

**Trimble** — Deep navy (#002D5B) with Trimble Yellow (#FFBE00) as accent. Modus Design
System uses blue progressions as primary UI color. Green (#349C44) reserved for success
states only. Clean sans-serif, moderate weight. Cards with subtle borders rather than
heavy shadows. Tone: engineering-grade professional, restrained.

**Leica Geosystems (Hexagon)** — Red primary (Leica heritage red), dark backgrounds for
product showcases. White space on content pages. Technical, precise typography. Product
photography is crisp with neutral backgrounds. Tone: premium instrumentation, Germanic
precision.

**Topcon** — Blue primary with subtle gray backgrounds. Product-centric photography.
Conservative layout, traditional corporate structure. Sans-serif throughout. Moderate
radius, standard shadow depth. Tone: dependable, established.

### Major GCs (Buyer Expectations)

**Kiewit** — Yellow (#FFCD23) and black. Bold, high-contrast. Arial Black for wordmark.
Project photography dominates. Minimal UI complexity, content-forward. Tone: muscular,
no-nonsense, field-ready.

**Skanska** — Skanska Blue (#143275) primary. Clean, modern wordmark. Sustainability
messaging throughout. White backgrounds, generous spacing. Professional sans-serif.
Tone: Scandinavian corporate, forward-looking, trustworthy.

**Turner Construction** — Dark blue wordmark, clean conservative layout. Project
photography with people on jobsites. Traditional corporate website structure.
Tone: established authority, understated.

**Granite Construction** — Earth tones, blue accents. Infrastructure and heavy equipment
imagery. Conservative design. Tone: dependable, infrastructure-scale.

### Drone Operators

**Zeitview (DroneBase)** — Dark theme with blue/teal accents. Aerial imagery hero.
Modern sans-serif, SaaS-style card layouts. Tone: data-meets-field-ops.

**Skycatch** — Blue primary, construction site photography. Clean dashboard-style
layouts emphasizing data products. Tone: precision analytics for construction.

---

## Construction Industry Visual Language

### Color Palette

The industry converges on a clear hierarchy: **blues for trust, warm accents for energy**.

Recommended palette for our demo (replacing current orange-only scheme):

| Role | Hex | Name | Rationale |
|------|-----|------|-----------|
| Primary | `#1B3A5C` | Slate Navy | Deep blue found across Procore, Trimble, Skanska, Turner. Trust. |
| Primary Light | `#2D5F8A` | Field Blue | Mid-blue for interactive states, links. Matches DroneDeploy/OpenSpace. |
| Accent | `#E8792B` | Site Orange | Construction-signal orange. Close to Procore (#F47E20) but warmer. |
| Accent Hover | `#C4611E` | Deep Amber | Darkened for hover/active states. |
| Accent Light | `#FEF0E3` | Orange Wash | Background tint for badges, alerts. |
| Success | `#1A7D4E` | Safety Green | Deeper than current, closer to Trimble's approach. |
| Warning | `#C27B1A` | Hard Hat Amber | Equipment-yellow territory without being Kiewit-bright. |
| Neutral 900 | `#1A1F26` | Asphalt | Near-black for primary text. Darker than current #111827. |
| Neutral 600 | `#4A5568` | Concrete | Secondary text. |
| Neutral 300 | `#CBD5E0` | Rebar Gray | Borders, dividers. |
| Neutral 100 | `#F0F2F5` | Gravel | Subtle backgrounds. Cooler than current #f8f9fa. |
| Surface | `#FFFFFF` | White | Card backgrounds. |

### Typography

Construction-tech favors **clean sans-serifs that feel heavier than typical SaaS**.

- **Keep Inter** for body text. Procore itself uses Inter. It works.
- **Headers: switch to IBM Plex Sans at 600-700 weight**. It has more mechanical
  character than Inter -- the squared-off terminals echo technical drawing letterforms.
  Used across industrial/enterprise SaaS. Free on Google Fonts.
- **Monospace: keep JetBrains Mono** for data values, bid amounts, robot IDs.
- **All-caps: use sparingly** for status badges (ACTIVE, COMPLETE) and section
  labels. Never for body text. Skydio and Kiewit use all-caps for category labels;
  it reads as industrial authority.
- **Letter-spacing: -0.02em to -0.03em** on headings (tighter than Inter default).
  This is universal across the category.

### Component Style

| Element | Current | Recommended | Reference |
|---------|---------|-------------|-----------|
| Card radius | 8px / 12px | **6px** | Trimble Modus, Procore CORE lean sharper. Construction = precision, not playful. |
| Button radius | 40px (pill) | **6px** (squared) | Every GC and survey company uses squared buttons. Pills read as consumer. |
| Button style | Solid orange pill | Solid fill, 6px radius, heavier padding (12px 24px) | Procore, Trimble, DroneDeploy all use filled rectangular buttons. |
| Border weight | 1px / 1.5px | **1px solid**, slightly cooler gray | Trimble and Procore use subtle 1px borders with low-contrast grays. |
| Shadow | 0 1px 3px | **0 1px 2px rgba(0,0,0,0.06)** default, **0 2px 8px rgba(0,0,0,0.08)** on hover | Lighter base shadows, more lift on interaction. Construction sites are bright. |
| Input fields | Pill (40px radius) | **6px radius**, 1px border, 44px height | Match button language. Pill inputs are a consumer pattern. |
| Status badges | Rounded pills | **4px radius, all-caps, 0.05em tracking, 11px font** | Tighter, more utilitarian. Think equipment status panels. |

### Distinctive Elements

What separates construction-tech from generic SaaS:

1. **Photography over illustration.** Every company uses real jobsite photos, drone
   aerials, or equipment shots. No cartoon illustrations or abstract blobs. Our demo
   should feel like it belongs on a dusty tablet at a site trailer.

2. **Data density tolerance.** Construction buyers expect dashboards with numbers,
   not marketing fluff. Showing bid amounts, timestamps, robot specs, and coordinates
   simultaneously is expected -- not cluttered.

3. **Utilitarian color usage.** Color means something: green = go/safe, amber = warning,
   red = stop/overdue. Orange = high visibility (like safety vests). No decorative
   gradients. If a color is present, it carries information.

4. **Heavier UI chrome.** Compared to consumer apps, construction-tech uses slightly
   thicker borders, heavier font weights, and more defined card boundaries. Content
   needs to be readable in bright outdoor light on tablets.

5. **Dark header bars.** Procore, Trimble, and Skydio all use dark (navy or black)
   top navigation. This anchors the interface and reads as "tool" rather than "website."

6. **Topographic/grid textures.** Subtle background patterns referencing survey grids,
   contour lines, or blueprint grids appear across DroneDeploy, Propeller, and Pix4D.
   A very faint grid or topo pattern could differentiate our demo background.

### Specific Recommendations for Our Demo

1. **Replace pill search input** (border-radius: 40px) with squared input (border-radius: 6px). Before: consumer chat-bubble shape. After: precision input field matching Trimble/Procore.

2. **Replace pill search button** with 6px-radius rectangular button inside the input. Before: floating circle. After: integrated rectangular "Search" button.

3. **Change accent color** from #E67E22 to #E8792B (warmer, more construction-orange) and add navy primary #1B3A5C for headers and nav background.

4. **Darken the header** to navy (#1B3A5C) with white text/links. Before: white header with gray border. After: dark command-bar feel like Procore/Trimble nav.

5. **Tighten card border-radius** from 8px/12px to 6px everywhere. Sharper = more precise = more construction.

6. **Add all-caps treatment to status badges** (SURVEYING, ACTIVE, COMPLETE) with 0.05em letter-spacing at 11px. Before: mixed-case soft pills. After: instrument-panel labels.

7. **Switch heading font** from Inter 700 to IBM Plex Sans 600/700. Load via Google Fonts alongside Inter. This adds mechanical character without a full redesign.

8. **Reduce heading letter-spacing** to -0.03em (already present, verify consistent).

9. **Replace step indicator pills** with squared badges (4px radius) connected by a thin line, not chevrons. Before: colorful pills with arrows. After: progress tracker like a project timeline.

10. **Change focus ring** from orange glow to blue (#2D5F8A) ring. Orange focus = confusing because orange means "construction alert." Blue focus = standard interactive affordance.

11. **Add a subtle grid background** to the hero section. A faint 40px CSS grid pattern at 3% opacity in #CBD5E0 references survey/blueprint grids without being heavy.

12. **Increase body text contrast.** Change --text-2 from #4B5563 to #4A5568 and --text-3 from #9CA3AF to #6B7280. Construction buyers are often outdoors on bright screens.

13. **Make bid amount displays more prominent.** Use JetBrains Mono at 600 weight, slightly larger (1.1em), with the navy primary color. Monetary values should feel like instrument readouts.

14. **Replace green badge background** (#ECFDF5) with a slightly more saturated #E6F5ED. Current shade is too minty/consumer.

15. **Add 1px left-border accent** on robot cards (4px wide, accent orange) instead of relying solely on shadow for card hierarchy. This is a common Procore/Trimble pattern for active/selected items.

16. **Square off the step-indicator pills** (currently border-radius: 20px) to 4px. Maintain the filled accent background for the active step.

17. **Use heavier font-weight (600)** for all interactive labels (buttons, links, nav items). Current 500 is too light for outdoor/bright-screen readability.

18. **Reduce shadow-lg intensity.** Change from rgba(0,0,0,0.1) to rgba(0,0,0,0.06) with a tighter spread. Construction-tech uses flatter designs; heavy shadows read as consumer.

19. **Add a "powered by" or data-source indicator** in the footer area using a small mono-font badge. Construction professionals expect transparency about data provenance.

20. **Consider a dark-mode variant** for the auction monitoring view. Skydio and Zeitview demonstrate that dark themes work for operational dashboards. Not essential for v1, but the navy palette (#1A1F26 background, #F0F2F5 text) would convert cleanly.

---

Sources referenced:
- [Procore CORE Design System](https://core.procore.com/)
- [Procore Brand Guide](https://brand.procore.com/design/)
- [Trimble Modus Design System](https://modus.trimble.com/foundations/color-palette/)
- [Trimble Brand Colors](https://www.brandcolorcode.com/trimble-inc)
- [OpenSpace Brand Refresh](https://www.openspace.ai/blog/new-brand-identity/)
- [DroneDeploy Brand Colors](https://brandfetch.com/dronedeploy.com)
- [Skanska Brand Colors](https://colorcodeshub.com/brand/skanska)
- [Construction Branding Color Guide](https://designbro.com/blog/guides/construction-company-branding-color/)
- [Construction Website Color Palettes](https://constructiondigitalmarketing.com/website-design/website-design-and-development/choosing-the-right-color-palette-for-your-construction-website/)
- [Top Construction Company Logos](https://www.digglescreative.com/blog/logos-for-the-top-10-construction-companies-in-the-us.html)
