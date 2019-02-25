import os
import stat
import sys
import zipfile


__version__ = '0.1'


def add_directory(zip_file, path, zip_path):
    for item in sorted(os.listdir(path)):
        current_path = os.path.join(path, item)
        current_zip_path = os.path.join(zip_path, item)
        if os.path.isfile(current_path):
            add_file(zip_file, current_path, current_zip_path)
        else:
            add_directory(zip_file, current_path, current_zip_path)


def add_file(zip_file, path, zip_path=None):
    permission = 0o555 if os.access(path, os.X_OK) else 0o444
    zip_info = zipfile.ZipInfo.from_file(path, zip_path)
    zip_info.date_time = (2019, 1, 1, 0, 0, 0)
    zip_info.external_attr = (stat.S_IFREG | permission) << 16
    with open(path, 'rb') as fp:
        zip_file.writestr(zip_info, fp.read(),
                          compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    if sys.version_info < (3, 7):
        sys.stderr.write('This script requires python 3.7+.\n')
        return 1
    if len(sys.argv) < 3:
        print('Usage: {} ZIP_FILE PATH...'
              .format(os.path.basename(sys.argv[0])))
        return 1

    failure = False
    output_path = sys.argv[1]
    with zipfile.ZipFile(output_path, 'w') as zip_file:
        for path in sorted(sys.argv[2:]):
            if os.path.isdir(path):
                add_directory(zip_file, path, os.path.basename(path))
            elif os.path.isfile(path):
                add_file(zip_file, path, os.path.basename(path))
            else:
                sys.stderr.write('Invalid PATH: {}\n'.format(path))
                failure = True
                break

    if failure:
        os.unlink(output_path)
        return 1

    print('Wrote {}'.format(output_path))
    return 0
