---
name: Lumina Gastronomy
colors:
  surface: '#1f0f10'
  surface-dim: '#1f0f10'
  surface-bright: '#483435'
  surface-container-lowest: '#190a0b'
  surface-container-low: '#281718'
  surface-container: '#2c1b1c'
  surface-container-high: '#382526'
  surface-container-highest: '#433030'
  on-surface: '#fbdbdb'
  on-surface-variant: '#e5bdbe'
  inverse-surface: '#fbdbdb'
  inverse-on-surface: '#3f2b2c'
  outline: '#ac8889'
  outline-variant: '#5c3f41'
  surface-tint: '#ffb3b6'
  primary: '#ffb3b6'
  on-primary: '#68001a'
  primary-container: '#ff5168'
  on-primary-container: '#5b0015'
  inverse-primary: '#be0037'
  secondary: '#ffdb9d'
  on-secondary: '#412d00'
  secondary-container: '#feb700'
  on-secondary-container: '#6b4b00'
  tertiary: '#62dda0'
  on-tertiary: '#003822'
  tertiary-container: '#18a56d'
  on-tertiary-container: '#00311d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b6'
  on-primary-fixed: '#40000c'
  on-primary-fixed-variant: '#920028'
  secondary-fixed: '#ffdea8'
  secondary-fixed-dim: '#ffba20'
  on-secondary-fixed: '#271900'
  on-secondary-fixed-variant: '#5e4200'
  tertiary-fixed: '#7ffaba'
  tertiary-fixed-dim: '#62dda0'
  on-tertiary-fixed: '#002112'
  on-tertiary-fixed-variant: '#005233'
  background: '#1f0f10'
  on-background: '#fbdbdb'
  surface-variant: '#433030'
typography:
  headline-xl:
    fontFamily: Outfit
    fontSize: 64px
    fontWeight: '700'
    lineHeight: 72px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1440px
  gutter: 24px
  margin-desktop: 80px
  margin-mobile: 20px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system is engineered for a premium, AI-driven culinary discovery experience. It targets sophisticated urban diners who value speed, exclusivity, and technological precision. The aesthetic is defined as **Hyper-Modern Glassmorphism**—merging a deep, cinematic dark mode with high-energy accents.

The emotional response should be one of "effortless luxury" and "intelligent curation." By utilizing frosted surfaces and vibrant light leaks against a void-black background, the UI mimics the atmosphere of a high-end, dimly lit lounge where the food (and the data) takes center stage.

**Visual Principles:**
- **Luminosity:** Use accent colors to draw the eye toward AI-generated insights and primary actions.
- **Translucency:** Depth is established through layers of glass rather than solid color shifts.
- **Precision:** Fine 1px borders and ample whitespace ensure the density of restaurant data feels manageable and curated.

## Colors
The palette is rooted in a deep "Ink Black" (#0A0A0A) to provide maximum contrast for the glass effects and photography. 

- **Electric Crimson (#FF3B5C):** Used for primary calls-to-action, status indicators (e.g., "Open Now"), and high-confidence AI matches.
- **Neon Amber (#FFB800):** Reserved for star ratings, premium "gold-tier" recommendations, and secondary interactive elements.
- **Glass Surfaces:** Surfaces are not solid; they utilize a highly transparent white tint (3%) to catch light, paired with a 10% opacity border to define edges against the dark background.

## Typography
This design system utilizes a dual-font strategy. **Outfit** provides a geometric, modern edge for headlines, while **Inter** ensures maximum legibility for dense restaurant metadata and AI descriptions.

- **Headlines:** Use high-contrast sizing. Large headlines should use negative letter spacing to feel tighter and more editorial.
- **Labels:** Small labels and "Micro-copy" (like price ranges or tags) should often use the `label-md` style with uppercase tracking to contrast against the organic feel of the restaurant imagery.
- **Color Application:** Use `text_primary` for titles and `text_secondary` for descriptions and supporting details to maintain a clear visual hierarchy.

## Layout & Spacing
The layout follows a **Fluid-Fixed Hybrid** model. On desktop, content is centered within a 1440px container using a 12-column grid.

- **Side-by-Side Structure:** For restaurant discovery, use a 40/60 split (e.g., Map or Filters on the left, Scrollable Results on the right).
- **Rhythm:** An 8px linear scale governs all padding and margins. 
- **Desktop Margins:** Generous 80px side margins are used on landing pages to create a "boutique" feel, while functional dashboards drop to 40px to maximize utility.
- **Mobile Reflow:** Elements stack vertically with a 20px safe area. Cards should occupy 100% of the width minus margins to maintain a large tap target.

## Elevation & Depth
Depth in this design system is achieved through **Backdrop Refraction** rather than traditional drop shadows.

- **The Glass Layer:** All elevated surfaces (cards, modals, navigation bars) must use `surface_color_rgba` combined with a `backdrop-filter: blur(16px)`.
- **Stroke Definition:** A 1px internal border (`border_color_rgba`) is mandatory for all glass elements to simulate the edge of a physical pane of glass catching light.
- **Shadows:** Use extremely soft, large-radius shadows (e.g., `0px 20px 40px rgba(0,0,0,0.4)`) only on the topmost floating elements like Modals or Popovers to separate them from the background glass layers.
- **Z-Axis:** 
  - Level 0: Background (#0A0A0A)
  - Level 1: Cards and content blocks (Blur 12px)
  - Level 2: Navigation and floating filters (Blur 20px)
  - Level 3: Modals and AI Chat Overlays (Blur 32px + Shadow)

## Shapes
The shape language is "Hyper-Rounded," emphasizing approachability and a modern hardware-inspired look (similar to high-end mobile OS styles).

- **Standard Elements:** Buttons and small input fields use a 16px (`rounded-lg`) radius.
- **Containers:** Restaurant cards and section containers use a 24px (`rounded-xl`) radius.
- **Pill Elements:** Search bars and status chips (e.g., "Trending") should be fully pill-shaped (999px) to contrast against the structured grid.
- **Media:** Photography must always match the border radius of its parent container to maintain the "encapsulated" glass look.

## Components
- **Buttons:** 
  - *Primary:* Electric Crimson background, white text, 16px radius. On hover, add a subtle outer glow using the primary color.
  - *Ghost:* Transparent background with a 1px `border_color_rgba`.
- **Cards:** The core of the experience. Must include a 1px border, 16px backdrop-blur, and 24px corner radius. Images within cards should have a subtle dark gradient overlay at the bottom to ensure white text remains readable.
- **AI Recommendation Chips:** Use a gradient border (Crimson to Amber) to signify an AI-generated tag.
- **Inputs:** Search fields should be glass-textured with a 10% white border. The cursor and focus state should utilize the Neon Amber color for high visibility.
- **Lists:** Use "Divideless" lists where items are separated by whitespace and subtle background hover states (2% white) rather than horizontal lines.
- **AI Chat Interface:** A floating glass orb or side-panel with the highest blur factor (32px), using "vibe-based" gradients in the background to indicate processing.