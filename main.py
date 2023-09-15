#!/usr/bin/env python3

from locations import get_countries, get_austrian_municipialities
from apt_groups import get_apt
from cvelistv5 import get_cves
from common import get_common_words
from static import get_static_lists


def main():
    get_cves()
    get_apt()
    get_countries()
    get_austrian_municipialities()
    get_common_words()
    get_static_lists()


if __name__ == "__main__":
    main()
