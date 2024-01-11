from typing import Dict, Optional

import torch
from docarray import DocumentArray
from jina import Executor, requests
import clip
import time

class CLIPTextEncoder(Executor):
    """Encode text into embeddings using the CLIP model."""

    def __init__(
        self,
        pretrained_model_name_or_path: str = 'ViT-B/32',
        base_tokenizer_model: Optional[str] = None,
        max_length: int = 77,
        device: str = 'cpu',
        traversal_paths: str = '@r',
        batch_size: int = 32,
        *args,
        **kwargs,
    ):
        """
        :param pretrained_model_name_or_path: Can be either:
            - A string, the model id of a pretrained CLIP model hosted
                inside a model repo on huggingface.co, e.g., 'openai/clip-vit-base-patch32'
            - A path to a directory containing model weights saved, e.g., ./my_model_directory/
        :param base_tokenizer_model: Base tokenizer model.
            Defaults to ``pretrained_model_name_or_path`` if None
        :param max_length: Max length argument for the tokenizer.
            All CLIP models use 77 as the max length
        :param device: Pytorch device to put the model on, e.g. 'cpu', 'cuda', 'cuda:1'
        :param traversal_paths: Default traversal paths for encoding, used if
            the traversal path is not passed as a parameter with the request.
        :param batch_size: Default batch size for encoding, used if the
            batch size is not passed as a parameter with the request.
        """
        super().__init__(*args, **kwargs)
        self.traversal_paths = traversal_paths
        self.batch_size = batch_size
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.base_tokenizer_model = (
            base_tokenizer_model or pretrained_model_name_or_path
        )
        self.max_length = max_length

        self.device = device

        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        
        self.preprocessor = preprocessor
        self.model = model
        self.model.to(device)
        
        # self.tokenizer = CLIPTokenizer.from_pretrained(self.base_tokenizer_model)
        # self.model = CLIPModel.from_pretrained(self.pretrained_model_name_or_path)
        # self.model.eval().to(device)


    @requests
    def encode(self, docs: DocumentArray, parameters: Dict, **kwargs):
        """
        Encode all documents with the `text` attribute and store the embeddings in the
        `embedding` attribute.

        :param docs: DocumentArray containing the Documents to be encoded
        :param parameters: A dictionary that contains parameters to control encoding.
            The accepted keys are ``traversal_paths`` and ``batch_size`` - in their
            absence their corresponding default values are used.
        """
        print('clip_text encode')
        for docs_batch in DocumentArray(
            filter(
                lambda x: bool(x.text),
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size)) :

            text_batch = docs_batch.texts
            t1 = time.time()
            with torch.inference_mode():
                input_tokens = [self.model.encode_text(clip.tokenize([t, "unknown"]).to(self.device)).cpu().to(dtype=torch.float32) for t in text_batch] # self._generate_input_tokens(text_batch)
                embeddings = input_tokens  # self.model.get_text_features(**input_tokens).cpu().numpy()
                for doc, embedding in zip(docs_batch, embeddings):
                    doc.embedding = embedding
                    # doc.embedding = np.array(embedding).astype('float32')[0]
            t2 = time.time()
            print("encode text cost:", t2 - t1)
            print(t1)
            print(t2)

