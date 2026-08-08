import os
import i18n
import os
from app.settings import SETTINGS

I18NDIR = os.getcwd()
LOCALESDIR = os.path.join(I18NDIR, 'app', 'locales')

i18n.set('file_format', 'json')
i18n.set('filename_format', '{namespace}.{format}')
i18n.set('skip_locale_root_data', True)

i18n.set('locale', SETTINGS.LANGUAGE)
i18n.set('fallback', 'en')

i18n.load_path.append(os.path.join(LOCALESDIR, SETTINGS.LANGUAGE))