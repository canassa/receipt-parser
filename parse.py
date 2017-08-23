"""
tesseract -l nld FullSizeRender.jpg output -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,+abcdefghijklmnopqrstuvwxyz
"""

from decimal import Decimal
import re
import argparse


def main(input_file):
    with open(input_file) as f:
        content = f.read()
        total = None
        items = []
        for l in content.split('\n'):
            l = l.upper()
            match = re.search('^([\w\s+]+) (\d+[.,‚]\d\d)$', l)

            if not match:
                continue

            item = match.group(1).strip().upper()
            value = Decimal(re.sub('[,‚]', '.', match.group(2)))

            if item == 'TOTAAL':
                total = value
                continue
            elif item == 'SUBTOTAAL':
                continue
            elif item == 'OVER EUR':
                continue

            match_qty = re.search('^(\d)+ X EUR (\d+[.,]\d\d)$', l)
            if match_qty:
                items[-1][2] = int(match_qty.group(1))
                continue

            items.append([item, value, 1])

        for i in items:
            print(i)

        total_calc = sum([i[1] for i in items])

        print('Total parsed: {}'.format(total_calc))
        print('Total: {}'.format(total))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()
    main(args.input_file)
