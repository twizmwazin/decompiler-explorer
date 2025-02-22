import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


BOOMERANG_INSTALL = Path(os.getenv("BOOMERANG_INSTALL_PATH", "/usr/bin"))
BOOMERANG_CLI = BOOMERANG_INSTALL / 'boomerang-cli'


def main():
    tempdir = tempfile.TemporaryDirectory()

    conts = sys.stdin.buffer.read()
    infile = tempfile.NamedTemporaryFile(dir=tempdir.name, delete=False)
    infile.write(conts)
    infile.flush()

    decomp = subprocess.run([BOOMERANG_CLI, infile.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    infile.close()

    sys.stdout.buffer.write(b'<pre>')
    outputs = Path('output') / Path(infile.name).name
    for source in outputs.glob('*.c'):
        with open(source, 'rb') as f:
            sys.stdout.buffer.write(f.read())

    sys.stdout.buffer.write(b'</pre>')

    shutil.rmtree(tempdir.name)


def version():
    proc = subprocess.run([BOOMERANG_CLI, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # boomerang-cli v0.5.2
    output = proc.stdout.decode()
    assert output.startswith('boomerang-cli ')
    version = output.split(' ')[1]
    assert version.startswith('v')
    version = version[1:]

    print(version)
    print()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--name':
        print('Boomerang')
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        version()
        sys.exit(0)

    main()
