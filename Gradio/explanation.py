from wordfreq import word_frequency
import spacy
from openai import OpenAI

client = OpenAI(api_key='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')

def main_idea(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Identify and elaborate on each key concept mentioned, only give me those words and do not explain it."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )
  return completion.choices[0].message.content

def details(sentence1, sentence2):
    completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "You are a helpful assistant."},
        {"role": "user",
         "content": f"Expand {sentence2} by adding details of these points such as {sentence1}. Do not add more than a sentence of extra details. You could also only add a few words."}
      ],
      temperature=0.5,
      top_p=0.5
    )
    return completion.choices[0].message.content

def examples(sentence):
    completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "You are a helpful assistant."},
        {"role": "user",
         "content": f"Add one concise sentence of example if it has, to {sentence} for better understanding. Give me the sentences after adding this example."}
      ],
      temperature=0.5,
      top_p=0.5
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

def explain_words(sentence):
  words = words_exp(sentence)
  assis = 'Give me a new verison of sentences which correctly explain these words in super easy-to-understand sentences or correctly paraphrase with super easy-to-understand words(consider their academic meaning if neccesary):'
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
      temperature=0.5,
      top_p=0.5,
  )

  return completion.choices[0].message.content

def simplify_structure(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Change all sentences into simple sentences without missing anything and ensure the sentences are readable and coherent. You can break original sentences down to achieve this. Also do not increase words' complexity."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5,
  )
  return completion.choices[0].message.content

def explain(sent):
  tmp = main_idea(sent)
  tmp1 = details(tmp, sent)
  tmp2 = examples(tmp1)
  tmp3 = explain_words(tmp2)
  tmp4 = simplify_structure(tmp3)
  result = explain_words(tmp4)
  return result