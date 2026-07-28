__version__ = '1.1.0'
import math
import inspect
import keyword
import re
from types import ModuleType
from typing import Any, get_args

# TODO:
# EZREgex todo:
# if overlapping groups, expand them all different amounts
# return the compiled replacement regex as well
# add code and string displays


# V2 color algorithm: credit to ChatGPT
def _rgb_to_html(r, g, b) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'

def _html_to_rgb(html: str) -> tuple:
    hex_color = html.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def _rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(x / 255) for x in rgb)

    # sRGB D65 -> XYZ
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    # D65 reference white
    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    x, y, z = f(x), f(y), f(z)

    return (
        116 * y - 16,
        500 * (x - y),
        200 * (y - z),
    )

def _lab_to_rgb(lab: tuple[float, float, float]) -> tuple[int, int, int] | None:
    L, a, b = lab

    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    def finv(t: float) -> float:
        t3 = t ** 3
        return t3 if t3 > 0.008856 else (t - 16 / 116) / 7.787

    x = 0.95047 * finv(fx)
    y = 1.00000 * finv(fy)
    z = 1.08883 * finv(fz)

    # XYZ -> linear sRGB
    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z

    # Out of sRGB gamut
    if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1):
        return None

    return tuple(
        round(max(0, min(1, _linear_to_srgb(x))) * 255)
        for x in (r, g, b)
    )

def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    linear = [_srgb_to_linear(x / 255) for x in rgb]
    return (
        0.2126 * linear[0]
        + 0.7152 * linear[1]
        + 0.0722 * linear[2]
    )

def _contrast_ratio(
    a: tuple[int, int, int],
    b: tuple[int, int, int],
) -> float:
    l1 = _relative_luminance(a)
    l2 = _relative_luminance(b)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def _generate_colors(amt: int, base: str, readability_distinctness_ratio:float=4.5) -> list[str]:
    """ Generate `amt` number of colors that are readable against the given base color.
        `base` must be an HTML color
        `readability_distinctness_ratio` is the minimum contrast ratio between colors.
            This represents the tradeoff between contrast against the background and
            the contrast between colors.
    """
    if amt <= 0:
        return []

    # if len(base) != 3 or any(not 0 <= x <= 255 for x in base):
        # raise ValueError("base must be an RGB tuple with values from 0 to 255")

    # base = tuple(map(int, base))
    base = _html_to_rgb(base)
    base_lab = _rgb_to_lab(base)

    # Generate candidate colors.
    #
    # We vary lightness, hue, and chroma. Higher chroma gives more vivid
    # colors, while multiple lightness levels prevent everything from
    # collapsing into the same perceptual region.
    candidates: list[tuple[tuple[int, int, int], tuple[float, float, float]]] = []

    for L in range(20, 91, 5):
        for hue in range(0, 360, 5):
            for chroma in range(30, 101, 10):
                angle = math.radians(hue)

                lab = (
                    L,
                    chroma * math.cos(angle),
                    chroma * math.sin(angle),
                )

                rgb = _lab_to_rgb(lab)
                if rgb is None:
                    continue

                # WCAG AA-ish readability threshold.
                if _contrast_ratio(rgb, base) < readability_distinctness_ratio:
                    continue

                candidates.append((rgb, lab))

    if not candidates:
        raise ValueError("Could not find any readable colors for this base")

    # Pick the first color furthest from the base.
    first = max(
        candidates,
        key=lambda x: (
            (x[1][0] - base_lab[0]) ** 2
            + (x[1][1] - base_lab[1]) ** 2
            + (x[1][2] - base_lab[2]) ** 2
        ),
    )

    selected = [first]
    remaining = [c for c in candidates if c != first]

    # Farthest-point sampling:
    # At every step, choose the candidate whose nearest selected color
    # is as far away as possible.
    while len(selected) < amt:
        if not remaining:
            break

        best = max(
            remaining,
            key=lambda candidate: min(
                (
                    (candidate[1][0] - chosen[1][0]) ** 2
                    + (candidate[1][1] - chosen[1][1]) ** 2
                    + (candidate[1][2] - chosen[1][2]) ** 2
                )
                for chosen in selected
            ),
        )

        selected.append(best)
        remaining.remove(best)

    return [_rgb_to_html(*rgb) for rgb, _ in selected]


# TODO: Better docs, and an example of the output in the docstring
def api(pattern, replacement_pattern=None, test_string=None, *,
        replacement_count=0,
        split_count=0,
        background_color='#FFFFFF',
        readability_distinctness_ratio=4.5
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
        'parts': [],
        'matches': []
    }

    parts = []
    global_cursor = 0
    group_spans_by_match = [
        list(dict.fromkeys(
            match.span(group_number)
            for group_number in range(1, len(match.groups()) + 1)
        ))
        for match in matches
    ]
    color_count = len(matches) + sum(map(len, group_spans_by_match))
    colors = _generate_colors(
        color_count,
        base=background_color,
        readability_distinctness_ratio=readability_distinctness_ratio,
    )
    match_colors = colors[:len(matches)]
    group_color_offset = len(matches)

    for match, match_color, all_groups in zip(
        matches,
        match_colors,
        group_spans_by_match,
    ):
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
        group_colors = dict(zip(
            all_groups,
            colors[group_color_offset:group_color_offset + len(all_groups)],
        ))
        group_color_offset += len(all_groups)
        cursor = match.span()[0]

        # First, get up until the match
        parts.append([None, None, test_string[global_cursor:cursor]])
        match_parts = []
        for g in sorted(all_groups, key=lambda x: x[0]):
            # This fixes the bug where overlapping groups get put in twice. By simply preventing
            # the cursor from moving backwards, we eliminate the latter (parent) group from being shown.
            if g[0] < cursor:
                continue

            # Print the match up until the group
            match_parts.append([match_color, None, test_string[cursor:g[0]]])

            # Print the group
            match_parts.append([match_color, group_colors[g], test_string[g[0]:g[1]]])
            cursor = g[1]
        match_parts.append([match_color, None, test_string[cursor:match.span()[1]]])
        global_cursor = match.span()[1]
        parts += match_parts
        match_json = {
            'match': {
                'string': match.group(),
                'parts': match_parts,
                'end': match.end(),
                'start': match.start(),
                "color": match_color,
            },
            "unnamed groups":{},
            "named groups":{},
        }

        for num, span in unnamed_groups.items():
            match_json['unnamed groups'][num] = {
                'string': match.group(num) or '',
                'end': span[1],
                'start': span[0],
                "color": group_colors[span],
            }

        for name, span in named_groups.items():
            match_json['named groups'][name] = {
                'string': match.group(name) or '',
                'end': span[1],
                'start': span[0],
                "color": group_colors[span],
            }
        json['matches'].append(match_json)

    # Don't forget to add any bit at the end that's not part of a match
    parts.append([None, None, test_string[global_cursor:]])

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
