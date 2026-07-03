# CyberFlow IDS: Approved File Format Submission Checklist

Use this checklist when your submission portal accepts only `.pdf`, `.docx`, and `.pptx`.

## Deliverable 1: Technical Core and Codebase (Submit as .docx or .pdf)

Target filename:
- CyberFlow_IDS_Technical_Source_Code.docx
- (Optional export) CyberFlow_IDS_Technical_Source_Code.pdf

### Required content
- Cover page with project title and student details.
- Live repository link (place prominently):
  - https://github.com/RaulGacusan748/cyberflow_ids
- Execution logs section:
  - Model Tournament terminal output (showing leaderboard and winning model).
  - Live packet replay simulation logs.
- Code appendices (full source code, pasted in labeled sections):
  - Appendix A: scratch/model_training_tournament.py
  - Appendix B: src/dashboard.py
  - Appendix C: scratch/live_detector.py

### Packaging steps
1. Create the document in Word.
2. Paste sections in this order: Cover Page, Repository Link, Execution Logs, Appendices A-C.
3. Save as `.docx`.
4. Export as `.pdf` if needed by portal.

### Verification checklist
- [ ] Repository URL is clickable and visible on first page.
- [ ] Training leaderboard log is included and readable.
- [ ] Live replay log is included and readable.
- [ ] All three appendices include full code.
- [ ] File opens cleanly on another machine.

---

## Deliverable 2: Two Presentations (Submit as .pdf or .pptx)

### 2.1 Technical Presentation (Peers and Graders)
Expected source file name:
- cyberflow_capstone_defense.html

Export to PDF:
1. Open the HTML file in Chrome/Edge.
2. Press Ctrl + P.
3. Destination: Save as PDF.
4. More Settings: enable Background graphics.
5. Save as: technical_presentation_gacusan.pdf

### 2.2 Business Presentation (Executive Audience)
Expected source file name:
- cyberflow_business_presentation.html

Export to PDF:
1. Open the HTML file in Chrome/Edge.
2. Press Ctrl + P.
3. Destination: Save as PDF.
4. More Settings: enable Background graphics.
5. Save as: executive_business_presentation_gacusan.pdf

### If portal requires .pptx
- Convert exported PDFs to `.pptx` via Adobe or PowerPoint import.

### Verification checklist
- [ ] Slides preserve backgrounds/colors after export.
- [ ] All text is readable in PDF preview.
- [ ] Final filenames match required naming.
- [ ] Converted `.pptx` opens without layout shift (if required).

---

## Deliverable 3: Final Written Report and Notebook Link (Submit as .docx or .pdf)

### 3.1 Capstone Final Report (Thesis)
Expected source file name:
- reports/cyberflow_ids_final_report.md

Packaging path:
1. Open markdown source.
2. Copy formatted content into Word.
3. Save as `.docx` or export `.pdf`.

### 3.2 Google Colab Notebook Link
Expected source file name:
- notebooks/colab_notebook_template.md

Packaging path:
1. Create a new notebook in Google Colab.
2. Copy template cells from your workspace file.
3. Run and validate outputs.
4. Click Share and set: Anyone with the link can view.
5. Paste the link on the cover page of Final Report or Technical Core document.

### Verification checklist
- [ ] Final report includes complete narrative sections.
- [ ] Colab link is clickable and publicly viewable.
- [ ] Link is placed in at least one submitted document cover page.

---

## Current Workspace Status (Auto-checked)

Found in workspace:
- scratch/model_training_tournament.py
- src/dashboard.py
- scratch/live_detector.py

Not currently found in workspace (create or locate before final packaging):
- cyberflow_capstone_defense.html
- cyberflow_business_presentation.html
- reports/cyberflow_ids_final_report.md
- notebooks/colab_notebook_template.md

---

## Final Upload Set (Recommended)

Minimum compliant submission (PDF-only route):
1. CyberFlow_IDS_Technical_Source_Code.pdf
2. technical_presentation_gacusan.pdf
3. executive_business_presentation_gacusan.pdf
4. cyberflow_ids_final_report.pdf

If `.docx` is accepted/preferred:
1. CyberFlow_IDS_Technical_Source_Code.docx
2. technical_presentation_gacusan.pdf (or `.pptx` if required)
3. executive_business_presentation_gacusan.pdf (or `.pptx` if required)
4. cyberflow_ids_final_report.docx
