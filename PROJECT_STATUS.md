# Annapurna Foods — Project Status

## Project Goal
Build a simple, mobile-friendly web portal for the
family-run Annapurna Foods business.

The portal will allow the user's father to record sales,
raw-material purchases, expenses, and inventory. The user
will review business performance and profit/loss remotely.

## Business Context
- Brand: Annapurna Foods
- Business managed by parents from their hometown
- Existing products: peanuts, three types of handmade
  chakli, chivda occasionally, and ladoo occasionally
- Sales channels: small alcohol shops, retailers, and
  neighbours through word of mouth
- FSSAI number obtained
- HUF process in progress
- New roasting machine is operational
- Roaster can handle peanuts, chana, green peas, and
  similar products

## Technical Plan
- Development environment: VMware Workstation
- Guest OS: Ubuntu Desktop LTS
- Backend: Python + FastAPI
- Database: SQLite initially
- Interface: simple, responsive browser-based GUI
- Source control: private GitHub repository
- Hosting: evaluate a suitable cloud host
- Persistent database storage and backups are mandatory

## User Requirements
- Father must be able to use the portal on a phone or PC
- Simple data-entry screens
- Record daily sales with product, quantity, and revenue
- Record raw-material purchases and expenses
- Track inventory and production
- Calculate profit/loss from recorded data
- Keep initial scope small
- Allow future expansion into a public brand website

## Development Rules
- Build incrementally and test each feature
- Avoid unnecessary complexity
- Never commit passwords, secrets, live business data,
  or SQLite database files to GitHub
- Maintain database backups separately
- Update this file after each major milestone
- Record the exact next action before stopping a session

## Current Status
- [x] Private GitHub repository created
- [x] Ubuntu ISO download completed
- [x] VMware VM created
- [x] Ubuntu installed and verified
- [x] Development environment installed
- [x] Initial application created
- [ ] Local application tested
- [ ] Cloud hosting selected
- [ ] Cloud deployment tested
- [ ] Backup and restore tested

## Development Environment (Working)
- Host: VMware Workstation on the development machine
- Guest OS: Ubuntu 26.04.1 LTS (verified)
- Editor and AI assistant: VS Code with the Kilo Code extension
- Kilo Code provider: FreeModel
  - Provider entry: `openainew`, display name `freemodel`
  - Model: `claude-opus-5-5` (shown as "claude")
- Kilo configuration is stored outside the repository, in
  `~/.config/kilo/kilo.jsonc`. No credentials are kept in
  the project folder, so none can be committed by accident.
- Source control: GitHub repository connected as the remote
  `origin` (github.com/Circuit09/annapurna-foods), branch `main`

## Current Application Scope
The project currently consists of a single public homepage.
No backend, no database and no JavaScript exist yet.

Files in the repository:
- `index.html` - homepage markup
- `style.css` - homepage styling
- `PROJECT_STATUS.md` - this file
- `README.md` - one-line project description

What the homepage contains:
- Header with brand name and tagline
- Sticky navigation bar linking to each section
- Hero / welcome section with call-to-action buttons
- Four product cards: Roasted Peanuts, Handmade Chakli
  (with separate Bhajani/Multigrain and Rice Flour variants),
  Chivda, Ladoo
- About Us section
- Contact section with Call and WhatsApp buttons
- Footer
- Responsive layout for Android phones and desktop screens

Known gaps in the homepage (to be addressed next):
- Phone number and WhatsApp number are still placeholders, so
  the contact buttons do not work yet
- No product photographs
- Product cards carry no prices, by design for now
- Business context above lists three types of handmade chakli,
  but the homepage currently shows two variants. The third
  needs to be confirmed before it is added.

## Last Completed Milestone
Initial homepage implemented with `index.html` and `style.css`,
then committed and pushed to GitHub on the `main` branch
(commit `dd6b64f`, "Build initial Annapurna Foods homepage").
Local `main` is in sync with `origin/main`.

## Next Action
Review the homepage in a browser on both desktop and an
Android phone, and confirm it looks correct. Then:

1. Review homepage and fix any layout or wording issues
2. Improve the design and add product photographs
3. Confirm the third chakli variant and add it to the page
4. Replace the phone and WhatsApp placeholders with the real
   numbers
5. Build the business dashboard
6. Add sales entry
7. Add expense entry
8. Add inventory tracking

## Important Decisions
Do not expose the development laptop directly to the
internet. Deploy to an independently hosted server only
after local testing and data-protection measures are ready.
