import os
import glob
import yaml
import zipfile
import typer
import xml.etree.ElementTree as ET
from zipfile import BadZipFile

app = typer.Typer()

def generateMetadata(path: str):
    ext = '*.cbz'
    badFile = []
    for file in glob.glob(os.path.join(path, ext)):
        print(f"Started doing {file}...", end='\t')

        try:
            # Extract info.yaml from the ZIP file
            with zipfile.ZipFile(file, 'r') as zip:
                if 'ComicInfo.xml' in zip.namelist():
                    print(" Skipped")
                    continue

                with zip.open('info.yaml') as f:
                    data = yaml.safe_load(f)

            # Create ComicInfo XML structure
            ComicInfo = ET.Element("ComicInfo")
            Count = ET.SubElement(ComicInfo, "Count")
            Writer = ET.SubElement(ComicInfo, "Writer")
            Title = ET.SubElement(ComicInfo, "Title")
            Tags = ET.SubElement(ComicInfo, "Tags")

            # Extract and process metadata from info.yaml
            for key in ['Title', 'Artist', 'Tags', 'Pages']:
                if key in data:
                    if key == 'Title':
                        Title.text = str(data[key])
                    elif key == 'Artist' or key == 'Tags':
                        Writer.text = ', '.join(map(str, data[key]))
                    elif key == 'Pages':
                        Count.text = str(data[key])

            # Write ComicInfo to XML file
            xml_file_path = os.path.join(path, "ComicInfo.xml")
            tree = ET.ElementTree(ComicInfo)
            tree.write(xml_file_path)

            # Update the ZIP file with the new metadata XML
            with zipfile.ZipFile(file, 'a', zipfile.ZIP_DEFLATED) as z:
                z.write(xml_file_path, "/ComicInfo.xml")
            print(" Done")
        except BadZipFile:
            print(" Bad Zip File")
            badFile.append(file)

    return badFile


@app.command()
def main(
    path: str = '.'
):
    for file in generateMetadata(path):
        print(file)

if __name__ == '__main__':
    typer.run(main)
