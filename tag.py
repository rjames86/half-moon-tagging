"""tag - Mavericks command line tool for tagging files

Usage:
  tag --list <path>...
  tag --add <tag> <path>...
  tag --set <tag> <path>...
  tag --remove <tag> <path>...
  tag (-h | --help)
  tag --version

Options:
  -l --list          List all tags at each path
  -a --add=<tag>     Add one or more (comma separated) tags to paths
  -s --set=<tag>     Set one or more (comma separated) tags on paths
  -r --remove=<tag>  Remove one or more (comma separated) tags from paths
  -h --help          Show this screen.
  --version          Show version.
"""

__author__ = 'schwa'

from docopt import docopt
import Foundation

NSURLTagNamesKey = 'NSURLTagNamesKey'

def get_tags(path):
    url = Foundation.NSURL.fileURLWithPath_(path)
    metadata, error = url.resourceValuesForKeys_error_([ NSURLTagNamesKey ], None)
    if not metadata:
        return []
    if NSURLTagNamesKey not in metadata:
        return []
    return metadata[NSURLTagNamesKey]

def set_tags(path, tags):
    url = Foundation.NSURL.fileURLWithPath_(path)
    result, error = url.setResourceValue_forKey_error_(tags, NSURLTagNamesKey, None)
    if not result:
        raise Exception('Could not set tags', error.encode('ascii', 'ignore'))

def add_tag(path, tag):
    tags = get_tags(path)
    if tag in tags:
        return
    set_tags(path, tags)

def add_tags(path, tags):
    if not tags:
        return
    old_tags = get_tags(path)
    new_tags = old_tags + [tag for tag in tags if tag not in old_tags]
    set_tags(path, new_tags)

def remove_tag(path, tag):
    tags = get_tags(path)
    for tag in tags:
        tags.remove(tag)
    set_tags(path, tags)

def remove_tags(path, tags):
    old_tags = get_tags(path)
    new_tags = [tag for tag in old_tags if tag not in tags]
    set_tags(path, new_tags)

def split_tags(s):
    tags = s.split(',')
    tags = [tag.strip() for tag in tags]
    return tags

def main(argv = None):
    #argv = shlex.split(raw_input('$ tag '))
    arguments = docopt(__doc__, argv = argv, version='tag 1.0a1')
    if arguments['--list']:
        for path in arguments['<path>']:
            print '{} ({})'.format(path, ', '.join(get_tags(path)))
    elif arguments['--add']:
        tags = split_tags(arguments['--add'])
        for path in arguments['<path>']:
            add_tags(path, tags)
    elif arguments['--set']:
        tags = split_tags(arguments['--set'])
        for path in arguments['<path>']:
            set_tags(path, tags)
    elif arguments['--remove']:
        tags = split_tags(arguments['--remove'])
        for path in arguments['<path>']:
            remove_tags(path, tags)

if __name__ == '__main__':
    main()
