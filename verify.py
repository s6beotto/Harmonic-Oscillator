from tika import parser

filename = 'build/report.pdf'

raw = parser.from_file(filename)
text = raw['content']

lines = text.split('\n')


print('\033[1m[Verification]\033[0m computing file %s' %filename)
finds = [l for l in lines if '??' in l]
if len(finds) > 0:
	print('??:\n\t' + '\n\t'.join(finds))

totalfinds = finds[:]

if len(totalfinds) > 0:
	print('%d errors found' %len(finds))
else:
	print('No errors found')
