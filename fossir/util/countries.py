

from __future__ import unicode_literals

import pycountry
from werkzeug.datastructures import ImmutableDict

from fossir.core.config import config
from fossir.util.caching import memoize


@memoize
def get_countries():
    _countries = {country.alpha_2: getattr(country, 'common_name', country.name) for country in pycountry.countries}
    _countries.update(config.CUSTOM_COUNTRIES)
    return ImmutableDict(_countries)


@memoize
def get_country(code):
    try:
        return get_countries()[code]
    except KeyError:
        try:
            return pycountry.historic_countries.get(alpha_2=code).name
        except KeyError:
            return None
