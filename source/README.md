## Overview

This directory contains directories and files used to generate the lookup dictionary with the KindleGen application. Some directories are empty, but are nevertheless needed by KindleGen. Some files are copied from the source without changes. Some files are edited. Minor edits include changes to title, author, hyperlinks, images. Major edits are in the content.opf, toc.ncx and all the xhtml files inside the Text sub-directory.

## Directory Structure

    Project
    ├── HDImages
    │   └── [empty]
    ├── mobi7
    │   ├── Images 
    │   │   ├── cover_image.jpg
    │   │   └── [more images]
    ├── mobi8
    │   ├── META-INF
    │   │   └── container.xml
    │   └── OEBPS
    │   │   ├── Fonts 
    │   │   │   └── [empty]
    │   │   ├── Images 
    │   │   │   ├── cover_image.jpg
    │   │   │   └── more images
    │   │   ├── Styles 
    │   │   │   ├── style0001.css
    │   │   │   ├── style0002.css
    │   │   │   └── style0003.css
    │   │   ├── Text     
    │   │   │   ├── cover_page.xhtml
    │   │   │   ├── part0000.xhtml
    │   │   │   └── [more xhtml]
    │   │   ├── content.opf
    │   │   ├── toc.ncx
    │   └── mimetype
    └── README.md

## Details

 - <Text> 
     directory containing the post-processed word files used to generate the lookup dictionary. 

- <Images>
    directories containing images used in the GDLC Kindle dictionary. They have been renamed to clarify their purpose. Copyrights may apply. 
    
 - <Styles>
     directory containing the css style files used with the xml files.

 - <Text>
     directory containing all the xhtml files needed to build the dictionary. These files have been thoroughly edited to support look-up.
 
 - content.opf
     file edited thoroughly to match the dictionary's meta information and structure.
 - container.xml 
     file copied without edits.
 - toc.ncx 
     file edited stlightly to reflect minor changes in content
     
## Note

The dictionary source files are based on [Gran Diccionari de la llengua catalana (Kindle Edition)](https://www.amazon.com/Gran-Diccionari-Llengua-Catalana-Catalan-ebook/dp/B00DZWFU), available for purchase from the Amazon website. The ebook was unpacked with the help of the `KindleUnpack` `calibre` plugin. The xhtml files were then edited to enable Kindle's look-up functionality. The code used to edit the files is hosted at [Project Location](https://github.com/ptoche/GDLC). This is a personal project currently unfit for distribution. 


Created 9 May 2020 with minor revisions since.

@author: Patrick TOCHE.