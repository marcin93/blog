AUTHOR = 'Marcin Cimaszewski'
SITENAME = 'Marcin Cimaszewski'
SITETITLE = 'Marcin Cimaszewski'
SITESUBTITLE = 'Senior Platform Engineer · M&A · R&D'
SITEURL = ''

FAVICON = '/images/favicons/favicon.ico'
PATH = 'content'
PAGE_URL = '../{slug}.html'
PAGE_SAVE_AS = '../{slug}.html'
DEFAULT_PAGINATION = 10
DIRECT_TEMPLATES = ['index', 'blog', 'tags', 'categories', 'archives']

BROWSER_COLOR = '#2563eb'
PYGMENTS_STYLE = 'monokai'

TIMEZONE = 'Europe/Berlin'

DISABLE_URL_HASH = True

I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = 'en_US'

COPYRIGHT_YEAR = 2026

# Feed generation
FEED_ALL_ATOM = 'feeds/all.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MAIN_MENU = True
HOME_HIDE_TAGS = True

MENUITEMS = (
    ('About', '/about.html'),
    ('Projects', '/projects.html'),
    ('Blog', '/blog.html'),
    ('Tags', '/tags.html'),
)

# Social widget
SOCIAL = (('mastodon', 'https://mastodon.social/@ves93'),
          ('linkedin', 'https://www.linkedin.com/in/marcincimaszewski'),
          ('twitter', 'https://twitter.com/mcimasz'),
          ('github','https://www.github.com/marcin93'),
          ('rss', '/feeds/all.atom.xml'),)

THEME = 'theme'
