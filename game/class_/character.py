try:
    from character_image import CharacterImage
    from klass import Class

except ImportError:
    from .character_image import CharacterImage
    from .klass import Class


class Character(Class, CharacterImage):
    ...
