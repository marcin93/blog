AUTHOR = 'Marcin Cimaszewski'
SITENAME = 'Marcin Cimaszewski'
#SITEURL = 'https://cimaszewski.eu'
SITETITLE = 'Marcin Cimaszewski'
SITESUBTITLE = 'ALM administrator, CI/CD, Automation passionate'
#FAVICON = SITEURL + '/images/favicon.ico'
FAVICON = '/images/favicons/favicon.ico'
PATH = 'content'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'

TIMEZONE = 'Europe/Berlin'

DISABLE_URL_HASH = True

I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = 'en_US'

COPYRIGHT_YEAR = 2023

#STATIC_PATHS = ['extra/custom.css']

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MAIN_MENU = True
HOME_HIDE_TAGS = True

MENUITEMS = (
    ('About', '/about.html'),
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
)

# Blogroll
#LINKS = (('Pelican', 'https://getpelican.com/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/marcincimaszewski'),
          ('twitter', 'https://twitter.com/mcimasz'),
          ('github','https://www.github.com/marcin93'),
          ('rss', '/feeds/all.atom.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = '/home/marcin/Dev/cimaszewski.eu/blog/Flex'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True