from python.encoder import get_properties
from clrprint import clrprint
import re

import main # NOTE This forces the list of processes to update
# TODO --> Link to git push somehow

def update_readme(property_values):
    with open('meta/template.md', 'r', encoding='utf8') as f:
        template = f.read()
        template = re.sub('\.\.\/', '', template)
        with open('README.md', 'w', encoding='utf8') as r:
            props = [var.strip() for var in re.findall('{\!(.+?)\!}', template)]
            for prop in props:
                if not (prop in property_values):
                    continue
                pattern = "{!\s*" + prop + "\s*!}"
                template = re.sub(pattern, property_values[prop], template)
            r.write(template)

if __name__ == "__main__":
    update_readme(get_properties())
    clrprint(
        "[", "Done", "] Updated '", "README", ".", "md","'",
        clr="w,g,w,b,w,b,w",
        sep="")