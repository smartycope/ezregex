#


### api
```python
.api(
   pattern, replacement_pattern = None, test_string = None, *, replacement_count = 0,
   split_count = 0, default_text_color = 'black', container_tag = 'span',
   container_class = 'ezregex-container', match_class = 'ezregex-match',
   group_class = 'ezregex-group', unmatched_class = 'ezregex-unmatched',
   foreground_saturation = 0.75, foreground_value = 1, background_value_bias = 0.5,
   background_saturation_bias = 0.9
)
```

---
This functions like an API, even though it's not ever used as an actual API. It's used by
the EZRegex frontend, as it loads this library locally. It made sense to put it in the
library itself, becasue it could be useful for other purposes.
