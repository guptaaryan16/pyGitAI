# The file to generate commit messages for the calls made to OpenAI models
#
# Based on https://github.com/Nutlope/aicommits/blob/develop/src/utils/openai.ts

import os

# from openai import OpenAI
from pygitai.context import Context
from pygitai.models import generate_prompt
import json
import http.client
from http.client import HTTPSConnection
from typing import Dict, Any, List, Optional, Tuple

# from https_proxy_agent import HttpsProxyAgent
# from known_error import KnownError
# from config import CommitType
# from prompt import generate_prompt
# from tiktoken import TiktokenModel

# def https_post(
#     hostname: str,
#     path: str,
#     headers: Dict[str, str],
#     json_data: Any,
#     timeout: int,
#     proxy: Optional[str] = None,
# ) -> Tuple[http.client.HTTPResponse, str]:
#     post_content = json.dumps(json_data)
#     connection = HTTPSConnection(hostname)
#     if proxy:
#         connection = HTTPSConnection(
#             hostname, timeout=timeout, context=HttpsProxyAgent(proxy).socks_context()
#         )
#     else:
#         connection = HTTPSConnection(hostname, timeout=timeout)

#     connection.request(
#         method="POST",
#         url=path,
#         body=post_content,
#         headers={
#             **headers,
#             "Content-Type": "application/json",
#             "Content-Length": len(post_content),
#         },
#     )

#     try:
#         response = connection.getresponse()
#         data = response.read().decode("utf-8")
#     finally:
#         connection.close()

#     return response, data


# def create_chat_completion(
#     api_key: str, json_data: Dict[str, Any], timeout: int, proxy: Optional[str] = None
# ) -> Dict[str, Any]:
#     response, data = https_post(
#         hostname="api.openai.com",
#         path="/v1/chat/completions",
#         headers={"Authorization": f"Bearer {api_key}"},
#         json_data=json_data,
#         timeout=timeout,
#         proxy=proxy,
#     )

#     if not (200 <= response.status < 300):
#         error_message = f"OpenAI API Error: {response.status} - {response.reason}"
#         if data:
#             error_message += f"\n\n{data}"

#         if response.status == 500:
#             error_message += "\n\nCheck the API status: https://status.openai.com"

#         raise KnownError(error_message)

#     return json.loads(data)


# def sanitize_message(message: str) -> str:
#     return message.strip().replace("\n", "").replace("\r", "").rstrip(".") + " "


# def deduplicate_messages(messages: List[str]) -> List[str]:
#     return list(set(messages))


def fetch_commit_message_openai(
    api_key: str,
    # model: TiktokenModel,
    locale: str,
    diff: str,
    completions: int,
    max_length: int,
    # commit_type: CommitType,
    timeout: int,
    proxy: Optional[str] = None,
) -> List[str]:
    # try:
    #     completion = create_chat_completion(
    #         api_key,
    #         {
    #             "model": model,
    #             "messages": [
    #                 {
    #                     "role": "system",
    #                     "content": generate_prompt(locale, max_length, commit_type),
    #                 },
    #                 {"role": "user", "content": diff},
    #             ],
    #             "temperature": 0.7,
    #             "top_p": 1,
    #             "frequency_penalty": 0,
    #             "presence_penalty": 0,
    #             "max_tokens": 200,
    #             "stream": False,
    #             "n": completions,
    #         },
    #         timeout,
    #         proxy,
    #     )

    #     return deduplicate_messages(
    #         [
    #             sanitize_message(choice["message"]["content"])
    #             for choice in completion["choices"]
    #             if choice.get("message", {}).get("content")
    #         ]
    #     )
    # except Exception as error:
    #     if getattr(error, "code", None) == "ENOTFOUND":
    #         raise KnownError(
    #             f"Error connecting to {error.hostname} ({error.syscall}). Are you connected to the internet?"
    #         )

    #     raise error
    pass
