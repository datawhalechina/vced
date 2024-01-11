from jina import Document, DocumentArray

d = Document(
    uri='https://www.gutenberg.org/files/1342/1342-0.txt').load_uri_to_text()  # 链接是傲慢与偏见的电子书，此处将电子书内容加载到 Document 中
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())  # 按照换行进行分割字符串
da.apply(lambda d: d.embed_feature_hashing())

q = (
    Document(text='she entered the room')  # 要匹配的文本
    .embed_feature_hashing()  # 通过 hash 方法进行特征编码
    .match(da, limit=5, exclude_self=True, metric='jaccard', use_scipy=True)  # 找到五个与输入的文本最相似的句子
)

print(q.matches[:, ('text', 'scores__jaccard')])  # 输出对应的文本与 jaccard 相似性分数

# 输出结果：
# [['staircase, than she entered the breakfast-room, and congratulated', 'of the room.',
#   'She entered the room with an air more than usually ungracious,',
#   'entered the breakfast-room, where Mrs. Bennet was alone, than she', 'those in the room.'],
#  [{'value': 0.6}, {'value': 0.6666666666666666}, {'value': 0.6666666666666666}, {'value': 0.6666666666666666},
#   {'value': 0.7142857142857143}]]
