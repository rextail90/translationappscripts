from translators.reverso_api import ReversoTranslator

t = ReversoTranslator(headless=False)
result = t.translate("مرحبا", "ar", "en")
print("Translation:", result)
t.close()