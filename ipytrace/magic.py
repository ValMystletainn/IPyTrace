import inspect
import os
from typing import TYPE_CHECKING

from IPython.core.getipython import get_ipython
from IPython.core.oinspect import (
    find_file,
    find_source_lines,
    getdoc,
    getsource,
    indent,
)
from IPython.display import publish_display_data
from IPython.utils import openpy

if TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.oinspect import Inspector


def _pinfo(obj, detail_level: int = 0):
    shell = get_ipython()  # type: InteractiveShell
    inspector = shell.inspector # type: Inspector
    mime_dict = inspector._get_info(obj, detail_level=detail_level)
    # TODO show by config
    if 'text/html' in mime_dict:
        mime_dict.pop('text/html')

    publish_display_data(mime_dict)

def pinfo(obj):
    _pinfo(obj, detail_level=0)

def pinfo2(obj):
    _pinfo(obj, detail_level=1)

def pdef(obj, oname='func'):
    shell = get_ipython()  # type: InteractiveShell
    inspector = shell.inspector # type: Inspector
    inspector.pdef(obj, oname=oname)

def pdoc(obj, formatter=None):
    shell = get_ipython()  # type: InteractiveShell
    inspector = shell.inspector # type: Inspector
    
    # inspector.pdoc() with out pager

    # head = inspector.__head  # is private # For convenience
    head = inspector._Inspector__head  # For convenience
    lines = []
    ds = getdoc(obj)
    if formatter:
        ds = formatter(ds).get('plain/text', ds)
    if ds:
        lines.append(head("Class docstring:"))
        lines.append(indent(ds))
    if inspect.isclass(obj) and hasattr(obj, '__init__'):
        init_ds = getdoc(obj.__init__)
        if init_ds is not None:
            lines.append(head("Init docstring:"))
            lines.append(indent(init_ds))
    elif hasattr(obj,'__call__'):
        call_ds = getdoc(obj.__call__)
        if call_ds:
            lines.append(head("Call docstring:"))
            lines.append(indent(call_ds))

    if not lines:
        inspector.noinfo('documentation')
    else:
        result = '\n'.join(lines)
        publish_display_data({
            'text/plain': result
        })

def pfile(obj):
    # copy from ipython
    shell = get_ipython()  # type: InteractiveShell
    inspector = shell.inspector # type: Inspector
    lineno = find_source_lines(obj)
    if lineno is None:
        inspector.noinfo('file')
        return

    ofile = find_file(obj)
    # run contents of file through pager starting at line where the object
    # is defined, as long as the file isn't binary and is actually on the
    # filesystem.
    if ofile.endswith(('.so', '.dll', '.pyd')):
        print('File %r is binary, not printing.' % ofile)
    elif not os.path.isfile(ofile):
        print('File %r does not exist, not printing.' % ofile)
    else:
        result = inspector.format(
            openpy.read_py_file(ofile, skip_encoding_cookie=False))
        publish_display_data({
            'text/plain': result
        })

def psource(obj, oname='object'):
    """Print the source code for an object."""

    shell = get_ipython()  # type: InteractiveShell
    inspector = shell.inspector # type: Inspector
    try:
        src = getsource(obj, oname=oname)
    except Exception:
        src = None

    if src is None:
        inspector.noinfo('source', oname=oname)
    else:
        result = inspector.format(src)
        publish_display_data({
            'text/plain': result
        })


def env(**kwargs):
    """
    %env
    with out parameters，print all environments variable
    xx=yy, set environment variable
    """
    pass

def matplotlib_gui():
    """
    TODO
    %matplotlib
    with out parameters，print the current backend of matplotlib
    -l list all useable matplotlib backend
    a string: name of a backend; change the backend
    """
    pass

def sx(cmd: str):
    """
    shell execute
    """
    shell = get_ipython() # type: InteractiveShell
    return shell.getoutput(cmd)

def who():
    pass

def who_ls():
    pass

def whos():
    pass

def store():
    """
    TODO
    see https://ipython.readthedocs.io/en/stable/config/extensions/storemagic.html
    """
    pass
