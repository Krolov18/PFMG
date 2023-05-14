import cue  # type: ignore

if __name__ == '__main__':
    CUE_FILE = "/home/korantin/PycharmProjects/PFMG/projects/schemas/primitive/primitives.cue"
    YAML_FILE = "/home/korantin/PycharmProjects/PFMG/lexique/data/french_v1/Gloses.yaml"
    cue.vet.files(CUE_FILE, YAML_FILE)
