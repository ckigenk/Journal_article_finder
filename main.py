#!/usr/bin/env python3
from bot.scrapper import JournalArticle


__author__="Collins Kigen"
__copyright__="Copyright 2022"
__credits__=["Collins Kigen"]
__license__="GPL"
__version__="1.0.0"
__maintainer__="Collins Kigen"
__email__="ckigen.k@gmail.com"

inst=JournalArticle()
inst.land_ncbi_page()
inst.search()
inst.scrape_data()
inst.save_data()