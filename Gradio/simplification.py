from wordfreq import word_frequency
import spacy
from openai import OpenAI
import openai

client = OpenAI(api_key='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')

def simplify(statement):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": f"Simplify the following sentences: {statement}",
            }
        ],
        temperature=0.5,
        top_p=0.5,
    )
    return completion.choices[0].message.content

def check_freq(sentence):

  nlp = spacy.load("en_core_web_sm")
  words = [tok.lemma_ for tok in nlp(sentence) if tok.pos_ not in ["PUNCT", "SPACE"]]

  freq_dict = {}
  for word in words:
    freq = word_frequency(word, 'en')
    freq_dict[word] = freq

  vocab = dict(sorted(freq_dict.items(), key=lambda item: item[1]))
  return vocab

def words_exp(sentence):

  freq_dict = check_freq(sentence)

  explain = dict((k, v) for k, v in freq_dict.items() if v < 1e-4)

  words = list(explain.keys())

  return words

def simplify_words(sentence):
  words = words_exp(sentence)
  assis = 'Give me a new verison of sentences which replace these words in simpler synonyms or explanations:'
  for word in words:
    assis += word
    assis += ', '
  assis += 'inside sentences and only give me the new version of explained sentences. Please combine with orginal sentence meanings and keep the original meanings.'

  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
         {"role": "system",
         "content": assis},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5,
  )

  return completion.choices[0].message.content

def simplify_structure(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Simpler sentences' structure, do not give me several points but a coherent paragraph, and not changing original sentences' meanings."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5,
  )
  return completion.choices[0].message.content

def output(sentence):

    tmp = simplify(sentence)
    tmp = simplify_structure(tmp)
    tmp = simplify_words(tmp)
    tmp = simplify_structure(tmp)
    tmp = simplify_words(tmp)

    return tmp