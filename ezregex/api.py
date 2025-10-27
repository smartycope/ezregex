import colorsys
import re

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
def toHtml(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def toRgb(html: str) -> tuple:
    hex_color = html.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def generate_colors(amt, s:float=1, v:float=1, offset:int=0):
    """ Generate `amt` number of colors evenly spaced around the color wheel
        with a given saturation and value
    """
    amt += 1
    return [toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((offset + ((1/amt) * (i + 1))) % 1.001, s, v)))) for i in range(amt-1)]

def furthest_colors(html, amt:int=5, v_bias:float=0, s_bias:float=0):
    """ Gets the `amt` number of colors evenly spaced around the color wheel from the given color
        `v_bias` and `s_bias` are between 0-1 and offset the colors
    """
    amt += 1
    h, s, v = colorsys.rgb_to_hsv(*map(lambda c: c/255, toRgb(html)))

    return [toHtml(*map(lambda c: round(c*255), colorsys.hsv_to_rgb(*((h + ((1/amt) * (i + 1))) % 1.001, (s+s_bias) % 1.001, (v+v_bias) % 1.001)))) for i in range(amt-1)]


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
    _colors = generate_colors(len(all_matches), s=foreground_saturation, v=foreground_value)
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
        colors = dict(zip(all_groups, furthest_colors(
            match_colors[match.span()],
            amt=len(all_groups),
            v_bias=background_value_bias,
            s_bias=background_saturation_bias
        )))
        cursor = match.span()[0]

        # First, get up until the match
        html_string += f'{test_string[global_cursor:cursor]}</span>'
        parts.append([None, None, test_string[global_cursor:cursor]])
        match_html = ''
        match_parts = []
        for g in sorted(all_groups, key=lambda x: x[0]):
            # This fixes the bug where overlapping groups get put in twice. By simply preventing
            # the cursor from moving backwards, we eliminate the latter (parent) group from being shown.
            if g[0] < cursor:
                continue

            # Print the match up until the group
            match_html += f'<span style="color: {match_colors[match.span()]};" class="{match_class}">{test_string[cursor:g[0]]}</span>'
            match_parts.append([match_colors[match.span()], None, test_string[cursor:g[0]]])

            # Print the group
            match_html += f'<span style="background-color: {colors[g]}; color: {match_colors[match.span()]};" class="{group_class}">{test_string[g[0]:g[1]]}</span>'
            match_parts.append([match_colors[match.span()], colors[g], test_string[g[0]:g[1]]])
            cursor = g[1]
        match_html += f'<span style="color: {match_colors[match.span()]};" class="{match_class}">{test_string[cursor:match.span()[1]]}</span>'
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
    html_string += test_string[global_cursor:]
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
