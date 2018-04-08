import pathlib
import os

import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

def svgtopng(filename, default_size=64, force_default_size=False):
    path = pathlib.Path(filename)
    if not path.exists:
        raise Exception('File does not exist: {}'.format(path))
    if not path.suffix == '.svg':
        raise Exception('Not an svg file: {}'.format(path))

    dest = path.parent / (path.stem + '.png')

    if path.is_symlink():
        target = pathlib.Path(os.readlink(str(path)))
        target = target.parent / (target.stem + '.png')
        dest.symlink_to(target)
        return

    if force_default_size:
        size = default_size
    else:
        try:
            size = int(path.parent.name)
        except ValueError:
            if default_size is None:
                raise Exception('Unable to extract icon size from directory name: {}'.format(path))
            else:
                size = default_size

    pix = GdkPixbuf.Pixbuf.new_from_file (str(path))
    if pix:
        if GdkPixbuf.Pixbuf.get_width(pix) > size or GdkPixbuf.Pixbuf.get_height(pix) > size:
            raise Exception('Size is too big: {}'.format(path))

        if not GdkPixbuf.Pixbuf.savev(pix, str(dest), "png", [], []):
            raise Exception('Could not save file: {}'.format(dest))
    else:
        raise Exception('Could not load file: {}'.format(path))



def main():
    import sys
    for filename in sys.argv[1:]:
        svgtopng(filename)

if __name__ == '__main__':
    main()