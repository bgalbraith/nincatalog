"""
Convert prepared legacy nincatalog text files to YAML fixtures for import
"""
import re

base = '/Users/bgalbraith/Projects/nincatalog/data/prepared/'
fixture_dir = '../catalog/fixtures/'

tables = ('artist', 'mediapackage', 'mediaformat', 'country', 'musiclabel',
          'era', 'itemrarity', 'item')

with open(fixture_dir + 'catalog_legacy_data.yaml', 'w') as fh:
    for table in tables:
        source = base + table + '.txt'
        with open(source) as fh2:
            data = fh2.readlines()
        fh.write('# %s model\n' % table)
        fields = data[0].strip().split('\t')
        for record in data[1:]:
            values = record.strip().split('\t')
            fh.write("- model: catalog.%s\n" % table)
            fh.write("  pk: %s\n" % values[0])
            fh.write("  fields:\n")
            for field, value in zip(fields[1:], values[1:]):
                if value == '':
                    continue
                if re.search('(#|:)', value) is not None or value[0] == '`':
                    if value.find('"') != -1:
                        value = ">\n      " + value
                    else:
                        value = "\"%s\"" % value
                fh.write("    %s: %s\n" % (field, value))
        fh.write('\n')