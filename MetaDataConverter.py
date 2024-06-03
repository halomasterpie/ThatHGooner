import zipfile
import yaml
import xml.etree.cElementTree as ET
from pathlib import Path

def generateMetaData(fname):
    ComicInfo = ET.Element("ComicInfo")
    Count = ET.SubElement(ComicInfo, "Count")
    Writer = ET.SubElement(ComicInfo, "Writer")
    Title = ET.SubElement(ComicInfo, "Title")
    Tags = ET.SubElement(ComicInfo, "Tags")
    metaData = "ComicInfo.xml"

    print("Opening: " + str(fname))

    with zipfile.ZipFile(fname) as z:
        with open('info.yaml', 'wb') as f:
            f.write(z.read('info.yaml'))

    with open('info.yaml') as f:
        result = yaml.safe_load(f)

    stream = open('info.yaml', 'r')
    data = yaml.safe_load(stream)

    def find(d, tag):
        if tag in d:
            yield d[tag]
        for k, v in d.items():
            if isinstance(v, dict):
                for i in find(v, tag):
                    yield i

    for val in find(data, 'Title'):
        Title.text = str(val)

    for val in find(data, 'Artist'):
        str_val = str(val)
        new_val1 = str_val.replace("[", "")
        new_val2 = new_val1.replace("'", "")
        new_val3 = new_val2.replace("]", "")
        Writer.text = new_val3

    for val in find(data, 'Tags'):
        str_val = str(val)
        new_val1 = str_val.replace("[", "")
        new_val2 = new_val1.replace("'", "")
        new_val3 = new_val2.replace("]", "")
        Tags.text = new_val3

    for val in find(data, 'Pages'):
        Count.text = str(val)

    tree = ET.ElementTree(ComicInfo)
    tree.write("ComicInfo.xml")

    ziptest = zipfile.ZipFile(fname, 'a', zipfile.ZIP_DEFLATED)
    ziptest.write(metaData)
    ziptest.close()

    print("Converted metadata for: " + str(fname))

my_dir = Path("D:/ANIYOMI/Anchira")
for file in my_dir.glob('*.cbz'):
    generateMetaData(file)
