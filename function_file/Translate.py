import deepl
import os

API_KEY = os.getenv('DeepL_API')

def deepltranslate(text,lang):
  translator = deepl.Translator(API_KEY)
  return(translator.translate_text(text, target_lang=lang))
