#!/usr/bin/env python3

"""
Convert RSS feed to HTML/PDF
"""
import copy
import logging
import shutil
import random
from pathlib import Path

import requests
from xhtml2pdf import pisa
from jinja2 import Template
from bs4 import BeautifulSoup
from ebooklib import epub

from rss_reader.exceptions import RSSFeedException


class Converter:
    """ Class for conversion RSS feed

        Attributes:
            title (str): Title of RSS feed
            entries (list): List of RSS news
            out_dir (str): Directory where output will be saved
    """

    def __init__(self, title, entries, out_dir="out", image_dir="images", temp_image_dir="_temp_images"):
        self.title = title
        self.entries = entries
        self.out_dir = out_dir

        self.image_dir = image_dir
        self.temp_image_dir = temp_image_dir

        self.font_path = Path(__file__).resolve().parent / 'fonts/Roboto-Regular.ttf'

    def _create_directories(self, image_dir):
        """ Create directories if not exist (self.out_dir and self.out_dir/image_dir) """
        if not Path(self.out_dir).is_dir():
            logging.info("Creating directory /%s", Path(self.out_dir))
            Path(self.out_dir).mkdir(parents=True, exist_ok=True)

        if not image_dir.is_dir():
            logging.info("Creating directory /%s", image_dir)
            image_dir.mkdir(parents=True, exist_ok=True)

    def _download_image(self, url, image_dir):
        """ Download image in self.out_dir/image_dir

            Returns:
                filename: image name
        """
        logging.info("Starting image download")

        image_dir = Path(self.out_dir) / image_dir

        try:
            self._create_directories(image_dir)
        except OSError:
            raise RSSFeedException(message="Сan not create directory")

        filename = url.split('/')[-1]
        response = requests.get(url, allow_redirects=True)

        with open(image_dir / filename, 'wb') as handler:
            handler.write(response.content)

        return filename

    def _replace_urls_to_local_path(self, entry):
        """ Replace img URLs in entry.summary to local file path

            Args:
                entry (dict): News dict

        """
        soup = BeautifulSoup(entry.summary, "html.parser")

        for img in soup.findAll('img'):
            # use placeholder
            if not img['src']:
                # copy placeholder to self.out_dir/self.image_dir
                filename = Path(__file__).resolve().parent / 'placeholder/placeholder.jpg'
                shutil.copyfile(filename, Path(self.out_dir) / self.image_dir / 'placeholder.jpg')
                img['src'] = str(Path(self.image_dir) / 'placeholder.jpg')
                entry.summary = str(soup)
                return entry

            filename = self._download_image(img['src'], self.image_dir)
            downloaded_img_local_path = Path(self.image_dir) / filename

            img['src'] = str(downloaded_img_local_path)
            entry.summary = str(soup)

        return entry

    def _replace_urls_to_absolute_path(self, entry):
        """ Replace img URLs in entry.summary to local absolute file path

            Special for xhtml2pdf (xhtml2pdf support only absolute file path)

            Args:
                entry (dict): News dict
        """
        soup = BeautifulSoup(entry.summary, "html.parser")

        for img in soup.findAll('img'):
            # use placeholder
            if not img['src']:
                filename = Path(__file__).resolve().parent / 'placeholder/placeholder.jpg'
                img['src'] = str(filename.absolute())
                entry.summary = str(soup)
                return entry

            filename = self._download_image(img['src'], self.temp_image_dir)
            downloaded_img_absolute_path = (Path(self.out_dir) / self.temp_image_dir / filename).absolute()

            img['src'] = str(downloaded_img_absolute_path)
            entry.summary = str(soup)

        return entry

    def _generate_html(self, is_cyrillic_font=False, is_absolute_path=False):
        """ Generate HTML

            Args:
                is_cyrillic_font (bool) Should we generate HTML with cyrillic_font (to convert to PDF)?
                is_absolute_path (bool): Should we generate HTML with absolute image PATH (to convert to PDF)?

            Returns:
                html: String with HTML code
        """
        template = '''<html>
            <head>
                <meta charset="utf-8">
                <title>{{title}}</title>
                
                <style type=text/css>
                    {% if is_cyrillic_font %}
                    @font-face { font-family: Roboto; src: url({{font_path}}), ; }
                    {% endif %}
                    body{
                      font-family: Roboto;
                    }
                    div 
                    { 
                      {% if is_cyrillic_font %}
                      margin: 2px;
                      font-size: 15px; 
                      {% else %}
                      margin: 20px;
                      font-size: 18px; 
                      {% endif %}
                    }
                </style> 
            </head>
            <body>
                {% for entry in entries %}
                    <div class='entry'>
                        <h2 class='title'>{{entry.title}}</h2>
                        <p><span class='date'>{{entry.published}}</span></p>
                        <p><a class='link' href='{{entry.link}}'>{{entry.link}}</a></p>
                        <div class='description'>{{entry.summary}}</div>
                    </div>
                {% endfor %}
            </body>
        </html>'''

        # replacing image url to downloaded image path
        temp_entries = copy.deepcopy(self.entries)
        if is_absolute_path:
            entries = [self._replace_urls_to_absolute_path(entry) for entry in temp_entries]
        else:
            entries = [self._replace_urls_to_local_path(entry) for entry in temp_entries]

        html = Template(template).render(title=self.title, entries=entries,
                                         is_cyrillic_font=is_cyrillic_font, font_path=self.font_path)
        return html

    def entries_to_html(self):
        """ Generate HTML file in self.out_dir """
        html = self._generate_html()

        with open(Path(self.out_dir) / 'out.html', 'w') as file_object:
            file_object.write(html)

    def entries_to_pdf(self):
        """ Generate PDF file in self.out_dir """
        html = self._generate_html(is_cyrillic_font=True, is_absolute_path=True)

        with open(Path(self.out_dir) / 'out.pdf', 'w+b') as file:
            pdf = pisa.CreatePDF(html, dest=file, encoding='UTF-8')

        # Delete temp folder (self.out_dir/self.temp_image_dir)
        temp_img_dir = Path(self.out_dir) / self.temp_image_dir
        logging.info("Cleaning up %s", temp_img_dir)
        shutil.rmtree(temp_img_dir)

        if pdf.err:
            raise RSSFeedException(message="Error during PDF generation")

    def entries_to_epub(self):
        """ Generate EPUB file in self.out_dir """
        html = self._generate_html()

        def add_images_to_book():
            soup = BeautifulSoup(chapter.content, "html.parser")
            image_urls = [img['src'] for img in soup.findAll('img') if img.has_attr('src')]

            added_images = []
            for image_url in image_urls:
                # Images can repeat, check
                if image_url in added_images:
                    continue

                added_images.append(image_url)
                img_local_filename = Path(self.out_dir) / image_url

                with open(img_local_filename, 'br') as file_object:
                    epimg = epub.EpubImage()
                    epimg.file_name = image_url
                    epimg.set_content(file_object.read())

                    book.add_item(epimg)

        book = epub.EpubBook()

        # set metadata
        book.set_identifier(f'id{random.randint(100000, 999999)}')
        book.set_title(self.title)
        book.set_language('en, ru')
        book.add_author('rss-reader')

        # create chapter
        chapter = epub.EpubHtml(title='Intro', file_name=f'chap_01.xhtml', lang='en, ru')
        chapter.content = html
        # add images
        add_images_to_book()
        # add chapter
        book.add_item(chapter)

        # define Table Of Contents
        book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
                    (epub.Section(self.title),
                     (chapter,))
                    )
        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        # add CSS file
        book.add_item(nav_css)
        # basic spine
        book.spine = ['nav', chapter]

        # write to the file
        epub.write_epub(Path(self.out_dir) / 'out.epub', book, {})
