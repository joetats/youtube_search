from youtube_search import AsyncYoutubeSearch, YoutubeSearch
import asyncio, time

async def main():
    t1=time.perf_counter()
    result=await AsyncYoutubeSearch("test", max_results=5, language="en-US").fetch(timeout=2)
    t2=time.perf_counter()
    assert result.count == 5
    assert result.max_results == 5
    assert isinstance(result.list(False), list)
    assert isinstance(result.json_string(), str) # clear_cache defaulted to True
    assert result.count == 0
    print(f"Async: {int(t2*1000-t1*1000)} ms")

    t3=time.perf_counter()
    result=YoutubeSearch("test", max_results=5, language="en-US").fetch(timeout=2)
    t4=time.perf_counter()
    assert result.count == 5
    assert result.max_results == 5
    assert isinstance(result.list(False), list)
    assert isinstance(result.json_string(), str) # clear_cache defaulted to True
    assert result.count == 0
    print(f"Sync: {int(t4*1000-t3*1000)} ms")
asyncio.run(main())
