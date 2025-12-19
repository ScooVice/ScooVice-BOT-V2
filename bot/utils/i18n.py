class I18n:
    def __init__(self):
        self.translations = {
            "en": {
                "kick_success": "Member kicked",
                "ban_success": "Member banned",
                "mute_success": "Member muted",
                "error_denied": "Action denied",
                "error_hierarchy": "Hierarchy error",
            },
            "id": {
                "kick_success": "Anggota dikeluarkan",
                "ban_success": "Anggota diblokir",
                "mute_success": "Anggota dibungkam",
                "error_denied": "Aksi ditolak",
                "error_hierarchy": "Kesalahan hierarki",
            },
        }

    def get(self, key, lang="en"):
        return self.translations.get(lang, self.translations["en"]).get(key, key)


i18n = I18n()
