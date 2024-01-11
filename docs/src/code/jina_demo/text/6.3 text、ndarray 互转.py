from jina import DocumentArray, Document  # 导包

# DocumentArray 相当于一个 list，用于存放 Document
da = DocumentArray([Document(text='hello world'),
                    Document(text='goodbye world'),
                    Document(text='hello goodbye')])
print(da)  # <DocumentArray (length=3) at 140545164218128>

vocab = da.get_vocabulary()
print(vocab)  # {'hello': 2, 'world': 3, 'goodbye': 4}

# text转为tensor向量
for d in da:
    d.convert_text_to_tensor(vocab, max_length=10)  # max_length为向量最大值，可不设置
    print(d.tensor)

# 输出结果：
# [0 0 0 0 0 0 0 0 2 3]  # 用这种方式简单将字符串转为向量
# [0 0 0 0 0 0 0 0 4 3]
# [0 0 0 0 0 0 0 0 2 4]

# tensor向量转为text
for d in da:
    d.convert_tensor_to_text(vocab)
    print(d.text)

# 输出结果：
# hello world
# goodbye world
# hello goodbye
