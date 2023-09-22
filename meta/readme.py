import re

def update_readme(property_values):
    with open('meta/template.md', 'r', encoding='utf8') as f:
        template = f.read()
        with open('README.md', 'w', encoding='utf8') as r:
            props = [var.strip() for var in re.findall('{\!(.+?)\!}', template)]
            for prop in props:
                if not (prop in property_values):
                    continue
                pattern = "{!\s*" + prop + "\s*!}"
                template = re.sub(pattern, property_values[prop], template)
            r.write(template)