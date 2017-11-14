#!/usr/bin/env python

import re
import sys

from tailer import Tailer
from timeout import timeout
from timeout import TimeoutError

def matchedLine(compiledSearchRegex, line):

    if not compiledSearchRegex:
        return False

    elif re.search(compiledSearchRegex, line):
        return True

    else:
        return False



def main(filepath, scrollBackLines, searchRegex):

    if searchRegex is None:
        # TODO error as no searchRegex
        compiledSearchRegex = None

    else:
        compiledSearchRegex = re.compile(searchRegex, re.MULTILINE)

    tailer = Tailer(open(filepath, 'rb'))

    try:
        try:
            if scrollBackLines > 0:
                lines = tailer.tail(scrollBackLines)

                for line in lines:
                    matched = matchedLine(compiledSearchRegex, line)

                    if matched:
                        return

            else:
                # Seek to the end so we can follow
                tailer.seek_end()

            for line in tailer.follow():
                matched = matchedLine(compiledSearchRegex, line)

                if matched:
                    return

        except KeyboardInterrupt:
            # Escape silently
            pass
    finally:
        tailer.close()



if __name__ == '__main__':
    try:
        with timeout(seconds=3):
            main("example.log", 1, "fred")
    except TimeoutError:
        sys.stdout.write('timeout\n')
