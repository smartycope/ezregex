__version__ = '1.0.0'

import colorsys
from html import escape as _html_escape
import inspect
import keyword
import re
from types import ModuleType
from typing import Any, get_args

# TODO:
# EZREgex todo:
# if overlapping groups, expand them all different amounts
# add classes to the spans so I can style them
# return the compiled replacement regex as well
# add code and string displays
# change the default background text color
# change the first color being white (give it a class?)
# remove empty spans

# These functions comprise the color algorithm
def _toHtml(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def _toRgb(html: str) -> tuple:
    hex_color = html.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def _generate_colors(amt, s:float=1, v:float=1, offset:int=0):
    """ Generate `amt` number of colors evenly spaced around the color wheel
        with a given saturation and value
    """
    amt += 1
    return [_toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((offset + ((1/amt) * (i + 1))) % 1.001, s, v)))) for i in range(amt-1)]

def _furthest_colors(html, amt:int=5, v_bias:float=0, s_bias:float=0):
    """ Gets the `amt` number of colors evenly spaced around the color wheel from the given color
        `v_bias` and `s_bias` are between 0-1 and offset the colors
    """
    amt += 1
    h, s, v = colorsys.rgb_to_hsv(*map(lambda c: c/255, _toRgb(html)))

    return [_toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((h + ((1/amt) * (i + 1))) % 1.001, (s+s_bias) % 1.001, (v+v_bias) % 1.001)))) for i in range(amt-1)]


# TODO: Better docs, and an example of the output in the docstring
def api(pattern, replacement_pattern=None, test_string=None, *,
        replacement_count=0,
        split_count=0,
        # Can accept any valid CSS color
        default_text_color='black',
        container_tag='span',
        container_class='ezregex-container',
        match_class='ezregex-match',
        group_class='ezregex-group',
        unmatched_class='ezregex-unmatched',
        foreground_saturation = .75,
        foreground_value = 1,
        background_value_bias = .5,
        background_saturation_bias = .9,
    ):
    """ This functions like an API, even though it's not ever used as an actual API. It's used by
        the EZRegex frontend, as it loads this library locally. It made sense to put it in the
        library itself, becasue it could be useful for other purposes.
    """
    if isinstance(pattern, str):
        raise ValueError(f'The api `pattern` parameter must be of type EZRegex, recieved {type(pattern)}')

    # Get an inverse, if nessicary
    if test_string is None:
        test_string = pattern.inverse()
    matches = list(re.finditer(pattern._compile(), test_string))
    # found = bool(len(matches))

    json = {
        'regex': pattern._compile(),
        'string': test_string,
        'string HTML': ...,
        'parts': [],
        'matches': []
    }

    html_string = f'<{container_tag} class="{container_class}"><span style="color: {default_text_color};" class="{unmatched_class}">'
    parts = []
    global_cursor = 0
    all_matches = [m.span() for m in matches]
    # Map match spans to unique colors
    _colors = _generate_colors(len(all_matches), s=foreground_saturation, v=foreground_value)
    match_colors = dict(zip(all_matches, _colors))

    for match in matches:
        all_groups = {match.span(i+1) for i in range(len(match.groups()))}
        named_groups = {i: match.span(i) for i in match.groupdict().keys()}
        # TODO: have named groups show their name and number instead of just their name
        # named_groups = {
        #     (cnt+1, ): match.span(cnt+1)
        #     for cnt, i in enumerate(match.groups())
        #     if i in match.groupdict().values()
        # }
        unnamed_groups = {
            cnt+1: match.span(cnt+1)
            for cnt, i in enumerate(match.groups())
            if i not in match.groupdict().values()
        }
        # Map group spans to unique colors
        # This gets equally spaced colors from the given color, so they're differentiable
        # and readable on a dark background
        colors = dict(zip(all_groups, _furthest_colors(
            match_colors[match.span()],
            amt=len(all_groups),
            v_bias=background_value_bias,
            s_bias=background_saturation_bias
        )))
        cursor = match.span()[0]

        # First, get up until the match
        html_string += f'{_html_escape(test_string[global_cursor:cursor])}</span>'
        parts.append([None, None, test_string[global_cursor:cursor]])
        match_html = ''
        match_parts = []
        for g in sorted(all_groups, key=lambda x: x[0]):
            # This fixes the bug where overlapping groups get put in twice. By simply preventing
            # the cursor from moving backwards, we eliminate the latter (parent) group from being shown.
            if g[0] < cursor:
                continue

            # Print the match up until the group
            match_html += f'<span style="color: {match_colors[match.span()]};" class="{match_class}">{_html_escape(test_string[cursor:g[0]])}</span>'
            match_parts.append([match_colors[match.span()], None, test_string[cursor:g[0]]])

            # Print the group
            match_html += f'<span style="background-color: {colors[g]}; color: {match_colors[match.span()]};" class="{group_class}">{_html_escape(test_string[g[0]:g[1]])}</span>'
            match_parts.append([match_colors[match.span()], colors[g], test_string[g[0]:g[1]]])
            cursor = g[1]
        match_html += f'<span style="color: {match_colors[match.span()]};" class="{match_class}">{_html_escape(test_string[cursor:match.span()[1]])}</span>'
        match_parts.append([match_colors[match.span()], None, test_string[cursor:match.span()[1]]])
        global_cursor = match.span()[1]
        # Don't print after the group, cause there might be another match that covers it
        html_string += match_html
        parts += match_parts
        # to_slice = lambda t: f'({t[0]}:{t[1]})'
        match_json = {
            'match': {
                'string': match.group(),
                'string HTML': match_html,
                'parts': match_parts,
                'end': match.end(),
                'start': match.start(),
                "color": match_colors[match.span()],
            },
            "unnamed groups":{},
            "named groups":{},
        }

        for num, span in unnamed_groups.items():
            match_json['unnamed groups'][num] = {
                'string': match.group(num) or '',
                'end': span[1],
                'start': span[0],
                "color": colors[span],
            }

        for name, span in named_groups.items():
            match_json['named groups'][name] = {
                'string': match.group(name) or '',
                'end': span[1],
                'start': span[0],
                "color": colors[span],
            }
        json['matches'].append(match_json)

    # Don't forget to add any bit at the end that's not part of a match
    html_string += _html_escape(test_string[global_cursor:])
    parts.append([None, None, test_string[global_cursor:]])
    html_string += f'</span></{container_tag}>'

    # Remove any empty spans
    html_string = re.sub(r'<span[^>]*></span>', '', html_string)

    json['string HTML'] = html_string
    json['parts'] = parts
    if replacement_pattern is not None:
        json['replaced'] = re.sub(pattern.str(), replacement_pattern.str(), test_string, replacement_count)
    else:
        json['replaced'] = None
    json['split'] = re.split(pattern.str(), test_string, split_count)
    return json


def _camel_case(name: str) -> str:
    return ''.join(
        word.capitalize() if index else word
        for index, word in enumerate(name.split('_'))
    )


def _json_default(value: Any) -> Any:
    if value is inspect.Parameter.empty:
        return None
    if value is Ellipsis:
        return '...'
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def _parameter_kind(parameter: inspect.Parameter) -> str:
    """Normalize Python signatures into the small set the browser understands."""
    name = parameter.name
    annotation = parameter.annotation
    annotation_args = set(get_args(annotation))

    if name == 'num_or_name':
        return 'name_or_number'
    if name in ('greedy', 'possessive') or annotation is bool:
        return 'boolean'
    if bool in annotation_args and type(None) in annotation_args:
        return 'auto_boolean'
    if annotation is int or name in ('min', 'max', 'num'):
        return 'integer'
    if name in ('patterns', 'inputs') and parameter.kind is inspect.Parameter.VAR_POSITIONAL:
        return 'variadic_pattern'
    if (
        name == 'pattern' or name.endswith('_pattern') or
        name in ('input', 'type', 'open', 'close')
    ):
        return 'pattern'
    if annotation is str or name in ('regex', 'name', 'char', 'and_char', 'chars'):
        return 'string'
    if str in annotation_args and int in annotation_args:
        return 'name_or_number'
    return 'python_expression'


def _origin_for(cls: type, name: str) -> str:
    if name in cls._compound_parts:
        return 'compound'

    for base in cls.__mro__[1:]:
        if name not in base.__dict__:
            continue
        base_name = base.__name__.lower()
        if 'advancedreplacements' in base_name:
            return 'advanced_replacements'
        if 'replacements' in base_name:
            return 'replacements'
        if 'advancedgroups' in base_name:
            return 'advanced_grouping'
        if 'groups' in base_name:
            return 'grouping'
        if 'assertions' in base_name:
            return 'assertions'
        if 'anchors' in base_name:
            return 'anchors'
        if 'base' in base_name:
            return 'base'
    return 'dialect'


def _aliases_for(cls: type, canonical: str, alias_map: dict[str, tuple[str, ...]]) -> list[str]:
    candidates = [canonical, _camel_case(canonical)]
    for alias in alias_map.get(canonical, ()):
        candidates.extend((alias, _camel_case(alias)))

    aliases = []
    for candidate in candidates:
        if (
            candidate != canonical and candidate not in aliases and
            candidate.isidentifier() and not keyword.iskeyword(candidate) and
            hasattr(cls, candidate) and getattr(cls, candidate) is getattr(cls, canonical)
        ):
            aliases.append(candidate)
    return aliases


def _dialect_class(module: ModuleType, base_class: type) -> type | None:
    candidates = [
        value for value in vars(module).values()
        if (
            inspect.isclass(value) and value is not base_class and
            issubclass(value, base_class) and value.__module__.startswith(module.__name__)
        )
    ]
    return candidates[0] if len(candidates) == 1 else None


def _dialect_label(cls: type) -> str:
    label = cls.__name__
    if label.endswith('EZRegex'):
        label = label[:-len('EZRegex')]
    if label == 'Javascript':
        return 'JavaScript'
    return label


def _describe_element(cls: type, name: str, alias_map: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    obj = getattr(cls, name)
    parameters = []

    if name not in cls._compound_parts:
        signature = inspect.signature(obj._func_list[0])
        for parameter in signature.parameters.values():
            if parameter.name in ('cur', 'args', 'kwargs'):
                continue
            kind = _parameter_kind(parameter)
            if name in ('literal', 'rliteral') and parameter.name == 'pattern':
                kind = 'string'
            browser_name = parameter.name
            if kind == 'pattern' and parameter.name == 'input':
                browser_name = 'pattern'
            elif kind == 'variadic_pattern' and parameter.name == 'inputs':
                browser_name = 'patterns'
            parameters.append({
                'name': browser_name,
                'python_name': parameter.name,
                'kind': kind,
                'required': parameter.default is inspect.Parameter.empty,
                'default': _json_default(parameter.default),
                'variadic': parameter.kind is inspect.Parameter.VAR_POSITIONAL,
                'keyword_only': parameter.kind is inspect.Parameter.KEYWORD_ONLY,
            })

    return {
        'name': name,
        'aliases': _aliases_for(cls, name, alias_map),
        'documentation': inspect.cleandoc(obj.docstring or ''),
        'origin': _origin_for(cls, name),
        'replacement': obj.replacement,
        'parameters': parameters,
    }


def _describe_function(name: str, function: Any) -> dict[str, Any]:
    parameters = []
    for parameter in inspect.signature(function).parameters.values():
        if parameter.name in ('self', 'cls', 'args', 'kwargs'):
            continue
        parameters.append({
            'name': parameter.name,
            'python_name': parameter.name,
            'kind': _parameter_kind(parameter),
            'required': parameter.default is inspect.Parameter.empty,
            'default': _json_default(parameter.default),
            'variadic': parameter.kind is inspect.Parameter.VAR_POSITIONAL,
            'keyword_only': parameter.kind is inspect.Parameter.KEYWORD_ONLY,
        })
    return {
        'name': name,
        'aliases': [],
        'documentation': inspect.cleandoc(inspect.getdoc(function) or ''),
        'parameters': parameters,
    }


def _describe_dialects() -> dict[str, Any]:
    """Return the private, JSON-safe runtime catalog used by ezregex-blockly."""
    import ezregex as root
    from .EZRegex import EZRegex
    from .psuedonyms import psuedonyms

    dialects = []
    seen_classes = set()
    for module_name, module in vars(root).items():
        if not isinstance(module, ModuleType):
            continue
        cls = _dialect_class(module, EZRegex)
        if cls is None or cls in seen_classes:
            continue
        seen_classes.add(cls)

        dialect_id = module.__name__.rsplit('.', 1)[-1]
        allow_greedy = False
        allow_possessive = False
        for base in cls.__mro__:
            if hasattr(base, '_allow_greedy'):
                allow_greedy = bool(base._allow_greedy)
                allow_possessive = bool(base._allow_possessive)
                break

        docs_match = re.search(r'https?://\S+', inspect.getdoc(cls) or '')
        elements = [
            _describe_element(cls, name, psuedonyms)
            for name in cls.parts(include_psuedonyms=False, include_functions=False)
        ]
        functions = []
        for function_name in ('options', 'replace'):
            function = getattr(cls, function_name, None)
            if function is not None:
                functions.append(_describe_function(function_name, function))

        dialects.append({
            'id': dialect_id,
            'label': _dialect_label(cls),
            'class_name': cls.__name__,
            'documentation_url': docs_match.group(0).rstrip('.,') if docs_match else '',
            'testing': 'python' if dialect_id == 'python' else (
                'javascript' if dialect_id == 'javascript' else 'compile'
            ),
            'capabilities': {
                'greedy': allow_greedy,
                'possessive': allow_possessive,
            },
            'flags': [
                {
                    'name': flag_name,
                    'value': flag_value,
                    'documentation': inspect.cleandoc(
                        cls._flag_docs_map.get(flag_name, '')
                    ),
                }
                for flag_name, flag_value in cls._flag_map.items()
            ],
            'elements': elements,
            'functions': functions,
        })

    priority = {'python': 0, 'javascript': 1, 'r': 2, 'pcre2': 3}
    dialects.sort(key=lambda dialect: (priority.get(dialect['id'], 99), dialect['label']))
    return {
        'schema_version': 1,
        'ezregex_version': root.__version__,
        'dialects': dialects,
    }
