import os
import json
from langchain import OpenAI
from models import request
from llama_index import (
    GPTSimpleVectorIndex,
    PromptHelper,
    LLMPredictor,
    QuestionAnswerPrompt,
    ServiceContext
)


def dispatch_action(req: request.PassageRequest, hash: str):
    path = os.path.join('cache', hash)
    vector = os.path.join(path, 'index.json')
    match req.action:
        case "ask":
            return ask(vector, str(req.param), req.token)
        case "topic":
            return get_topics(vector, req.token)
        case "getTopicRelative":
            return get_topic_relative(vector, str(req.param), req.token)
        case "summary":
            return summary(vector, req.token)


def ask(vector: str, ask_question: str, token: str):
    response = common_ask(vector, ask_question, token)
    if response.response is None:
        return {
            "errno": 10002,
            "message": "Gpt未返回信息，请检查Token是否有效！"
        }
    return {
        "content": response.response
    }


def summary(vector: str, token: str):
    response = common_ask(vector, "Summary this passage in Chinese", token)
    if response.response is None:
        return {
            "errno": 10002,
            "message": "Gpt未返回信息，请检查Token是否有效！"
        }
    return {
        "content": response.response
    }


def get_topics(vector: str, token: str):
    response = common_ask(vector, "Analysis this passage, getting the topic or key word of it. "
                                  "Returning {{xxx#relative}}. 'xxx' is the the topic or key word of the passage and "
                                  "relative is a num between 0 and 1 presenting the closeness of "
                                  "the topic or key word and the text. "
                                  "For example, returning '{{Minecraft#0.2}},{{Game#0.8}}'", token)
    return get_topic_with_relative(response)


def get_topic_relative(vector: str, key_word: str, token: str):
    response = common_ask(vector, "Analysis this passage, getting the relative of the topic or key word "
                                  "with the passage. "
                                  "Returning {{xxx#relative}}. 'xxx' is the the topic or key word given and "
                                  "relative is a num between 0 and 1 presenting the closeness of "
                                  "the topic or key word and the text. "
                                  "For example, giving 'TopicA,TopicB' returning "
                                  "'{{TopicA#0.2}},{{TopicB#0.8}}'. Now the giving keyword is " + key_word, token)
    return get_topic_with_relative(response)


def get_topic_with_relative(response):
    if response.response is None:
        return {
            "errno": 10002,
            "message": "Gpt未返回信息，请检查Token是否有效！"
        }
    topic = []
    topics = response.response.split(",")
    for i in topics:
        cts = i.split("#")
        if len(cts) != 2:
            return {
                "errno": 10003,
                "message": "Gpt返回无效信息，请尝试重新请求或舍弃请求."
            }
        temp = {
            "topic": str(cts[0]).replace("{{", "").replace("\n", "").replace("{", ""),
            "relative": str(cts[1]).replace("}}", "").replace("}", "")
        }
        topic.append(temp)
    return {
        "content": topic
    }


def common_ask(vector: str, ask_question: str, token: str, prompt: str = "Please answer the question with the context "
                                                                         "information"):
    llm_predictor, prompt_helper = prepare_llama_para(token)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    qa_prompt_impl = (
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        f"{prompt}: {{query_str}}\n"
    )
    qa_prompt = QuestionAnswerPrompt(qa_prompt_impl)
    index = GPTSimpleVectorIndex.load_from_disk(vector, service_context=service_context)
    response = index.query(ask_question, response_mode="compact", text_qa_template=qa_prompt)
    return response


def prepare_llama_para(token):
    os.environ["OPENAI_API_KEY"] = token
    max_input_size = 4096
    num_outputs = 1024
    max_chunk_overlap = 20
    chunk_size_limit = 1000
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    return llm_predictor, prompt_helper
