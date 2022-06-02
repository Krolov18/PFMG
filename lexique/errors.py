class ErrorsWithCodes(type):
    def __getattribute__(self, code):
        msg = super().__getattribute__(code)
        return msg if code.startswith("__") else f"[{code}] {msg}"


class Errors(metaclass=ErrorsWithCodes):
    E001 = "Le fichier Gloses.yaml semble vide."
    E002 = "Le fichier Blocks.yaml semble vide."
    E003 = "Les champs 'kalaba' et 'translation' sont obligatoires."
    E004 = "Les champs 'kalaba' et 'translation' ne peuvent pas être vides."
    E005 = "Dans un bloc, une catégorie ne peut pas être vide."
    E006 = "L'attribut '{attribute}' n'est pas un attribut reconnu (attributs valides : {attributes})."
    E007 = "La valeur '{value}' n'est pas une valeur reconnue (valeurs valides : {values})."
    E008 = "La règle '{rule}' n'a pas été reconnue."
