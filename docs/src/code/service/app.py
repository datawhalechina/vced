from docarray import Document
from jina import Flow, DocumentArray
import os
import glob
from jina.types.request.data import DataRequest
import torch


def config():
    os.environ['JINA_PORT'] = '45679'  # the port for accessing the RESTful service, i.e. http://localhost:45678/docs
    os.environ['JINA_WORKSPACE'] = './workspace'  # the directory to store the indexed data
    os.environ['TOP_K'] = '20'  # the maximal number of results to return
    os.environ['DEVICE'] = 'cuda'  # the device for model, should be "cpu" or "cuda". For usage of cuda, should set env JINA_MP_START_METHOD="spawn" before starting Jina & Python. ref: https://github.com/jina-ai/jina/issues/2514 
    
def check_device():
    device = "cpu"
    if (
        os.environ.get("DEVICE") == "cuda" and 
        torch.cuda.is_available() and
        os.environ.get("JINA_MP_START_METHOD") == "spawn"
    ):
        device = "cuda"
    print(f"The CLIP model is loaded on device: {device}")
    return device   
    
def get_docs(data_path):
    for fn in glob.glob(os.path.join(data_path, '*.mp4')):
        yield Document(uri=fn, id=os.path.basename(fn))


def check_index(resp: DataRequest):
    for doc in resp.docs:
        print(f'check_index: {doc.uri}')


def getTime(t: int):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    t_str = "%02d:%02d:%02d" % (h, m, s)
    print(t_str)
    return t_str


def cutVideo(start_t: str, length: int, input: str, output: str, uid: str):
    user_dir = os.path.join('static', 'output', uid)
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    os.system(f'ffmpeg -ss {start_t} -i {input} -t {length} -c:v copy -c:a copy {user_dir}/{output}')


def check_search(resp: DataRequest):
    for i, doc in enumerate(resp.docs):
        print(f'Query text: {doc.text}')
        print(f'Matches: {len(doc.matches)}')
        for m in doc.matches:
            print(m)
            print(
                f'+- id: {m.id}, score: {m.tags["maxImageScore"]}, indexRange: {m.tags["leftIndex"]}-{m.tags["rightIndex"]}, uri: {m.tags["uri"]}')
        print('-' * 10)

        leftIndex = doc.matches[0].tags["leftIndex"]
        rightIndex = doc.matches[0].tags["rightIndex"]
        t_str = getTime(leftIndex)

        # cutVideo(t_str, rightIndex - leftIndex, doc.matches[0].tags["uri"], f"match_{i}_{doc.matches[0].id}.mp4")


if __name__ == '__main__':

    config()
    device = check_device()

    f = Flow(protocol="grpc", port=os.environ['JINA_PORT']).add(
        uses='videoLoader/config.yml',
        uses_requests={"/index": "extract"},
        name="video_loader"
    ).add(
        uses="customClipImage/config.yml",
        name="image_encoder",
        uses_requests={"/index": "encode"},
        uses_with={"device": device}
    ).add(
        uses="customClipText/config.yml",
        name="text_encoder",
        uses_requests={"/search": "encode"},
        uses_with={"device": device}
    ).add(
        uses="customIndexer/config.yml",
        name="indexer",
        uses_metas={"workspace": os.environ['JINA_WORKSPACE']}
    )

    with f:
        f.block()
