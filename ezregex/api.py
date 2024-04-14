import colorsys
import re

foreground_s = .75
foreground_v = 1.
background_v_bias = .5
background_s_bias = .9

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


def api(pattern, replacement_pattern=None, test_string=None, *, replacement_count=0, split_count=0):
    # Get an inverse, if nessicary
    if test_string is None:
        test_string = pattern.inverse()
    matches = list(re.finditer(pattern._compile(), test_string))
    found = bool(len(matches))

    json = {
        'regex': pattern._compile(),
        'string': test_string,
        'string HTML': ...,
        'parts': [],
        'matches': []
    }

    html_string = '<p><span style="color: white;">'
    parts = []
    globalCursor = 0
    allMatches = [m.span() for m in matches]
    # Map match spans to unique colors
    _colors = generate_colors(len(allMatches), s=foreground_s, v=foreground_v)
    matchColors = dict(zip(allMatches, _colors))

    for match in matches:
        allGroups = {match.span(i+1) for i in range(len(match.groups()))}
        namedGroups = {i: match.span(i) for i in match.groupdict().keys()}
        # TODO: have named groups show their name and number instead of just their name
        # namedGroups = {
        #     (cnt+1, ): match.span(cnt+1)
        #     for cnt, i in enumerate(match.groups())
        #     if i in match.groupdict().values()
        # }
        unnamedGroups = {
            cnt+1: match.span(cnt+1)
            for cnt, i in enumerate(match.groups())
            if i not in match.groupdict().values()
        }
        # Map group spans to unique colors
        # This gets equally spaced colors from the given color, so they're differentiable
        # and readable on a dark background
        colors = dict(zip(allGroups, furthest_colors(
            matchColors[match.span()],
            amt=len(allGroups),
            v_bias=background_v_bias,
            s_bias=background_s_bias
        )))
        cursor = match.span()[0]

        # First, get up until the match
        html_string += f'{test_string[globalCursor:cursor]}</span>'
        parts.append([None, None, test_string[globalCursor:cursor]])
        match_html = ''
        match_parts = []
        for g in sorted(allGroups, key=lambda x: x[0]):
            # This fixes the bug where overlapping groups get put in twice. By simply preventing
            # the cursor from moving backwards, we eliminate the latter (parent) group from being shown.
            if g[0] < cursor:
                continue

            # Print the match up until the group
            match_html += f'<span style="color: {matchColors[match.span()]};">{test_string[cursor:g[0]]}</span>'
            match_parts.append([matchColors[match.span()], None, test_string[cursor:g[0]]])

            # Print the group
            match_html += f'<span style="background-color: {colors[g]}; color: {matchColors[match.span()]};">{test_string[g[0]:g[1]]}</span>'
            match_parts.append([matchColors[match.span()], colors[g], test_string[g[0]:g[1]]])
            cursor = g[1]
        match_html += f'<span style="color: {matchColors[match.span()]};">{test_string[cursor:match.span()[1]]}</span>'
        match_parts.append([matchColors[match.span()], None, test_string[cursor:match.span()[1]]])
        globalCursor = match.span()[1]
        # Don't print after the group, cause there might be another match that covers it
        html_string += match_html
        parts += match_parts
        toSlice = lambda t: f'({t[0]}:{t[1]})'
        match_json = {
            'match': {
                'string': match.group(),
                'string HTML': match_html,
                'parts': match_parts,
                'end': match.end(),
                'start': match.start(),
                "color": matchColors[match.span()],
            },
            "unnamed groups":{},
            "named groups":{},
        }

        for num, span in unnamedGroups.items():
            match_json['unnamed groups'][num] = {
                'string': match.group(num) or '',
                'end': span[1],
                'start': span[0],
                "color": colors[span],
            }

        for name, span in namedGroups.items():
            match_json['named groups'][name] = {
                'string': match.group(name) or '',
                'end': span[1],
                'start': span[0],
                "color": colors[span],
            }
        json['matches'].append(match_json)

    # Don't forget to add any bit at the end that's not part of a match
    html_string += test_string[globalCursor:]
    parts.append([None, None, test_string[globalCursor:]])
    html_string += '</span></p>'
    json['string HTML'] = html_string
    json['parts'] = parts
    if replacement_pattern is not None:
        json['replaced'] = re.sub(pattern.str(), replacement_pattern.str(), test_string, replacement_count)
    else:
        json['replaced'] = None
    json['split'] = re.split(pattern.str(), test_string, split_count)
    return json
