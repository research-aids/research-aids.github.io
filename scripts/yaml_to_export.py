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
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/colonial-heritage/research-guides-dev/refs/heads/main/"



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
    os.makedirs(os.path.dirname(md_name), exist_ok=True)
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

def write_level_base_md(f):
    _, (published, level, lang, name) = get_export_path(f, "WEBSITE", "md")
    folder_name = f"{EXPORT_DIR}/WEBSITE/{level}"
    

    # published = os.path.split(out_dir)[-1].capitalize()
    with open(f"{folder_name}/{level}.md", "w") as md:
        level_md = f"""---
layout: default
title: {level_str}
nav_enabled: true
has_toc: true
parent: {published.capitalize()}
---
This is level {level_str[-1]} of the RAs.
"""
        md.write(level_md)
        # return level_md



def export_website(f, md_content):
    md_name, (published, level, lang, name) = get_export_path(f, "WEBSITE", "md")
    
    pdf_button = f"[Download PDF]({GITHUB_RAW_BASE_URL + get_export_path(f, "PDF")}){{: .btn .btn-blue }}"
    docx_button = f"[Download DOCX]({GITHUB_RAW_BASE_URL + get_export_path(f, "DOCX")}){{: .btn .btn-blue }}"
    
    website_content = front_matter(published, name, level, lang) + "\n\n" +\
                                pdf_button + " |||    " + docx_button +\
                                "\n\n" + md_content

    with open(md_name, "w") as web_handle:
        web_handle.write(website_content)
    # return website_content

    
def export_pdf(f, md_content):
    md_name, _ = get_export_path(f, "WEBSITE", "md")
        
    pdf = MarkdownPdf()#toc_level=2)
    pdf.add_section(Section(markdown_content, toc=False))
    pdf.meta["title"] = name
    pdf.meta["author"] = "wreints"
    # print(f"saving {new_name}")
    pdf.save(new_name)


def export_docx(f):
    from pdf2docx import Converter

    pdf_file, _ = get_export_path(f, "PDF")
    docx_file = get_export_path(f, "DOCX")

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

            level, lang, name = parse_filepath(f)

            md_content = export_markdown(f)
            export_level_base(f)
            export_website(f, md_content)

            export_pdf(f, md_content)
            export_docx(f, md_content)
