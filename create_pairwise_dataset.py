import jsonpickle
import argparse
import sys
import random
import csv
import json
import uuid
from dataset_utils import questions, PairwisePoems


def read_file_content(filename):
    file_ = open(filename, "r")
    content = file_.read()
    file_.close()
    return content


def read_gpt2_poems():
    content = read_file_content("source_corpora/gpt2_poems.txt")
    # Only take poems with 4 lines
    return [poem for poem in content.split("\n\n")[:-1] if poem.count("\n") == 4]


def read_hafez_poems():
    content = read_file_content("source_corpora/hafez_poems.txt")
    return [poem for poem in content.split("\n\n")]


def read_deepspeare_poems():
    content = read_file_content("source_corpora/deepspeare_poems.txt")
    poems = []
    for poem in [p for p in content.split("\n\n") if p != ""]:
        # split poem in lines
        lines = poem.split("\n")
        # Remove first line
        lines = lines[1:]
        # from each line remove first 14 chars
        lines = [line[14:] for line in lines]
        # concat lines with linebreak
        poems.append("\n".join(lines))
    return poems


def read_eng_gutenbearg_pomes():
    content = read_file_content("source_corpora/eng_gutenberg_measures_all.json")
    json_content = jsonpickle.decode(content)
    poems = []
    for poem_id in json_content.keys():
        poem_entry = json_content[poem_id]['poem']
        stanzas = []
        for stanza_id in poem_entry.keys():
            stanza = poem_entry[stanza_id]
            lines = []
            for line_id in stanza.keys():
                line = stanza[line_id]
                lines.append(line['text'])
            stanza = "\n".join(lines)
            stanzas.append(stanza)
        poems.extend(stanzas)
    poems = [poem for poem in poems if poem.count("\n") == 4 and len(poem) > 130]
    return poems


def read_jhamtani_poems():
    jhamtani_content = read_file_content("source_corpora/jhamtani_poems.json")
    poems_list = eval(jhamtani_content)
    poems = []
    for endings, poem in poems_list:
        # replaces eol token with LF
        poem = poem.replace("<eos> ", "\n")
        poems.append(poem)
    return poems


def read_truepoetry_poems():
    truepoetry_content = read_file_content("source_corpora/truepoetry_poems.txt")
    poems = truepoetry_content.split("\n\n")
    return poems


def read_ngram_poems():
    ngram_content = read_file_content("source_corpora/ngram_poems_act.txt")
    return [poem for poem in ngram_content.split("\n\n") if len(poem) > 80]


def read_lstm_poems():
    lstm_content = read_file_content("source_corpora/lstm_poems.txt")
    return [poem for poem in lstm_content.split("\n\n") if len(poem) > 80]


def format_text_for_csv(text):
    # Replace LF with HTML line break
    text = text.replace("\n", "<br>")
    # Remove blank line indicators
    text = text.replace("[NEWLINE]", "")
    text = text.lower()
    return text


def create_dataset(datasets, n, probabilities):
    pairs = []
    # Get available datasets
    dataset_keys = list(datasets.keys())
    for i in range(n):
        # Choose a dataset from all corpus with the provided probabilities
        dataset1 = random.choices(dataset_keys, weights=probabilities, k=1)[0]
        # Choose the first poem from the chosen corpus
        poem1 = random.choice(datasets[dataset1])
        poem2 = poem1
        # Choose the second corpus
        dataset2 = random.choice(dataset_keys)
        # Get a poem from the second corpus which is not equal to the first chosen poem
        while poem2 == poem1:
            poem2 = random.choice(datasets[dataset2])
        # Remove bad formatting and make it ready for csv
        poem1 = format_text_for_csv(poem1)
        poem2 = format_text_for_csv(poem2)

        # Distribute questions on 3 stacks randomly
        question_ids = list(questions.keys())
        random.shuffle(question_ids)
        question_set1 = question_ids[:3]
        question_set2 = question_ids[3:6]
        question_set3 = question_ids[6:10]

        # Set a unique pair id for later identification
        pair_id = str(uuid.uuid4())

        # Setup first stack of questions and create a pair with them
        question1_id = question_set1[0]
        question1 = questions[question1_id]
        question2_id = question_set1[1]
        question2 = questions[question2_id]
        question3_id = question_set1[2]
        question3 = questions[question3_id]
        pair1 = PairwisePoems(pair_id, poem1, poem2, dataset1, dataset2,
                              question1=question1, question1_id=question1_id,
                              question2=question2, question2_id=question2_id,
                              question3=question3, question3_id=question3_id)

        # Setup second stack of questions and create a pair with them
        question1_id = question_set2[0]
        question1 = questions[question1_id]
        question2_id = question_set2[1]
        question2 = questions[question2_id]
        question3_id = question_set2[2]
        question3 = questions[question3_id]
        pair2 = PairwisePoems(pair_id, poem1, poem2, dataset1, dataset2,
                              question1=question1, question1_id=question1_id,
                              question2=question2, question2_id=question2_id,
                              question3=question3, question3_id=question3_id)

        # Setup last stack of questions now with remaining 4 questions and bundle them with the 2 selected poems
        question1_id = question_set3[0]
        question1 = questions[question1_id]
        question2_id = question_set3[1]
        question2 = questions[question2_id]
        question3_id = question_set3[2]
        question3 = questions[question3_id]
        question4_id = question_set3[3]
        question4 = questions[question4_id]
        pair3 = PairwisePoems(pair_id, poem1, poem2, dataset1, dataset2,
                              question1=question1, question1_id=question1_id,
                              question2=question2, question2_id=question2_id,
                              question3=question3, question3_id=question3_id,
                              question4=question4, question4_id=question4_id)

        pairs.append(pair1)
        pairs.append(pair2)
        pairs.append(pair3)
    # Shuffle that one annotator does not get all questions after each other
    random.shuffle(pairs)
    return pairs


def filter_4byte_chars(s):
    i = 0
    j = len(s)
    # you need to convert
    # the immutable string
    # to a mutable list first
    s = list(s)
    while i < j:
        # get the value of this byte
        k = ord(s[i])
        # this is a 1-byte character, skip to the next byte
        if k <= 127:
            i += 1
        # this is a 2-byte character, skip ahead by 2 bytes
        elif k < 224:
            i += 2
        # this is a 3-byte character, skip ahead by 3 bytes
        elif k < 240:
            i += 3
        # this is a 4-byte character, remove it and update
        # the length of the string we need to check
        else:
            s[i:i + 4] = []
            j -= 4
    return ''.join(s)

parser = argparse.ArgumentParser(description="Create a pairwise dataset with ")
parser.add_argument("--prob-real", dest="real_prob", type=float, default=0.5)
parser.add_argument("--output-filename", dest="output_filename", default="dataset.csv")

args = parser.parse_args()

real_prob = args.real_prob
output_filename = args.output_filename

assert 0. <= real_prob <= 1., "prob-real should be in range 0 and 1"

# Retrieve poems from text files
gpt2_poems = read_gpt2_poems()
hafez_poems = read_hafez_poems()
deepspeare_poems = read_deepspeare_poems()
jhamtani_poems = read_jhamtani_poems()
gutberg_poems = read_eng_gutenbearg_pomes()
truepoetry_poems = read_truepoetry_poems()
ngram_poems = read_ngram_poems()
lstm_poems = read_lstm_poems()

datasets = {
    "hafez": hafez_poems,
    "gutenberg": gutberg_poems,
    "jhamtani": jhamtani_poems,
    "deepspeare": deepspeare_poems,
    "true_poetry": truepoetry_poems,
    "ngram": ngram_poems,
    "gpt2": gpt2_poems,
    "lstm": lstm_poems
}

# Calculate probabilities for each dataset with provided probability for real corpus
generated_prob = (1 - real_prob) / len(datasets.keys())
probabilities = [generated_prob] * len(datasets.keys())
probabilities[1] = real_prob

# Create a dataset with 850 pairs
dataset = create_dataset(datasets, 850, probabilities=probabilities)
dataset_json = jsonpickle.encode(dataset, unpicklable=False)
# Remove chars which cannot be displayed in AMT
dataset_json = filter_4byte_chars(dataset_json)
# Remove any other encoding issues
dataset_json = dataset_json.encode(encoding="utf-8", errors="replace").decode(encoding="utf-8", errors="ignore")

# Write to csv
dataset_dict = json.loads(dataset_json)
fieldnames = dataset_dict[0].keys()
with open("created_datasets/" + output_filename, "w+", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset_dict)
