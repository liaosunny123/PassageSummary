import os
from passages import passageAnalysis
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    PromptHelper
)


def save_passage(content: str, token: str):
    name = hash(str)
    res = {
        "hash": name
    }

    # permanently cache
    dir_path = os.path.join('cache', str(name))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        return res
    file_name = os.path.join(dir_path, 'raw')
    index_name = os.path.join(dir_path, 'index.json')
    with open(file_name, "w") as file:
        file.write(content)
    llm_predictor, prompt_helper = passageAnalysis.prepare_llama_para(token)
    documents = SimpleDirectoryReader(dir_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context
    )
    index.save_to_disk(index_name)
    return res


def get_passage_content(hash: str):
    with open(hash, "r") as file:
        return file.read()
