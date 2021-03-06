"""
Tests for the localeurl application.

    >>> import localeurl
    >>> import localeurl.settings

Module utils:

    >>> from localeurl.utils import *

    >>> is_locale_independent('/nl/about')
    False
    >>> is_locale_independent('/media/img/logo.png')
    True
    >>> is_locale_independent('/')
    True
    >>> is_locale_independent('/test/independent/bla/bla')
    True

    >>> strip_path('/')
    ('', '/')
    >>> strip_path('/about/')
    ('', '/about/')
    >>> strip_path('/about/localeurl/')
    ('', '/about/localeurl/')
    >>> strip_path('/fr/about/localeurl/')
    ('fr', '/about/localeurl/')
    >>> strip_path('/en-gb/about/localeurl/')
    ('en-gb', '/about/localeurl/')
    >>> strip_path('/pl/about/localeurl/')
    ('', '/pl/about/localeurl/')

Module middleware:

    >>> from django.test.client import Client
    >>> c = Client()

    >>> r = c.get('/test/')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/nl/test/'
    True

    >>> r = c.get('/test/?somevar=somevalue')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/nl/test/?somevar=somevalue'
    True

    >>> r = c.get('/fr/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'fr'
    True

    >>> r = c.get('/en-us/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-us'
    True

    >>> r = c.get('/test/independent/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'nl-be'
    True

    >>> r = c.get('/test/independent/extra/path/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'nl-be'
    True

    >>> r = c.get('/en-us/test/independent/')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/test/independent/'
    True

    >>> r = c.get('/nl/test/independent/?somevar=somevalue')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/test/independent/?somevar=somevalue'
    True

Test middleware with default language not being prefixed:

    (Changing the settings at runtime is a bit of a hack.)
    >>> localeurl.settings.PREFIX_DEFAULT_LOCALE = False

    >>> r = c.get('/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'nl-be'
    True

    >>> r = c.get('/nl/test/')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/test/'
    True

    >>> r = c.get('/fr/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'fr'
    True

    >>> localeurl.settings.PREFIX_DEFAULT_LOCALE = True

Template tags and filters:

    >>> r = c.get('/nl/test/locale_url/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /nl/test/dummy/ \\n /en-us/test/dummy/4 \\n /fr/test/dummy/4 \\n /nl/test/dummy/4 \\n'

    >>> r = c.get('/nl/test/chlocale/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /nl/admin/ \\n /en-gb/admin/ \\n /nl/admin/ \\n'

    >>> r = c.get('/nl/test/rmlocale/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /admin/ \\n /admin/ \\n /admin/ \\n'

Testing PREFIX_DEFAULT_LOCALE templatetags:

    >>> localeurl.settings.PREFIX_DEFAULT_LOCALE = False

    >>> r = c.get('/test/locale_url/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /test/dummy/ \\n /en-us/test/dummy/4 \\n /fr/test/dummy/4 \\n /test/dummy/4 \\n'

    >>> r = c.get('/fr/test/chlocale/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /admin/ \\n /en-gb/admin/ \\n /fr/admin/ \\n'

    >>> localeurl.settings.PREFIX_DEFAULT_LOCALE = True

"""
