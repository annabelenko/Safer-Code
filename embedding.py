import openai
import logn

OPENAI_CLIENT: openai.AsyncOpenAI | None = None
PROVIDER_ID = 'openai'


def init_openai(openai_key: str | None = None) -> openai.AsyncOpenAI:

    global OPENAI_CLIENT
    if not OPENAI_CLIENT:
        openai_key = '--' # Replace with your OpenAI API key
        OPENAI_CLIENT = openai.AsyncOpenAI(api_key=openai_key)

    return OPENAI_CLIENT


def get_openai_client() -> openai.AsyncOpenAI:
    return init_openai()

async def get_embedding(
        text: str,
        model: str = 'text-embedding-ada-002',
        max_retry: int = 5,
        openai_client: openai.AsyncOpenAI | None = None) -> list[float]:

    if openai_client is None:
        openai_client = get_openai_client()

    attempts = 0
    response = None
    while attempts < max_retry:
        try:
            attempts += 1
            response = await openai_client.embeddings.create(input=text,
                                                             model=model,
                                                             timeout=10)
            break
        except openai.RateLimitError:
            logn._framework_log.info(f'openai.error.RateLimitError...Retrying in {10 * attempts} seconds')
            logn.time.sleep(10 * attempts)
        except openai.APITimeoutError:
            logn._framework_log.info(f'openai.error.Timeout...Retrying in {2 * attempts} seconds')
            logn.time.sleep(2 * attempts)
        except openai.APIConnectionError:
            logn._framework_log.info(f'openai.error.APIConnectionError...Retrying in {2 * attempts} seconds')
            logn.time.sleep(2 * attempts)
        except openai.APIError as exc:
            logn._framework_log.info(f'openai.APIError...Retrying in {2 * attempts} seconds', exc_info=exc)
            logn.time.sleep(2 * attempts)

    if response is None:
        raise RuntimeError(f'OpenAI calls failed after {max_retry} attempts.')

    return [e.embedding for e in response.data][0]

async def embedding_main():

    embedding = await get_embedding('hello, world')
    print("Embedding:", embedding)

if __name__ == "__main__":
    import asyncio
    asyncio.run(embedding_main())