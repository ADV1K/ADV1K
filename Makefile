LATO_VARIANTS = Thin ThinItalic Light LightItalic Regular Italic Bold BoldItalic Black BlackItalic
LATO_BASE_URL = https://github.com/google/fonts/raw/main/ofl/lato

watch:
	{ find resume -name "*.typ"; echo resume.toml; } | entr -r make pdf

open:
	open -a "Google Chrome" "file://$(PWD)/resume-advik.pdf"

fonts:
	mkdir -p .fonts
	$(foreach v,$(LATO_VARIANTS),curl -fL "$(LATO_BASE_URL)/Lato-$(v).ttf" -o ".fonts/Lato-$(v).ttf";)

pdf:
	typst compile resume/resume.typ resume-advik.pdf --root . --font-path .fonts

doc: pdf
	pandoc resume-advik.pdf -o resume-advik.docx

.PHONY: watch open pdf doc fonts
