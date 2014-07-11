"""
Convert nincatalog XML database tables to flat files
"""
import xml.etree.ElementTree as ET

base = '/Users/bgalbraith/Projects/nincatalog/data/'
tables = ('added_date', 'categories', 'collection', 'country', 'dataview',
          'era', 'format', 'halo', 'labels', 'packagetype', 'scale',
          'tracklist')

for table in tables:
    source = base + table + '.xml'
    tree = ET.parse(source)
    root = tree.getroot()
    header = list()
    fh = open(base + table + '.txt', 'w')
    for entry in root:
        if len(header) == 0:
            for item in entry:
                header.append(item.tag)
            fh.write('\t'.join(header)+'\n')
        record = list()

        for field in header:
            f = entry.find(field)
            if f is None:
                text = ''
            else:
                text = f.text
                if text is None:
                    text = ''
                text = text.replace('\n', '')
            record.append(text)

        fh.write('\t'.join(record)+'\n')
    fh.close()