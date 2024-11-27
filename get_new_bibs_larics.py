from scholarly import scholarly, ProxyGenerator
import bibtexparser

# pg = ProxyGenerator()
# success = pg.FreeProxies()
# scholarly.use_proxy(pg)
# with open('/home/frano/devel/code/git/publications/bibs/larics.bib') as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)

# print(bib_database.entries)
# print("PROXYING THIS SHIT")

prof_ids = ['keYJZDEAAAAJ','jYn27PkAAAAJ', 'y78ounEAAAAJ', 'dQGlphIAAAAJ','DKoiNVAAAAAJ']
titles = []
bib_out = open("new_bibs.bib", "w")
for id in prof_ids:
    # break
    author = scholarly.search_author_id(id, filled = True, sortby = "year", publication_limit = 3)
    # print(len(author['publications']))
    # break
    for pub in author['publications']:
        # print(pub)
        bib_entry = pub['bib']
        title = bib_entry['title']
        if title in titles:
            print("Item already added")
        else:
            if 'arxiv' not in bib_entry['citation'].lower() and 'authorea' not in bib_entry['citation'].lower():
                print("Adding: %s" % title)
                titles.append(title)
            else:
                print("Skipping preprint")

print("Found %s unique titles" % len(titles))


from habanero import Crossref, cn

cr = Crossref()

for new_title in titles:
    result = cr.works(query = new_title)
    for res_item in result['message']['items'][:5]:
        print(res_item)
        input("STOP")
    doi = result['message']['items'][0]['DOI']
    bib_entry = cn.content_negotiation(ids = doi, format = "bibentry")
    bib_out.write(bib_entry)
bib_out.close()