import re

EXAMPLES = [
    'BE 0839.865.887',
    '0467.049.060 ',
    '467049060',
    'BTW BE 0448.868.983'
]

REGEX = re.compile(
    r'(BTW)?(?P<country_code>[A-Za-z]{2})?0?(?P<real_data>\d{9})'
)

OUTPUT = '{country_code}{real_data}'.format
NOT_MATCH = set()

def normalize(tva):
    tva = tva.replace('.', '').replace(' ', '').replace('-', '')
    m = REGEX.match(tva)
    if m is None:
        if tva not in NOT_MATCH:
            NOT_MATCH.add(tva)
            print(repr(f'did not match: {tva}'))
        return
    d = m.groupdict()
    if d['country_code'] is None:
        d['country_code'] = 'BE'
    return OUTPUT(**d)


if __name__ == '__main__':
    for t in EXAMPLES:
        print(normalize(t))
