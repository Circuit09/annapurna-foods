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
- [ ] Ubuntu ISO download completed
- [ ] VMware VM created
- [ ] Ubuntu installed and verified
- [ ] Development environment installed
- [ ] Initial application created
- [ ] Local application tested
- [ ] Cloud hosting selected
- [ ] Cloud deployment tested
- [ ] Backup and restore tested

## Last Completed Milestone
Private GitHub repository created.

## Next Action
Create and commit this status file. Then complete the
Ubuntu ISO download and create the Annapurna-Dev VM.

## Important Decisions
Do not expose the development laptop directly to the
internet. Deploy to an independently hosted server only
after local testing and data-protection measures are ready.
