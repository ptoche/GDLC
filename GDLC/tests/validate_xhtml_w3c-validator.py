"""
Pure Python command line for HTML validation using W3C online validator.

    pip install -U Online-W3C-Validator

https://github.com/nad2000/W3C-Validator
"""
from w3c_validator import validate
file = '/Users/PatrickToche/GDLC/output/GDLC_processed/mobi8/OEBPS/Text/part0000.xhtml' 
with open(file, encoding='utf8') as infile:
    # print(infile.readlines()[:10])  # check that the file is properly opened
    messages = validate(infile)["messages"]
    for m in messages:
        print("Type: %(type)s, Line: %(lastLine)d, Description: %(message)s" % m)


# Traceback (most recent call last):

#   File "<ipython-input-24-3004e5ab8683>", line 3, in <module>
#     messages = validate(infile)["messages"]

#   File "/Users/patricktoche/miniconda3/envs/sp/lib/python3.8/site-packages/w3c_validator/validator.py", line 41, in validate
#     is_remote = filename.startswith("http://") or filename.startswith(

# AttributeError: '_io.TextIOWrapper' object has no attribute 'startswith'

