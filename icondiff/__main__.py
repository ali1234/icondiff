import argparse
import subprocess
import pathlib

from icondiff.svgtopng import svgtopng

bootstrap_path = pathlib.Path(__file__).parent / 'css' / 'bootstrap.min.css'


def git_export(repository, commit):
    print('Exporting', commit)
    cmd = 'git -C {repository} archive --prefix={commit}/ {commit} | tar -x'
    return subprocess.check_call([
            '/bin/sh', '-c', cmd.format(repository=repository, commit=commit)
    ])


def gen_pngs(dir):
    path = pathlib.Path(dir)
    print('Generating pngs for', path)
    for child in path.iterdir():
        if not child.is_symlink() and child.suffix == '.svg':
            try:
                svgtopng(child)
            except Exception as e:
                print('File skipped:', e)
        elif child.is_dir():
            gen_pngs(child)


def scan_pngs(topdir, dir=None):
    if dir == None:
        dir = topdir
    path = pathlib.Path(dir)
    for child in path.iterdir():
        if not child.is_symlink() and child.suffix == '.png':
            yield child.relative_to(topdir)
        elif child.is_dir():
            yield from scan_pngs(topdir, child)


def scan_dirs(dirs):
    for dir in dirs:
        yield from scan_pngs(dir)


def diff_paths(paths):
    first = paths[0].read_bytes()
    for p in paths[1:]:
        if p.read_bytes() != first:
            return True
    return False


def diff_pngs(dirs, all=False):
    it = sorted(list(set(scan_dirs(dirs))))
    if all:
        yield from it
        return
    for png in it:
        paths = [(dir / png) for dir in dirs]
        if any(not p.exists for p in paths):
            yield png
        elif len(set(p.stat().st_size for p in paths)) > 1:
            yield png
        elif diff_paths(paths):
            yield png


def html_img(path):
    return '<img src="{}">'.format(str(path))


def gen_diff(commits, all=False):
    count = 0
    with open('diff.html', 'w') as diff:
        diff.write('<html><head><title>diff {}</title>\n'.format(' - '.join(commits)))
        diff.write('<link rel="stylesheet" href="{}">'.format(bootstrap_path))

        diff.write('</head><body>\n')
        diff.write('<table class="table table-striped">\n')
        diff.write('<tr><th>Filename</th><th>{}</th></tr>\n'.format('</th><th>'.join(commits)))

        for different in diff_pngs(commits, all):
            count +=1
            diff.write('<tr><td>{}</td><td>{}</td>\n'.format(str(different), '</td><td>'.join(html_img(commit / different) for commit in commits)))

        diff.write('</table>\n')
        diff.write('{} differences.'.format(count))

        diff.write('</body></html>')


def main():

    parser = argparse.ArgumentParser(description='Visually diff SVG icons.')
    parser.add_argument('repository', metavar='repository', type=str,
                        help='Path to Git repository.')
    parser.add_argument('commits', metavar='commit', type=str, nargs='+',
                        help='Git commits.')
    parser.add_argument('-a', '--all', action='store_true',
                        help="Don't skip identical files.")

    args = parser.parse_args()
    for commit in args.commits:
        git_export(args.repository, commit)
        gen_pngs(commit)
    gen_diff(args.commits, len(args.commits)==1 or args.all)


if __name__ == '__main__':
    main()