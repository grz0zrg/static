# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Minimalist static site builder to be used with https://github.com/grz0zrg/pynut (not needed but may be useful to concat JS/CSS/HTML file into a single file!)
#
# This tool was built to produce my portfolio at : www.onirom.fr
# For an usage example : https://github.com/grz0zrg/portfolio
#
# It provide a simple way to produce generated HTML pages content from a combination of JSON data definitions and HTML templates.
# It also generate a sitemap, the sitemap is constructed from the given URL in the program arguments.
#
# Usage: static_build.py json/categories.json json/items.json dist/index.html https://www.myportfolio.com

import os
import re
import sys
import glob
import json
import codecs
import datetime
from xml.etree import ElementTree as ET

def gen_nav_menu(html_template_file, pages):
    with open(html_template_file, 'r') as content_file:
        html_template = content_file.read()

    pages_nav = []

    for current_page in pages:
        html_output = ""

        current_page_name = current_page["name"].replace(" ", "_")

        for item in pages:
            temp_html = ""

            page_name_org = item["name"]
            page_name = page_name_org.replace(" ", "_")

            if page_name == current_page_name:
                temp_html += html_template.replace("{active}", "active")
            else:
                temp_html += html_template.replace("{active}", "")

            html_output += temp_html.replace("{name}", page_name).replace("{_name}", page_name_org)

        pages_nav.append(html_output)

    return pages_nav

def gen_content(html_template_file, pages, content_json):
    with open(html_template_file, 'r') as content_file:
        html_template = content_file.read()

    contents = []

    dict_tmp = {}

    for key in content_json:
        dict_tmp[key.replace(" ", "_")] = content_json[key]

    content_json = dict_tmp

    for current_page in pages:
        html_output = ""

        content_obj = content_json[current_page["name"].replace(" ", "_")]

        for content in content_obj:
            html_temp = html_template
            
            for key in content:
                if type(content[key]) is list:
                    tmp_content = ''.join('<div>{0}</div>'.format(w) for w in content[key])
                else:
                    tmp_content = content[key]
                html_temp = html_temp.replace("{" + key + "}", tmp_content)

            html_output += html_temp

        contents.append(html_output)
    
    return contents

work_directory = os.getcwd()

if len(sys.argv) <= 3:
    print("Usage example: python static_build.py categories.json items.json dist/index.html https://www.myportfolio.com")
else:
    print("\n Static site builder :\n")

    json_pages = sys.argv[1]
    json_content = sys.argv[2]
    html_file = sys.argv[3]
    site_url = sys.argv[4]

    (json_pages_name, tmp_ext) = os.path.splitext(json_pages)
    
    pages_nav_html_arr = []
    contents_html_arr = []

    html_template_file = "template/" + json_pages_name + ".html"

    # read pages; JSON file
    with open("json/" + json_pages) as data_file:    
        data = json.load(data_file)

    pages = data["pages"]

    print("   Generating nav. data...")

    # generate HTML nav. data per pages
    if os.path.isfile(html_template_file):
        pages_nav_html_arr = gen_nav_menu(html_template_file, pages)
    
    # read content; JSON file
    with open("json/" + json_content) as data_file:    
        data = json.load(data_file)

    (json_content_name, tmp_ext) = os.path.splitext(json_content)

    html_template_file = "template/" + json_content_name + ".html"

    print("   Generating content data...\n")

    # generate HTML content data per pages
    if os.path.isfile(html_template_file):
        contents_html_arr = gen_content(html_template_file, pages, data)
    
    # read HTML skeleton
    content = ""

    with codecs.open(filename=html_file, mode='r', encoding='UTF-8') as f:
        for line in f:
            content += line
        f.close()

    # search & replace date tag
    today = datetime.date.today()
    today_formatted = today.strftime('%b %d, %Y')

    content = content.replace("{date}", today_formatted)

    index = 0
    
    # construct all HTML pages + sitemap from the informations gathered
    urlset_xml = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    url_tag_xml = ET.SubElement(urlset_xml, "url")
    loc_tag_xml = ET.SubElement(url_tag_xml, "loc")
    loc_tag_xml.text = site_url + "/"
    lastmod_tag_xml = ET.SubElement(url_tag_xml, "lastmod")
    lastmod_tag_xml.text = today.strftime('%Y-%m-%d')
    changefreq_tag_xml = ET.SubElement(url_tag_xml, "changefreq")
    changefreq_tag_xml.text = "monthly"
    priority_tag_xml = ET.SubElement(url_tag_xml, "priority")
    priority_tag_xml.text = "1.00"

    for page_name in pages:
        page_name = page_name["name"].replace(" ", "_")

        page_filename = "dist/" + page_name + ".html"

        print("   Constructing page '" + page_filename + "'")

        temp_content = content

        temp_content = temp_content.replace("{" + json_pages_name + "}", pages_nav_html_arr[index])
        temp_content = temp_content.replace("{" + json_content_name + "}", contents_html_arr[index])

        f = codecs.open(filename=page_filename, mode='w', encoding='UTF-8')
        f.write(temp_content)
        f.close()

        index += 1

        # sitemap
        url_tag_xml = ET.SubElement(urlset_xml, "url")
        loc_tag_xml = ET.SubElement(url_tag_xml, "loc")
        loc_tag_xml.text = site_url + "/" + page_name + ".html"
        lastmod_tag_xml = ET.SubElement(url_tag_xml, "lastmod")
        lastmod_tag_xml.text = today.strftime('%Y-%m-%d')
        changefreq_tag_xml = ET.SubElement(url_tag_xml, "changefreq")
        changefreq_tag_xml.text = "monthly"
        priority_tag_xml = ET.SubElement(url_tag_xml, "priority")
        priority_tag_xml.text = "1.00"

    # construct sitemap for downloadable documents as well
    print("\n   Producing sitemap...")

    filenames_list = []
    for (dirpath, dirnames, filenames) in os.walk("dist/get/"):
        filenames = [dirpath.replace("dist/", "") + s for s in filenames]
        filenames_list.extend(filenames)
        break
    
    for filename in filenames_list:
        url_tag_xml = ET.SubElement(urlset_xml, "url")
        loc_tag_xml = ET.SubElement(url_tag_xml, "loc")
        loc_tag_xml.text = site_url + "/" + filename
        lastmod_tag_xml = ET.SubElement(url_tag_xml, "lastmod")
        lastmod_tag_xml.text = today.strftime('%Y-%m-%d')
        changefreq_tag_xml = ET.SubElement(url_tag_xml, "changefreq")
        changefreq_tag_xml.text = "monthly"
        priority_tag_xml = ET.SubElement(url_tag_xml, "priority")
        priority_tag_xml.text = "1.00"
    
    tree = ET.ElementTree(urlset_xml)
    tree.write("dist/sitemap.xml", encoding='utf-8', xml_declaration=True)

    print("\n Done.")
