from openai import OpenAI

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
         "content": "Remove all details such as facts, examples, or explanations."},
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
         "content": "Use super simple words and simple sentences to paraphrase the following sentence."},
        {"role": "user",
         "content": sentence}
      ],
      temperature=0.5,
      top_p=0.5
  )

  return completion.choices[0].message.content

from simplification import output

def summary(sentence):
  tmp = topic(sentence)
  tmp2 = output(tmp)
  tmp3 = removal(tmp2)
  tmp4 = remove_details(tmp3)
  res = simple_sent(tmp4)
  return res