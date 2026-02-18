Report build instructions

1. Upload the contents of the `report/` folder to Overleaf or compile locally.
2. Overleaf: Create a new project, then upload `ieee_report.tex` and `ieee_refs.bib`, and upload your real photos into `images/`.
3. Local build: use Latexmk or pdflatex+bibtex commands:
   - latexmk -pdf ieee_report.tex
   - or: pdflatex ieee_report.tex; bibtex ieee_report; pdflatex ieee_report.tex; pdflatex ieee_report.tex
4. Replace placeholder images in `report/images/` with real photos (use the same filenames or update the `\includegraphics{}` references).
5. A full expanded draft of the report has been created: see `ieee_report_full.tex` (includes a detailed ~10-page literature review and expanded analysis). If you need further revisions or want me to include specific papers, upload them and I will incorporate them.