# clip-as-service
&ensp;&ensp;clip-as-service是jina-ai推出的多模态编码服务（支持多国语言文本的编码和图像的编码），可以以微服务的形式轻松嵌入到神经网络相关项目的代码框架中。  
&ensp;&ensp;clip-as-service的神经网络框架使用了TensorRT,ONNX和PyTorch，在保证
易用性的同时，提供了较快的运行速度。同时，该服务还可在本地端运行时，自适应的调整多个模型。  
&ensp;&ensp;在接口方面，clip-as-service可以在gRPC,HTTP,WebSocket等多个协议之间轻松切换，提供了较为灵活的调用方式。
### 安装方式

&ensp;&ensp;clip-as-service由服务端(clip-service)和用户端(clip-client)组成，两种组件均可通过pip的方式安装。
```
pip install clip-client
```

```
pip install clip-server
```

### 基本使用：  
&ensp;&ensp;用户可直接通过向服务器接口发送请求的方式来对文本和图像进行编码：
```python

from clip_client import Client

c = Client('grpcs://demo-cas.jina.ai:2096')

r = c.encode(
    [
        'First do it',
        'then do it right',
        'then do it better',
        'https://picsum.photos/200',
    ]
)
print(r)
"""
[[ 0.07928467 -0.2836914   0.30810547 ...  0.21350098 -0.0380249
  -0.48266602]
 [ 0.2553711  -0.4111328  -0.00085449 ...  0.0949707  -0.10095215
  -0.6015625 ]
 [ 0.16320801 -0.13867188  0.2631836  ... -0.03359985 -0.3359375
  -0.38305664]
 [-0.23547363  0.60302734  0.2434082  ...  0.2076416   0.09716797
   0.39892578]]
"""

```

如果用户想在本地端启动clip-as-service服务，则可以使用以下方式：  
pytorch框架:
```
python -m clip_server
```
ONNX框架：  
```
python -m clip_server onnx-flow.yml
```
TensorRT框架：  
```
python -m clip_server tensorrt-flow.yml
```

在本地端成功启动clip-server之后（当然，用户也可以在自己的服务器集群中部署，需支持公网IP访问），
用户可在本地端使用clip-client通过端口的形式请求模型调用来对文本和图像进行编码。
```python
from clip_client import Client

c = Client('grpc://0.0.0.0:51000')
c.profile()
```  
之后，用户便可以调用自己需要的API来对数据进行处理。
  
clip-as-service