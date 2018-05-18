# coding=utf-8
"""
Some basic get list test to verify that the wrapper is working.
You need to set `API_KEY`, `LIST_ID` ENV to successfully get result.
"""
import asyncio
import os

from mailchimp3.mailchimpclient import MailChimpError


async def main():
    from mailchimp3 import MailChimp

    API_KEY = os.getenv('API_KEY')
    LIST_ID = os.getenv('LIST_ID')

    client = MailChimp(API_KEY)

    # SUCCESS
    result = await client.lists.get(LIST_ID)
    print(result)

    # FAIL
    try:
        await client.lists.get('asdf')
    except MailChimpError as e:
        print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
