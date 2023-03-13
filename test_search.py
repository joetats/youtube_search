from youtube_search import AsyncYoutubeSearch, YoutubeSearch
import asyncio, time

async def main():
    t1=time.perf_counter()
    result=await AsyncYoutubeSearch("test", max_results=5, timeout=2, language="en-US").fetch()
    t2=time.perf_counter()
    print(f"Result: {result.list()}")
    print(f"Async: {int(t2*1000-t1*1000)} ms")

    t3=time.perf_counter()
    result=YoutubeSearch("test", max_results=5, timeout=2, language="en-US").fetch()
    t4=time.perf_counter()
    print(f"Result: {result.list()}")
    print(f"Sync: {int(t4*1000-t3*1000)} ms")
asyncio.run(main())
