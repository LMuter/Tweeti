#!/bin/bash


#pandoc text/*.md -o text/out.pdf --toc --citeproc --bibliography text/van2023number.bib; xdg-open text/out.pdf
#pandoc text/*.md -o text/out.pdf --bibliography=text/van2023number.bib; xdg-open text/out.pdf

#pandoc text/*.md --top-level-division=chapter --toc --toc-depth=1 --filter pandoc-citeproc --bibliography text/bibliography.bib --csl text/apa-5th-edition.csl -o text/out.pdf; xdg-open text/out.pdf

output_location="output"
fname="developer_manual.pdf"
output_file="$output_location/$(date +'%y%m%d')_$fname"

#pandoc text/*.md --toc --toc-depth=2 --filter pandoc-citeproc --bibliography literature/bibliography.bib --csl templates/apa-5th-edition.csl --strip-comments -o $output_file; xdg-open $output_file
pandoc text/*.md --highlight-style tango --filter pandoc-citeproc --bibliography literature/bibliography.bib --csl templates/apa-5th-edition.csl --strip-comments -o $output_file; xdg-open $output_file
