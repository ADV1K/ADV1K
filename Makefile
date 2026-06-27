watch:
	{ find resume -name "*.typ"; echo resume.toml; } | entr -r make pdf

open:
	open -a "Google Chrome" "file://$(PWD)/resume-advik.pdf"

pdf:
	typst compile resume/resume.typ resume-advik.pdf --root .

doc: pdf
	pandoc resume-advik.pdf -o resume-advik.docx

.PHONY: watch open pdf doc
