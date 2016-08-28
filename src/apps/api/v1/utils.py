import re


def truncate_markdown(text, truncate_length=0):
	"""If self.text is more than self.truncate_length characters long,
	it will be cut at the next word-boundary and '...' will
	be appended.
	To prevent corrupting markdown punctuation syntax, truncate only on
	word-boundary end followed by space followed by word-boundary start.
	"""

	if not text:
		return ''

	if truncate_length == 0:
		return self.text

	if len(text) < truncate_length:
		return text

	pattern = r'^(.{%d,}?\b)\s+\b.*' % (truncate_length - 1)
	text_re = re.compile(pattern, re.DOTALL)
	match = text_re.match(text)
	if not match:
		return text

	return '%s%s' % (match.group(1), '...')

