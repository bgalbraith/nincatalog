"""
Convert legacy nincatalog images to new naming scheme and db reference
"""
import glob
import os
import shutil

project_dir = '/Users/bgalbraith/Projects/nincatalog/'
src_dir = project_dir + 'archive/common/itemimages/'
dst_dir = project_dir + 'nincatalog/media/item_images/'
source = project_dir + 'data/prepared/item.txt'
fixture_dir = project_dir + 'nincatalog/catalog/fixtures/'

with open(fixture_dir + 'catalog_legacy_images.yaml', 'w') as fh:
    with open(source) as fh2:
        data = fh2.readlines()
    fh.write('# itemimage model\n')
    fields = data[0].strip().split('\t')

    db_image_counter = 0
    for record in data[1:]:
        values = record.strip().split('\t')
        pk = values[0]
        old_key = values[-1]
        os.chdir(src_dir)
        images = glob.glob("%s*.jpg" % old_key)
        item_image_counter = 0
        for image in images:
            db_image_counter += 1
            item_image_counter += 1
            key = image[:-4].split('-')[2][0]
            image_type = {'f': 1, 'b': 2, 'd': 4}.get(key, 3)
            filename = '%s-%02d.jpg' % (pk, item_image_counter)

            shutil.copy(src_dir+image, dst_dir+filename)

            fh.write("- model: catalog.itemimage\n")
            fh.write("  pk: %d\n" % db_image_counter)
            fh.write("  fields:\n")
            fh.write("    image: item_images/%s\n" % filename)
            fh.write("    item: %s\n" % pk)
            fh.write("    type: %d\n" % image_type)