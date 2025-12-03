from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re
import argparse
from io import StringIO


# unused: from docx import Document
from Markdown2docx import Markdown2docx
# from md2docx_python.src.md2docx_python import markdown_to_word
from markdown_pdf import MarkdownPdf, Section

from ResearchAids import ResearchAid
from md_to_website import download_button, front_matter


# def create_export_dir_structure(export_dir):
    
EXPORT_DIR = "EXPORTS"
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/colonial-heritage/research-aids/refs/heads/main/"



def parse_filename(orig_path, has_path=False):
    path_part = r'.+\/' if has_path else ''
    m = re.search(fr'{path_part}(.*)_[0-9]+\.yml', orig_path)
    if m:
        return m.group(1)
    raise ValueError(f"{orig_path} couldn't be parsed!")

def parse_filepath(fp):
    *pref, published, level, lang, fname = fp.split(os.path.sep)
    return published, level, lang, parse_filename(fname)


def get_export_path(orig_path, export_folder, extension=None, make_dirs=True):
    published, level, lang, name = parse_filepath(orig_path)
    if not extension:
        extension = export_folder.lower()
    extension = ("." + extension if not extension.startswith(".") else extension)
    export_path =  os.path.join(EXPORT_DIR, export_folder, published, level, lang, name) + extension
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    return export_path, (published, level, lang, name)


def export_markdown(f):
    md_name, _ = get_export_path(f, "MD")
    with open(f) as handle:
        yaml_content = yaml.safe_load(handle)
        ra = ResearchAid(yaml_content)
        if ra._parsed:
            md_content = ra()
            with open(md_name, "w") as md_handle:
                md_handle.write(md_content)

            return md_content


    
def export_pdf(f, md_content):
    pdf_name, _ = get_export_path(f, "PDF")
        
    pdf = MarkdownPdf()#toc_level=2)
    pdf.add_section(Section(md_content, toc=False))
    pdf.meta["title"] = "NAME"
    pdf.meta["author"] = "wreints"
    print(f"saving {pdf_name}")
    pdf.save(pdf_name)


def export_docx(f):
    from pdf2docx import Converter

    pdf_file, _ = get_export_path(f, "PDF")
    docx_file, _ = get_export_path(f, "DOCX")


    print(os.listdir(os.path.dirname(pdf_file)))
    # convert pdf to docx
    cv = Converter(pdf_file)
    cv.convert(docx_file)      # all pages by default
    cv.close()



if __name__ == "__main__":

    for cur_dir in ("published", "review"):
        eng = glob(f"{cur_dir}/*/English/*.yml")
        dutch = glob(f"{cur_dir}/*/Dutch/*.yml")
        # top = glob(f"{BASE_DIR}/TopLevel/*.yml")
    
        yaml_files = sorted(dutch + eng)

        for f in tqdm(yaml_files):
        # print(f"processing {f}...")

            md_content = export_markdown(f)

            export_pdf(f, md_content)
            export_docx(f)
