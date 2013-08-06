#!/usr/bin/env python

import sys

import twyg.cmdline


if __name__ == '__main__':
    try:
        sys.exit(twyg.cmdline.main())
    except KeyboardInterrupt:
        sys.exit(1)

