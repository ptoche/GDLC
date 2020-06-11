"""
Invoke lxml.etree to check validity of XHTML documents.

    conda install -n myenv -c conda-forge tidy-html5
    conda install -n myenv -c conda-forge lxml

To pass a string:
    from io import StringIO
and wrap the string with StringIO(string)

Note: XHTML is best parsed as XML.

Available boolean keyword arguments:

    attribute_defaults - read the DTD (if referenced by the document) and add the default attributes from it
    dtd_validation - validate while parsing (if a DTD was referenced)
    load_dtd - load and parse the DTD while parsing (no validation is performed)
    no_network - prevent network access when looking up external documents (on by default)
    ns_clean - try to clean up redundant namespace declarations
    recover - try hard to parse through broken XML
    remove_blank_text - discard blank text nodes between tags, also known as ignorable whitespace. This is best used together with a DTD or schema (which tells data and noise apart), otherwise a heuristic will be applied.
    remove_comments - discard comments
    remove_pis - discard processing instructions
    strip_cdata - replace CDATA sections by normal text content (on by default)
    resolve_entities - replace entities by their text value (on by default)
    huge_tree - disable security restrictions and support very deep trees and very long text content (only affects libxml2 2.7+)
    compact - use compact storage for short text content (on by default)
    collect_ids - collect XML IDs in a hash table while parsing (on by default). Disabling this can substantially speed up parsing of documents with many different IDs if the hash lookup is not used afterwards.

Other keyword arguments:

    encoding - override the document encoding
    target - a parser target object that will receive the parse events (see The target parser interface)
    schema - an XMLSchema to validate against (see validation)
"""
import os
from lxml import etree

dir = '/Users/PatrickToche/GDLC/output/GDLC_processed/mobi8/OEBPS/Text'
file = os.path.join(dir, 'part0000.xhtml')
base, ext = os.path.splitext(file)
outfile = base + '_clean' + ext

parser = etree.XMLParser(encoding='utf-8', recover=True, ns_clean=True, remove_blank_text=True, remove_comments=True, remove_pis=True, strip_cdata=True)
with open(file, encoding='utf8') as infile, open(outfile, 'w') as fixed:
    if os.path.isfile(file):
        tree = etree.parse(infile.read(), parser)
        # tree = etree.parse(StringIO(infile))
        error = parser.error_log[0]
        print(error.message, 'line = ', error.line, 'column = ', error.column)
        result = etree.tostring(tree.getroot(), pretty_print=True, method='xml')
        
    print(root, file=fixed)



# from: https://github.com/voipir/python-sii/tree/master/src/sii/lib/validation.py
def validate_schema(doc_xml, schema_xml=None):
    """ Validate XML against its XSD Schema definition provided by the SII.

    :param `lxml.etree.Element` doc_xml: Handle to XML etree root node.
    """
    doc_xml = deepcopy(doc_xml)

    doc_new    = etree.Element(doc_xml.tag, nsmap={None: 'http://www.sii.cl/SiiDte'})
    doc_new[:] = doc_xml[:]                # move children into new root
    doc_new.attrib.update(doc_xml.attrib)  # copy attributes of the root node

    # reload xml
    buff = BytesIO(etree.tostring(doc_new, method='c14n'))
    xml  = etree.parse(buff).getroot()

    if not schema_xml:
        schema_pth = resolve_schema(doc_xml)

        with open(schema_pth, 'rb') as fh:
            schema_xml = etree.parse(fh)

    schema = etree.XMLSchema(schema_xml)
    schema.assertValid(xml)

    return True  # if no assertion gets thrown above, we can safely assume a `True` validity. 