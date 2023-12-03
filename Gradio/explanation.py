from openai import OpenAI
from wordfreq import word_frequency
import spacy

client = OpenAI(api_key='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')
T = 0.5
t = 0.5

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

def explain_words(sentence):
  words = words_exp(sentence)
  assis = 'Give me a new verison of sentences which correctly explain these words in simpler sentences or correctly paraphrase with super easy-to-understand words(consider their academic meaning if neccesary):'
  for word in words:
    assis += word
    assis += ', '
  assis += 'inside sentences and only give me the new version of explained sentences.'

  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
         {"role": "system",
         "content": assis},
        {"role": "user",
         "content": sentence}
      ],
      temperature=T,
      top_p=t,
  )

  return completion.choices[0].message.content

def add_description(sentence):

  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Include more descriptive adjectives, adverbs, or modifiers to provide a clearer explanation to the following sentences, and only give me the sentence after expand."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=T,
      top_p=t
  )

  return completion.choices[0].message.content

def add_connectors(sentence):

  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Incorporate transitional phrases or connectors to smoothly connect ideas and expand on the following sentences."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=T,
      top_p=t
  )

  return completion.choices[0].message.content

def split(sentence):

  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Simpler sentences' structure, do not give me several points but a coherent paragraph, and not changing sentence's meanings."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=T,
      top_p=t
  )

  return completion.choices[0].message.content

def explanation(sentence):

  tmp = add_description(sentence)
  tmp = add_connectors(tmp)
  tmp = split(tmp)
  tmp = explain_words(tmp)

  return tmp