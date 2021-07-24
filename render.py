from jinja2 import Environment, FileSystemLoader
from json import load
import os
import timeago, datetime
from slugify import slugify
import yaml
path = 'posts/'
files = []
posts = []
with open('config.json') as config_file:
    config = load(config_file)

# go through all posts and generate each blog post file
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for yaml_file in f:
        if '.yaml' in yaml_file:# check for yaml format
            with open(path+yaml_file) as file:
                docs = yaml.load_all(file, Loader=yaml.FullLoader) # load file
                for doc in docs:
                    doc['link'] = slugify(doc['title'])+'.html'
                    doc['date'] = timeago.format(doc['date'], datetime.datetime.now())
                    doc['url'] = "{}/{}".format(config['site_url'], doc['link'])
                    doc['image'] = "{}/assets/{}".format(config['site_url'], doc['image'])
                    posts.append(doc)
                    template_env = Environment(loader=FileSystemLoader(searchpath='./'))
                    template = template_env.get_template('layout/blogdetail.html')
                    with open("build/{}.html".format(slugify(doc['title'])), 'w') as output_file:
                        output_file.write(
                            template.render(
                                site=config,
                                blog=doc
                            )
                        )



template_env = Environment(loader=FileSystemLoader(searchpath='./'))
template = template_env.get_template('layout/index.html')
with open('build/index.html', 'w') as output_file:
    output_file.write(
        template.render(
            site=config,
            blogs=posts
        )
    )
exit()












