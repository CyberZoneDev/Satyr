import asyncio


class Utils:
    @staticmethod
    def get_event_loop():
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()

        return loop
