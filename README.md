# PassageSummary
PassageSummary是一个基于Gpt工作的Api，提供文章总结，话题提取等若干总结功能。

# 约束

ApiService提供基本的文本缓存服务，支持对于完全相同的文本的缓存。此外，在ApiService返回异常的时候，会返回`errno`和`message`两个参数，其分别表示全局唯一错误码和错误信息。  

ApiService的返回内容均为Json格式，其中token参数表示OpenAI的ApiKey，使用`gpt-3.5-turbo`模型。  

# Api

得到ApiService的工作状态：

```
GET /
{
	"message":"This server is working normally."
}
```

上传文本：

```
POST /passage
请求：
{
	"content":"This is a content",
	"token":"sk-ss"
}

返回：
正常返回：
{
	"hash":"d622ac64268ce69eef0f3dc8277d06a9182f71c7"
}
错误返回：
{
	"errno":1,
	"message":"文本转换异常"
}
```

询问文本：

```
POST /passage/{hash}
请求：
{
	"action":"ask",
	"param":"这篇文章主要描述了什么？",
	"token":"sk-xxx"
}

返回：
正常返回：
{
	"content":"这篇文章主要讲述了...."
}
错误返回：
{
	"errno":2,
	"message":"文章内容不存在..."
}
```

得到文章话题：

```
POST /passage/{hash}
请求:
{
	"action":"topic",
	"token":"sk-xxx"
}

返回：
正常返回：
{
	"topics":
	[
		{
			"topic":"原神怎么你了？",
			"relative":"0.2"
		}
	]
}
//topic表示的是话题，relative表示话题相关度
错误返回：
{
	"errno":2,
	"message":"文章内容不存在..."
}
```

判断文章与话题的相关度：

```
POST /passage/{hash}
请求:
{
	"action":"getTopicRelative",
	"param":"原神,原批",
	"token":"sk-xxx"
}

返回：
正常返回：
{
	"topics":
	[
		{
			"topic":"原神",
			"relative":"0.2"
		},
		{
			"topic":"原批",
			"relative":"0.9"
		}
	]
}
//topic表示的是话题，relative表示话题相关度
错误返回：
{
	"errno":2,
	"message":"文章内容不存在..."
}
```

总结文章：

```
POST /passage/{hash}
请求:
{
	"action":"summary",
	"token":"sk-xxx"
}

返回：
正常返回：
{
	"content":"这篇文章讲述了一个原批转换为星批的故事。"
}

错误返回：
{
	"errno":2,
	"message":"文章内容不存在..."
}
```

