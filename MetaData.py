import typer
import zipfile
import yaml
import xml.etree.cElementTree as ET
import glob

app = typer.Typer()

def generateMetadata(path:str):
    ext = '*.cbz'
    for file in glob.glob(path + '/' + ext):
        print(f"Started doing {file}")

        # Extract info.yaml from the ZIP file
        with zipfile.ZipFile(file) as zip:
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
        tree = ET.ElementTree(ComicInfo)
        tree.write(f"{path}/ComicInfo.xml")

        # Update the ZIP file with the new metadata XML
        with zipfile.ZipFile(file, 'a', zipfile.ZIP_DEFLATED) as z:
            z.write(f"{path}/ComicInfo.xml")

@app.command()
def main(
    path: str = '.'
):
    generateMetadata(path)

if __name__ == '__main__':
    typer.run(main)