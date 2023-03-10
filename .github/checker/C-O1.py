import re

import vera
from utils import get_filename

# Inspired by
# https://github.com/github/gitignore/blob/master/C.gitignore
# https://github.com/github/gitignore/blob/master/Gcov.gitignore
_UNWANTED_FILES_REGEXES = [
    # Prerequisites
    re.compile(r'.*\.d$'),

    # Object files
    re.compile(r'.*\.o$'),
    re.compile(r'.*\.ko$'),
    re.compile(r'.*\.obj$'),
    re.compile(r'.*\.elf$'),

    # Linker output
    re.compile(r'.*\.ilk$'),
    re.compile(r'.*\.map$'),
    re.compile(r'.*\.exp$'),

    # Precompiled Headers
    re.compile(r'.*\.gch$'),
    re.compile(r'.*\.pch$'),

    # Libraries
    re.compile(r'.*\.lib$'),
    re.compile(r'.*\.a$'),
    re.compile(r'.*\.la$'),
    re.compile(r'.*\.lo$'),

    # Shared objects (inc. Windows DLLs)
    re.compile(r'.*\.dll$'),
    re.compile(r'.*\.so$'),
    re.compile(r'.*\.so\..*$'),
    re.compile(r'.*\.dylib$'),

    # Executables
    re.compile(r'.*\.exe$'),
    re.compile(r'.*\.out$'),
    re.compile(r'.*\.app$'),
    re.compile(r'.*\.i.*86$'),
    re.compile(r'.*\.x86_64$'),
    re.compile(r'.*\.hex$'),

    # Debug files
    re.compile(r'.*\.su$'),
    re.compile(r'.*\.idb$'),
    re.compile(r'.*\.pdb$'),

    # Kernel Module Compile Results
    re.compile(r'.*\.mod.*$'),
    re.compile(r'.*\.cmd$'),
    re.compile(r'^modules\.order$'),
    re.compile(r'^Module\.symvers$'),
    re.compile(r'^Mkfile\.old$'),
    re.compile(r'^dkms\.conf$'),

    # gcc coverage testing tool files
    re.compile(r'.*\.gcno$'),
    re.compile(r'.*\.gcda$'),
    re.compile(r'.*\.gcov$'),

    # Temporary files
    re.compile(r'.*~.*'),
    re.compile(r'.*#.*'),

    # Valgrind core dump files
    re.compile(r'^vgcore\.\d+$')
]

_UNWANTED_BINARY_MAGIC = [
    # ELF
    b'\x7fELF',

    # EXE
    b'MZ',

    # Mach-O
    b'\xfe\xed\xfa\xce',

    # PE
    b'\x4d\x5a',
]


def is_unwanted_binary(file: str) -> bool:
    with open(file, 'rb') as f:
        first_line = f.readline()
        return any(first_line.startswith(magic) for magic in _UNWANTED_BINARY_MAGIC)


def check_delivery_files():
    for file in vera.getSourceFileNames():
        if is_unwanted_binary(file):
            vera.report(vera.Token(" ", 0, 1, "O1", file), "MAJOR:C-O1")
            continue
        file_name = get_filename(file)
        for regex in _UNWANTED_FILES_REGEXES:
            if regex.match(file_name):
                vera.report(vera.Token(" ", 0, 1, "O1", file), "MAJOR:C-O1")
                break


check_delivery_files()
