from openai import OpenAI
from simplification import output

client = OpenAI(api_key='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')

def topic(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Identify the main idea of the following sentences. Only give me the sentences of the main idea."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )

  return completion.choices[0].message.content

def removal(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Remove any information that is repetitive or not crucial to understanding the main idea and the supporting points."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )

  return completion.choices[0].message.content

def remove_details(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Remove all details such as reasons, facts, examples, or explanations."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )

  return completion.choices[0].message.content

def simple_sent(sentence):
  completion = client.chat.completions.create(
      model='gpt-4-1106-preview',
      messages=[
        {"role": "system",
         "content": "Make this sentence simpler without changing sentence meaning."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )

  return completion.choices[0].message.content

def summary(sentence):

  tmp = topic(sentence)
  tmp = output(tmp)
  tmp = removal(tmp)
  tmp = remove_details(tmp)
  res = simple_sent(tmp)

  return res