#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File and Path operations

Kodi xbmc*.*() functions usually take utf-8 encoded commands, thus try_encode
works.
Unfortunatly, working with filenames and paths seems to require an encoding in
the OS' getfilesystemencoding - it will NOT always work with unicode paths.
However, sys.getfilesystemencoding might return None.
Feed unicode to all the functions below and you're fine.

WARNING: os.path won't really work with smb paths (possibly others). For
xbmcvfs functions to work with smb paths, they need to be both in passwords.xml
as well as sources.xml
"""
from __future__ import absolute_import, division, unicode_literals
import shutil
import os
from os import path  # allows to use path_ops.path.join, for example
from distutils import dir_util
import xbmc
import xbmcvfs

from .tools import unicode_paths

# Kodi seems to encode in utf-8 in ALL cases (unlike e.g. the OS filesystem)
KODI_ENCODING = 'utf-8'


def encode_path(path):
    """
    Filenames and paths are not necessarily utf-8 encoded. Use this function
    instead of try_encode/trydecode if working with filenames and paths!
    (os.walk only feeds on encoded paths. sys.getfilesystemencoding returns None
    for Raspberry Pi)
    """
    return unicode_paths.encode(path)


def decode_path(path):
    """
    Filenames and paths are not necessarily utf-8 encoded. Use this function
    instead of try_encode/trydecode if working with filenames and paths!
    (os.walk only feeds on encoded paths. sys.getfilesystemencoding returns None
    for Raspberry Pi)
    """
    return unicode_paths.decode(path)


def translate_path(path):
    """
    Returns the XBMC translated path [unicode]
    e.g. Converts 'special://masterprofile/script_data'
    -> '/home/user/XBMC/UserData/script_data' on Linux.
    """
    translated = xbmc.translatePath(path.encode(KODI_ENCODING, 'strict'))
    return translated.decode(KODI_ENCODING, 'strict')


def exists(path):
    """
    Returns True if the path [unicode] exists. Folders NEED a trailing slash or
    backslash!!
    """
    return xbmcvfs.exists(path.encode(KODI_ENCODING, 'strict')) == 1


def rmtree(path, *args, **kwargs):
    """Recursively delete a directory tree.

    If ignore_errors is set, errors are ignored; otherwise, if onerror
    is set, it is called to handle the error with arguments (func,
    path, exc_info) where func is os.listdir, os.remove, or os.rmdir;
    path is the argument to that function that caused it to fail; and
    exc_info is a tuple returned by sys.exc_info().  If ignore_errors
    is false and onerror is None, an exception is raised.

    """
    return shutil.rmtree(encode_path(path), *args, **kwargs)


def copyfile(src, dst):
    """Copy data from src to dst"""
    return shutil.copyfile(encode_path(src), encode_path(dst))


def makedirs(path, *args, **kwargs):
    """makedirs(path [, mode=0777])

    Super-mkdir; create a leaf directory and all intermediate ones. Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist.  This is recursive.
    """
    return os.makedirs(encode_path(path), *args, **kwargs)


def remove(path):
    """
    Remove (delete) the file path. If path is a directory, OSError is raised;
    see rmdir() below to remove a directory. This is identical to the unlink()
    function documented below. On Windows, attempting to remove a file that is
    in use causes an exception to be raised; on Unix, the directory entry is
    removed but the storage allocated to the file is not made available until
    the original file is no longer in use.
    """
    return os.remove(encode_path(path))


def walk(top, topdown=True, onerror=None, followlinks=False):
    """
    Directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 3-tuple

        dirpath, dirnames, filenames

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name).

    If optional arg 'topdown' is true or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top down).  If topdown is false, the triple
    for a directory is generated after the triples for all of its
    subdirectories (directories are generated bottom up).

    When topdown is true, the caller can modify the dirnames list in-place
    (e.g., via del or slice assignment), and walk will only recurse into the
    subdirectories whose names remain in dirnames; this can be used to prune the
    search, or to impose a specific order of visiting.  Modifying dirnames when
    topdown is false is ineffective, since the directories in dirnames have
    already been generated by the time dirnames itself is generated. No matter
    the value of topdown, the list of subdirectories is retrieved before the
    tuples for the directory and its subdirectories are generated.

    By default errors from the os.listdir() call are ignored.  If
    optional arg 'onerror' is specified, it should be a function; it
    will be called with one argument, an os.error instance.  It can
    report the error to continue with the walk, or raise the exception
    to abort the walk.  Note that the filename is available as the
    filename attribute of the exception object.

    By default, os.walk does not follow symbolic links to subdirectories on
    systems that support them.  In order to get this functionality, set the
    optional argument 'followlinks' to true.

    Caution:  if you pass a relative pathname for top, don't change the
    current working directory between resumptions of walk.  walk never
    changes the current directory, and assumes that the client doesn't
    either.

    Example:

    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/email'):
        print root, "consumes",
        print sum([getsize(join(root, name)) for name in files]),
        print "bytes in", len(files), "non-directory files"
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

    """
    # Get all the results from os.walk and store them in a list
    walker = list(os.walk(encode_path(top),
                          topdown,
                          onerror,
                          followlinks))
    for top, dirs, nondirs in walker:
        yield (decode_path(top),
               [decode_path(x) for x in dirs],
               [decode_path(x) for x in nondirs])


def copy_tree(src, dst, *args, **kwargs):
    """
    Copy an entire directory tree 'src' to a new location 'dst'.

    Both 'src' and 'dst' must be directory names.  If 'src' is not a
    directory, raise DistutilsFileError.  If 'dst' does not exist, it is
    created with 'mkpath()'.  The end result of the copy is that every
    file in 'src' is copied to 'dst', and directories under 'src' are
    recursively copied to 'dst'.  Return the list of files that were
    copied or might have been copied, using their output name.  The
    return value is unaffected by 'update' or 'dry_run': it is simply
    the list of all files under 'src', with the names changed to be
    under 'dst'.

    'preserve_mode' and 'preserve_times' are the same as for
    'copy_file'; note that they only apply to regular files, not to
    directories.  If 'preserve_symlinks' is true, symlinks will be
    copied as symlinks (on platforms that support them!); otherwise
    (the default), the destination of the symlink will be copied.
    'update' and 'verbose' are the same as for 'copy_file'.
    """
    src = encode_path(src)
    dst = encode_path(dst)
    return dir_util.copy_tree(src, dst, *args, **kwargs)


def basename(path):
    """
    Returns the filename for path [unicode] or an empty string if not possible.
    Safer than using os.path.basename, as we could be expecting \\ for / or
    vice versa
    """
    try:
        return path.rsplit('/', 1)[1]
    except IndexError:
        try:
            return path.rsplit('\\', 1)[1]
        except IndexError:
            return ''
