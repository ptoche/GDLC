"""Validate xml structure
Status: In Progress

Reference: https://lxml.de/validation.html

""" 
import bs4
from bs4 import BeautifulSoup, Tag, PageElement

def validate_xml(file :str, url=None) -> bool:
    """
    Args:
        file (str): path/to/xml/file
        url (str): url/to/xsd/schema/file
    Returns:
        True if the file was validated, False otherwise.
    Modules: lxml (etree, objectivity), lxml.etree (XMLSyntaxError)
    Notes:
        XHTML is a markup language that is designed by combining XML and HTML. 
        XHTML can be seen as a cleaner version of HTML, which is also stricter than HTML. 
        XHTML is a W3C recommendation. 
    """
    from lxml import etree, objectify
    from lxml.etree import XMLSyntaxError
    if not url:
        url = 'http://www.w3.org/2001/xml.xsd'
    with open(file, 'rb') as xml:
        xml = xml.read()
        try:
            schema = etree.XMLSchema(etree.parse(url))
            parser = objectify.makeparser(schema=schema)
            objectify.fromstring(xml, parser)
            print('xml file ', file, 'has been validated.')
            return True
        except XMLSyntaxError as error:
            print('xml file', file, 'was not validated.\n')
            print('The following error occurred:\n\n', error)
            return False



file = '/Users/PatrickToche/GDLC/output/GDLC_processed/mobi8/OEBPS/Text/part0150.xhtml'
validate_xml(file)
