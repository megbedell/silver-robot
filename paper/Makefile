TMP_SUFFS   = pdf aux bbl blg log dvi ps eps out ent
LATEX       = pdflatex -interaction=nonstopmode -halt-on-error
SUFF        = pdf
RM_TMP      = $(foreach d, ${TEX_FILES}, rm -rf $(foreach suff, ${TMP_SUFFS}, ${d}.${suff}))
NAME        = dimensions
CHECK_RERUN = grep Rerun ${NAME}.log

# You shouldn't need to edit below here.
default: ${NAME}.pdf

${NAME}.pdf: ${NAME}.tex
	${LATEX} ${NAME}.tex
	( ${CHECK_RERUN} && ${LATEX} ${NAME}.tex ) || echo "Done."
	( ${CHECK_RERUN} && ${LATEX} ${NAME}.tex ) || echo "Done."

clean:
	$(RM_TMP)
