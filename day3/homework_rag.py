from huggingface_hub import login
import torch
import random
from sentence_transformers import SentenceTransformer




login("yourkey")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(0)

# モデル(Gemma2)の読み込み

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_name = "google/gemma-2-2b-jpn-it"
tokenizer = AutoTokenizer.from_pretrained(model_name)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            quantization_config=bnb_config,
            torch_dtype=torch.bfloat16,
        )


def generate_output(query):
  messages = [
      {"role": "user", "content": query},
  ]
  input_ids = tokenizer.apply_chat_template(
      messages,
      add_generation_prompt=True,
      return_tensors="pt"
  ).to(model.device)

  terminators = [
      tokenizer.eos_token_id,
      tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]

  outputs = model.generate(
      input_ids,
      max_new_tokens=256,
      eos_token_id=terminators,
      do_sample=False,
      # temperature=0.6, # If do_sample=True
      # top_p=0.9,  # If do_sample=True
  )

  response = outputs[0][input_ids.shape[-1]:]
  return tokenizer.decode(response, skip_special_tokens=True)


#question =  "LLMにおけるInference Time Scalingとは？"
query =  [f"\n\n[質問1] ちくわの製造ロードマップは？",
          f"\n\n[質問2] ワニは誰が育てている？",
          f"\n\n[質問3] ちくわ会社は何社ある？",
          f"\n\n[質問4] ワニは全部何匹いる？",
          f"\n\n[質問5] 登場人物はだれ？"]
for i in query:
    response = generate_output(i)
    print(response)

#RAG導入

emb_model = SentenceTransformer("infly/inf-retriever-v1-1.5b", trust_remote_code=True)
# In case you want to reduce the maximum length:
emb_model.max_seq_length = 4096

with open("AI/llm-question.txt", "r", encoding="utf-8") as f:
  raw_writedown = f.read()


# ドキュメントを用意する。
documents = [text.strip() for text in raw_writedown.split("。")]
print("ドキュメントサイズ: ", len(documents))
print("ドキュメントの例: \n", documents[0])


# Retrievalの実行
question = "ちくわ製造のロードマップを教えて"
print(question)

query_embeddings = emb_model.encode([question], prompt_name="query")
document_embeddings = emb_model.encode(documents)

# 各ドキュメントの類似度スコア
scores = (query_embeddings @ document_embeddings.T) * 100
print(scores.tolist())

topk=5
""" topk = 5
for i, index in enumerate(scores.argsort()[0][::-1][:topk]):
  print(f"取得したドキュメント{i+1}: (Score: {scores[0][index]})")
  print(documents[index], "\n\n") """

#回答に役立つ該当の発言はreference[1871]〜に含まれてます。
references = "\n".join(["* " + documents[i] for i in scores.argsort()[0][::-1][:topk]])
query =  [f"[参考資料]\n{references}\n\n[質問1] ちくわの製造ロードマップは？",
          f"[参考資料]\n{references}\n\n[質問2] ワニは誰が育てている？",
          f"[参考資料]\n{references}\n\n[質問3] ちくわ会社は何社ある？",
          f"[参考資料]\n{references}\n\n[質問4] ワニは全部何匹いる？",
          f"[参考資料]\n{references}\n\n[質問5] 登場人物はだれ？"]

for i in query:
    print("----------------------")
    response = generate_output(query)
    print(response)