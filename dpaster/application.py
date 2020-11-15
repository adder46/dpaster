import json
import pathlib

import click
import pygments.lexers
import pygments.util
import pyperclip
import requests

from dpaster import __version__


CONF_PATH = pathlib.Path("~/.config").expanduser() / "dpaster" / "dpaster.conf"


@click.group()
@click.pass_context
@click.version_option(__version__)
def cli(ctx): # pylint: disable=unused-argument
    """
    Client interface for https://dpaste.com/ pastebin
    """

@cli.command()
@click.option(
    "--syntax", "-s",
    help="Choose syntax (e.g. python, java, bash)",
    required=False,
    metavar="OPT"
)
@click.option(
    "--expires", "-e",
    help="Choose expiry time in days (e.g. 10)",
    required=False,
    metavar="OPT",
    type=int
)
@click.option(
    "--title", "-t",
    help="Choose title",
    required=False,
    metavar="OPT",
    type=str
)
@click.option(
    "--raw", "-r",
    is_flag=True,
    help="Get raw URL",
    required=False,
    metavar="OPT"
)
@click.argument('file', type=click.File("r"), default="-", required=False)
def paste(file, syntax, expires, title, raw):
    """
    Paste to dpaste.org
    """
    try:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
    except FileNotFoundError:
        pathlib.Path.mkdir(CONF_PATH.parent, exist_ok=True)
        with open(CONF_PATH, "w") as conf_file:
            options = {
                "enable_autocp": False,
                "enable_raw": False,
                "default_syntax": None,
                "default_expires": None
            }
            json.dump(options, conf_file)

    content = file.read()

    req = requests.post(
        "http://dpaste.com/api/v2/",
        data={
            "title": title,
            "content": content,
            "syntax": syntax or options.get("default_syntax") or get_syntax(file.name, content),
            "expiry_days": expires or options.get("default_expires")
        }
    )

    req.raise_for_status()

    url = req.text.strip()

    if raw or options.get("enable_raw"):
        url += ".txt"

    click.echo(url)

    if options["enable_autocp"]:
        pyperclip.copy(url)

@cli.command()
@click.option(
    "--show",
    is_flag=True,
    help="View current settings"
)
@click.option(
    "--enable-autocp/--disable-autocp",
    default=None,
    help="Automatically copy the URL to clipboard"
)
@click.option(
    "--enable-raw/--disable-raw",
    default=None,
    help="Always get raw URL",
    metavar="OPT",
)
@click.option(
    "--default-syntax",
    help="Choose default syntax (e.g. python, java, bash)",
    metavar="OPT"
)
@click.option(
    "--default-expires",
    help="Choose default expiry time in days (e.g. 10)",
    metavar="OPT",
    type=int
)
def config(show, enable_autocp, enable_raw, default_syntax, default_expires):
    """
    Configure available settings
    """
    if show:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
            for key, value in options.items():
                print("{}: {}".format(key, value))
            return

    if all(x is None for x in {enable_autocp, enable_raw, default_syntax, default_expires}):
        click.echo("Try 'dpaster config --help' for help")
        return

    with open(CONF_PATH, "r") as conf_file:
        options = json.load(conf_file)
        for name, value in {
            "enable_autocp": enable_autocp,
            "enable_raw": enable_raw,
            "default_syntax": default_syntax,
            "default_expires": default_expires
        }.items():
            if value is not None:
                options[name] = value

    with open(CONF_PATH, "w") as conf_file:
        json.dump(options, conf_file)


def get_syntax(filename, content):
    if filename != "<stdin>":
        try:
            syntax = pygments.lexers.guess_lexer_for_filename(filename, content)
        except pygments.util.ClassNotFound:
            return "text"
    else:
        try:
            syntax = pygments.lexers.guess_lexer(content)
        except pygments.util.ClassNotFound:
            return "text"
    return {
        'ABAP': 'abap',
        'ABNF': 'abnf',
        'ADL': 'adl',
        'ANTLR': 'antlr',
        'ANTLR With ActionScript Target': 'antlr-as',
        'ANTLR With C# Target': 'antlr-csharp',
        'ANTLR With CPP Target': 'antlr-cpp',
        'ANTLR With Java Target': 'antlr-java',
        'ANTLR With ObjectiveC Target': 'antlr-objc',
        'ANTLR With Perl Target': 'antlr-perl',
        'ANTLR With Python Target': 'antlr-python',
        'ANTLR With Ruby Target': 'antlr-ruby',
        'APL': 'apl',
        'ActionScript': 'as',
        'ActionScript 3': 'as3',
        'Ada': 'ada',
        'Agda': 'agda',
        'Aheui': 'aheui',
        'Alloy': 'alloy',
        'AmbientTalk': 'at',
        'Ampl': 'ampl',
        'Angular2': 'ng2',
        'ApacheConf': 'apacheconf',
        'AppleScript': 'applescript',
        'Arduino': 'arduino',
        'AspectJ': 'aspectj',
        'Asymptote': 'asy',
        'Augeas': 'augeas',
        'AutoIt': 'autoit',
        'Awk': 'awk',
        'BBC Basic': 'bbcbasic',
        'BBCode': 'bbcode',
        'BC': 'bc',
        'BNF': 'bnf',
        'BST': 'bst',
        'BUGS': 'bugs',
        'Base Makefile': 'basemake',
        'Bash': 'bash',
        'Bash Session': 'console',
        'Batchfile': 'bat',
        'Befunge': 'befunge',
        'BibTeX': 'bib',
        'BlitzBasic': 'blitzbasic',
        'BlitzMax': 'blitzmax',
        'Boa': 'boa',
        'Boo': 'boo',
        'Boogie': 'boogie',
        'Brainfuck': 'brainfuck',
        'C': 'c',
        'C#': 'csharp',
        'C++': 'cpp',
        'CAmkES': 'camkes',
        'CBM BASIC V2': 'cbmbas',
        'CFEngine3': 'cfengine3',
        'CMake': 'cmake',
        'COBOL': 'cobol',
        'COBOLFree': 'cobolfree',
        'CPSA': 'cpsa',
        'CSS': 'css',
        'CSS+Django/Jinja': 'css+django',
        'CSS+Genshi Text': 'css+genshitext',
        'CSS+Lasso': 'css+lasso',
        'CSS+Mako': 'css+mako',
        'CSS+Myghty': 'css+myghty',
        'CSS+PHP': 'css+php',
        'CSS+Ruby': 'css+erb',
        'CSS+Smarty': 'css+smarty',
        'CSS+mozpreproc': 'css+mozpreproc',
        'CUDA': 'cuda',
        "Cap'n Proto": 'capnp',
        'CapDL': 'capdl',
        'Ceylon': 'ceylon',
        'ChaiScript': 'chai',
        'Chapel': 'chapel',
        'Charmci': 'charmci',
        'Cheetah': 'cheetah',
        'Cirru': 'cirru',
        'Clay': 'clay',
        'Clean': 'clean',
        'Clojure': 'clojure',
        'ClojureScript': 'clojurescript',
        'CoffeeScript': 'coffee-script',
        'Coldfusion CFC': 'cfc',
        'Coldfusion HTML': 'cfm',
        'Common Lisp': 'common-lisp',
        'Component Pascal': 'componentpascal',
        'Coq': 'coq',
        'Crmsh': 'crmsh',
        'Croc': 'croc',
        'Cryptol': 'cryptol',
        'Crystal': 'cr',
        'Csound Document': 'csound-document',
        'Csound Orchestra': 'csound',
        'Csound Score': 'csound-score',
        'Cypher': 'cypher',
        'Cython': 'cython',
        'D': 'd',
        'DASM16': 'dasm16',
        'DTD': 'dtd',
        'Darcs Patch': 'dpatch',
        'Dart': 'dart',
        'Debian Control file': 'control',
        'Debian Sourcelist': 'sourceslist',
        'Delphi': 'delphi',
        'Diff': 'diff',
        'Django/Jinja': 'django',
        'Docker': 'docker',
        'Duel': 'duel',
        'Dylan': 'dylan',
        'Dylan session': 'dylan-console',
        'DylanLID': 'dylan-lid',
        'E-mail': 'email',
        'EBNF': 'ebnf',
        'ECL': 'ecl',
        'ERB': 'erb',
        'Earl Grey': 'earl-grey',
        'Easytrieve': 'easytrieve',
        'Eiffel': 'eiffel',
        'Elixir': 'elixir',
        'Elixir iex session': 'iex',
        'Elm': 'elm',
        'EmacsLisp': 'emacs',
        'Embedded Ragel': 'ragel-em',
        'Erlang': 'erlang',
        'Erlang erl session': 'erl',
        'Evoque': 'evoque',
        'Ezhil': 'ezhil',
        'F#': 'fsharp',
        'Factor': 'factor',
        'Fancy': 'fancy',
        'Fantom': 'fan',
        'Felix': 'felix',
        'Fennel': 'fennel',
        'Fish': 'fish',
        'Flatline': 'flatline',
        'FloScript': 'floscript',
        'Forth': 'forth',
        'Fortran': 'fortran',
        'FortranFixed': 'fortranfixed',
        'FoxPro': 'foxpro',
        'Freefem': 'freefem',
        'GAP': 'gap',
        'GAS': 'gas',
        'GLSL': 'glsl',
        'Genshi': 'genshi',
        'Genshi Text': 'genshitext',
        'Gettext Catalog': 'pot',
        'Gherkin': 'cucumber',
        'Gnuplot': 'gnuplot',
        'Go': 'go',
        'Golo': 'golo',
        'GoodData-CL': 'gooddata-cl',
        'Gosu': 'gosu',
        'Gosu Template': 'gst',
        'Groff': 'groff',
        'Groovy': 'groovy',
        'HLSL': 'hlsl',
        'HSAIL': 'hsail',
        'HTML': 'html',
        'HTML + Angular2': 'html+ng2',
        'HTML+Cheetah': 'html+cheetah',
        'HTML+Django/Jinja': 'html+django',
        'HTML+Evoque': 'html+evoque',
        'HTML+Genshi': 'html+genshi',
        'HTML+Handlebars': 'html+handlebars',
        'HTML+Lasso': 'html+lasso',
        'HTML+Mako': 'html+mako',
        'HTML+Myghty': 'html+myghty',
        'HTML+PHP': 'html+php',
        'HTML+Smarty': 'html+smarty',
        'HTML+Twig': 'html+twig',
        'HTML+Velocity': 'html+velocity',
        'HTTP': 'http',
        'Haml': 'haml',
        'Handlebars': 'handlebars',
        'Haskell': 'haskell',
        'Haxe': 'hx',
        'Hexdump': 'hexdump',
        'Hspec': 'hspec',
        'Hxml': 'haxeml',
        'Hy': 'hylang',
        'Hybris': 'hybris',
        'IDL': 'idl',
        'INI': 'ini',
        'IRC logs': 'irc',
        'Icon': 'icon',
        'Idris': 'idris',
        'Igor': 'igor',
        'Inform 6': 'inform6',
        'Inform 6 template': 'i6t',
        'Inform 7': 'inform7',
        'Io': 'io',
        'Ioke': 'ioke',
        'Isabelle': 'isabelle',
        'J': 'j',
        'JAGS': 'jags',
        'JCL': 'jcl',
        'JSGF': 'jsgf',
        'JSON': 'json',
        'JSON-LD': 'jsonld',
        'JSONBareObject': 'json-object',
        'Jasmin': 'jasmin',
        'Java': 'java',
        'Java Server Page': 'jsp',
        'JavaScript': 'js',
        'JavaScript+Cheetah': 'js+cheetah',
        'JavaScript+Django/Jinja': 'js+django',
        'JavaScript+Genshi Text': 'js+genshitext',
        'JavaScript+Lasso': 'js+lasso',
        'JavaScript+Mako': 'js+mako',
        'JavaScript+Myghty': 'js+myghty',
        'JavaScript+PHP': 'js+php',
        'JavaScript+Ruby': 'js+erb',
        'JavaScript+Smarty': 'js+smarty',
        'Javascript+mozpreproc': 'javascript+mozpreproc',
        'Julia': 'julia',
        'Julia console': 'jlcon',
        'Juttle': 'juttle',
        'Kal': 'kal',
        'Kconfig': 'kconfig',
        'Kernel log': 'kmsg',
        'Koka': 'koka',
        'Kotlin': 'kotlin',
        'LLVM': 'llvm',
        'LLVM-MIR': 'llvm-mir',
        'LLVM-MIR Body': 'llvm-mir-body',
        'LSL': 'lsl',
        'Lasso': 'lasso',
        'Lean': 'lean',
        'LessCss': 'less',
        'Lighttpd configuration file': 'lighty',
        'Limbo': 'limbo',
        'Literate Agda': 'lagda',
        'Literate Cryptol': 'lcry',
        'Literate Haskell': 'lhs',
        'Literate Idris': 'lidr',
        'LiveScript': 'live-script',
        'Logos': 'logos',
        'Logtalk': 'logtalk',
        'Lua': 'lua',
        'MAQL': 'maql',
        'MIME': 'mime',
        'MOOCode': 'moocode',
        'MQL': 'mql',
        'MSDOS Session': 'doscon',
        'MXML': 'mxml',
        'Makefile': 'make',
        'Mako': 'mako',
        'Mask': 'mask',
        'Mason': 'mason',
        'Mathematica': 'mathematica',
        'Matlab': 'matlab',
        'Matlab session': 'matlabsession',
        'MiniD': 'minid',
        'MiniScript': 'ms',
        'Modelica': 'modelica',
        'Modula-2': 'modula2',
        'MoinMoin/Trac Wiki markup': 'trac-wiki',
        'Monkey': 'monkey',
        'Monte': 'monte',
        'MoonScript': 'moon',
        'Mosel': 'mosel',
        'Mscgen': 'mscgen',
        'MuPAD': 'mupad',
        'MySQL': 'mysql',
        'Myghty': 'myghty',
        'NASM': 'nasm',
        'NCL': 'ncl',
        'NSIS': 'nsis',
        'Nemerle': 'nemerle',
        'NewLisp': 'newlisp',
        'Newspeak': 'newspeak',
        'Nginx configuration file': 'nginx',
        'Nimrod': 'nim',
        'Nit': 'nit',
        'Nix': 'nixos',
        'Notmuch': 'notmuch',
        'NuSMV': 'nusmv',
        'NumPy': 'numpy',
        'OCaml': 'ocaml',
        'ODIN': 'odin',
        'Objective-C': 'objective-c',
        'Objective-C++': 'objective-c++',
        'Objective-J': 'objective-j',
        'Octave': 'octave',
        'Ooc': 'ooc',
        'Opa': 'opa',
        'OpenEdge ABL': 'openedge',
        'PEG': 'peg',
        'PHP': 'php',
        'PL/pgSQL': 'plpgsql',
        'POVRay': 'pov',
        'PacmanConf': 'pacmanconf',
        'Pan': 'pan',
        'ParaSail': 'parasail',
        'Pawn': 'pawn',
        'Perl': 'perl',
        'Perl6': 'perl6',
        'Pig': 'pig',
        'Pike': 'pike',
        'PkgConfig': 'pkgconfig',
        'Plain text': 'text',
        'Pony': 'pony',
        'PostScript': 'postscript',
        'PostgreSQL SQL dialect': 'postgresql',
        'PostgreSQL console (psql)': 'psql',
        'PowerShell': 'powershell',
        'PowerShell Session': 'ps1con',
        'Praat': 'praat',
        'Prolog': 'prolog',
        'Properties': 'properties',
        'Protocol Buffer': 'protobuf',
        'Pug': 'pug',
        'Puppet': 'puppet',
        'PyPy Log': 'pypylog',
        'Python': 'python',
        'Python 2.x': 'python2',
        'Python 2.x Traceback': 'py2tb',
        'Python Traceback': 'pytb',
        'Python console session': 'pycon',
        'QBasic': 'qbasic',
        'QML': 'qml',
        'QVTO': 'qvto',
        'RConsole': 'rconsole',
        'REBOL': 'rebol',
        'RHTML': 'rhtml',
        'RPMSpec': 'spec',
        'RQL': 'rql',
        'RSL': 'rsl',
        'Racket': 'racket',
        'Ragel': 'ragel',
        'Ragel in C Host': 'ragel-c',
        'Ragel in CPP Host': 'ragel-cpp',
        'Ragel in D Host': 'ragel-d',
        'Ragel in Java Host': 'ragel-java',
        'Ragel in Objective C Host': 'ragel-objc',
        'Ragel in Ruby Host': 'ragel-ruby',
        'Raw token data': 'raw',
        'Rd': 'rd',
        'ReasonML': 'reason',
        'Red': 'red',
        'Redcode': 'redcode',
        'Relax-NG Compact': 'rnc',
        'ResourceBundle': 'resource',
        'Rexx': 'rexx',
        'Ride': 'ride',
        'Roboconf Graph': 'roboconf-graph',
        'Roboconf Instances': 'roboconf-instances',
        'RobotFramework': 'robotframework',
        'Ruby': 'rb',
        'Ruby irb session': 'rbcon',
        'Rust': 'rust',
        'S': 'splus',
        'SARL': 'sarl',
        'SAS': 'sas',
        'SCSS': 'scss',
        'SPARQL': 'sparql',
        'SQL': 'sql',
        'SWIG': 'swig',
        'Sass': 'sass',
        'Scala': 'scala',
        'Scalate Server Page': 'ssp',
        'Scaml': 'scaml',
        'Scheme': 'scheme',
        'Scilab': 'scilab',
        'ShExC': 'shexc',
        'Shen': 'shen',
        'Sieve': 'sieve',
        'Silver': 'silver',
        'Slash': 'slash',
        'Slim': 'slim',
        'Slurm': 'slurm',
        'Smali': 'smali',
        'Smalltalk': 'smalltalk',
        'SmartGameFormat': 'sgf',
        'Smarty': 'smarty',
        'Snobol': 'snobol',
        'Snowball': 'snowball',
        'Solidity': 'solidity',
        'SourcePawn': 'sp',
        'SquidConf': 'squidconf',
        'Stan': 'stan',
        'Standard ML': 'sml',
        'Stata': 'stata',
        'SuperCollider': 'sc',
        'Swift': 'swift',
        'TADS 3': 'tads3',
        'TAP': 'tap',
        'TASM': 'tasm',
        'TOML': 'toml',
        'Tcl': 'tcl',
        'Tcsh': 'tcsh',
        'Tcsh Session': 'tcshcon',
        'TeX': 'tex',
        'Tea': 'tea',
        'Tera Term macro': 'ttl',
        'Termcap': 'termcap',
        'Terminfo': 'terminfo',
        'Terraform': 'terraform',
        'Thrift': 'thrift',
        'Todotxt': 'todotxt',
        'TrafficScript': 'rts',
        'Transact-SQL': 'tsql',
        'Treetop': 'treetop',
        'Turtle': 'turtle',
        'Twig': 'twig',
        'TypeScript': 'ts',
        'TypoScript': 'typoscript',
        'TypoScriptCssData': 'typoscriptcssdata',
        'TypoScriptHtmlData': 'typoscripthtmldata',
        'USD': 'usd',
        'Unicon': 'unicon',
        'UrbiScript': 'urbiscript',
        'VB.net': 'vb.net',
        'VBScript': 'vbscript',
        'VCL': 'vcl',
        'VCLSnippets': 'vclsnippets',
        'VCTreeStatus': 'vctreestatus',
        'VGL': 'vgl',
        'Vala': 'vala',
        'Velocity': 'velocity',
        'VimL': 'vim',
        'WDiff': 'wdiff',
        'Web IDL': 'webidl',
        'Whiley': 'whiley',
        'X10': 'x10',
        'XML': 'xml',
        'XML+Cheetah': 'xml+cheetah',
        'XML+Django/Jinja': 'xml+django',
        'XML+Evoque': 'xml+evoque',
        'XML+Lasso': 'xml+lasso',
        'XML+Mako': 'xml+mako',
        'XML+Myghty': 'xml+myghty',
        'XML+PHP': 'xml+php',
        'XML+Ruby': 'xml+erb',
        'XML+Smarty': 'xml+smarty',
        'XML+Velocity': 'xml+velocity',
        'XQuery': 'xquery',
        'XSLT': 'xslt',
        'XUL+mozpreproc': 'xul+mozpreproc',
        'Xorg': 'xorg.conf',
        'Xtend': 'xtend',
        'YAML': 'yaml',
        'YAML+Jinja': 'yaml+jinja',
        'Zeek': 'zeek',
        'Zephir': 'zephir',
        'Zig': 'zig',
        'aspx-cs': 'aspx-cs',
        'aspx-vb': 'aspx-vb',
        'autohotkey': 'ahk',
        'c-objdump': 'c-objdump',
        'cADL': 'cadl',
        'ca65 assembler': 'ca65',
        'cfstatement': 'cfs',
        'cpp-objdump': 'cpp-objdump',
        'd-objdump': 'd-objdump',
        'dg': 'dg',
        'eC': 'ec',
        'liquid': 'liquid',
        'markdown': 'md',
        'mozhashpreproc': 'mozhashpreproc',
        'mozpercentpreproc': 'mozpercentpreproc',
        'nesC': 'nesc',
        'objdump': 'objdump',
        'objdump-nasm': 'objdump-nasm',
        'reStructuredText': 'rst',
        'reg': 'registry',
        'scdoc': 'scdoc',
        'sqlite3con': 'sqlite3',
        'systemverilog': 'systemverilog',
        'ucode': 'ucode',
        'verilog': 'verilog',
        'vhdl': 'vhdl',
        'xtlang': 'extempore'
    }.get(syntax.name, "text")
