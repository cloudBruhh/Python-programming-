import re

PROMPTS = {
    "adjective": "An adjective (e.g., happy, scary, weird): ",
    "plural_noun": "A plural noun (e.g., pancakes, shoes, cats): ",
    "animal": "An animal (e.g., cat, dog, dragon): ",
    "name": "A person's name (e.g., John, Sarah): ",
    "noun": "A noun (e.g., book, pencil, chair): ",
    "verb_past_tense": "A past tense verb (e.g., jumped, danced, ran): ",
    "exclamation": "An exclamation (e.g., Wow, Oops, Yikes): ",
    "place": "A place (e.g., park, mall, beach): ",
    "number": "A number (e.g., 5, 10, 100): ",
}

def load_template(filename):
    with open(filename, "r") as file:
        return file.read()

def extract_placeholders(text):
    return re.findall(r"<([^>]+)>", text)

def get_user_inputs(placeholders):
    inputs = {}
    for placeholder in placeholders:
        if placeholder not in inputs:
            prompt = PROMPTS.get(placeholder, f"Enter a {placeholder.replace('_', ' ')}: ")
            inputs[placeholder] = input(prompt)
    return inputs

def generate_story(template, inputs):
    for placeholder, word in inputs.items():
        template = template.replace(f"<{placeholder}>", word)
    return template

def main():
    template = load_template("madlib.txt")
    placeholders = extract_placeholders(template)
    inputs = get_user_inputs(placeholders)
    story = generate_story(template, inputs)
    
    print("\n" + "=" * 40)
    print("YOUR MADLIB STORY:")
    print("=" * 40)
    print(story)

if __name__ == "__main__":
    main()