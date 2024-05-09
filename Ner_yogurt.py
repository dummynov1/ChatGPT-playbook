import spacy
from spacy import displacy
from collections import Counter

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Sample list of 1000 yogurt descriptions
yogurt_descriptions = [
    "Yoplait Plain yogurt low sugar vanilla 4 oz",
    "Dannon Greek yogurt mixed berry 6 oz",
    "Chobani Nonfat plain yogurt 5.3 oz",
    "Yoplait Lowfat yogurt strawberry 4 oz",
    "Fage Total Greek yogurt honey 6 oz",
    # ... (rest of the 1000 descriptions)
]

# Process each description using spaCy
entities = []
for desc in yogurt_descriptions:
    doc = nlp(desc)
    entities.extend([(ent.text, ent.label_) for ent in doc.ents])

# Group entities by label
entity_counts = {}
for entity, label in entities:
    if label not in entity_counts:
        entity_counts[label] = Counter()
    entity_counts[label][entity] += 1

# Print top entities for each label
for label, counter in entity_counts.items():
    print(f"Top {label}:")
    for entity, count in counter.most_common(5):
        print(f"{entity}: {count}")
    print()
