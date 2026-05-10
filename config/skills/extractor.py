import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text, skill_list):
    text = text.lower()
    skill_list = [skill.lower() for skill in skill_list]

    found = []

    for skill in skill_list:
        if skill in text:
            found.append(skill)

    return list(set(found))