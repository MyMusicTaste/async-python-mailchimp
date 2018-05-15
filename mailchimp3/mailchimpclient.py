# coding=utf-8
"""
Mailchimp v3 Api SDK

Documentation: http://developer.mailchimp.com/documentation/mailchimp/
"""
from __future__ import unicode_literals
import functools
import re

from urllib.parse import urljoin
from urllib.parse import urlencode

import logging

import aiohttp
from aiohttp import BasicAuth

_logger = logging.getLogger('mailchimp3.client')


def _enabled_or_noop(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.enabled:
            return fn(self, *args, **kwargs)

    return wrapper


class MailChimpError(Exception):
    pass


class MailChimpClient(object):
    """
    MailChimp class to communicate with the v3 API
    """

    def __init__(self, mc_api=None, mc_user='python-mailchimp', enabled=True, timeout=None, request_headers=None):
        """
        Initialize the class with your optional user_id and required api_key.

        If `enabled` is not True, these methods become no-ops. This is
        particularly useful for testing or disabling with configuration.

        :param mc_api: Mailchimp API key
        :type mc_api: :py:class:`str`
        :param mc_user: Mailchimp user id
        :type mc_user: :py:class:`str`
        :param enabled: Whether the API should execute any requests
        :type enabled: :py:class:`bool`
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param request_headers: (optional) Headers for
            :py:func:`requests.requests`.
        :type request_headers: :py:class:`dict`
        """
        super(MailChimpClient, self).__init__()
        self.enabled = enabled
        self.timeout = timeout
        if mc_api:
            if not re.match(r"^[0-9a-f]{32}$", mc_api.split('-')[0]):
                raise ValueError(
                    'The API key that you have entered is not valid, did you enter a username by mistake?\n'
                    'The order of arguments for API key and username has reversed in 2.1.0')
            self.auth = BasicAuth(mc_user, mc_api)
            datacenter = mc_api.split('-').pop()
            self.base_url = 'https://{0}.api.mailchimp.com/3.0/'.format(datacenter)
        else:
            raise Exception('You must provide an API key')
        self.request_headers = request_headers

    async def _make_request(self, **kwargs):
        _logger.info(u'{method} Request: {url}'.format(**kwargs))
        if kwargs.get('json'):
            _logger.info('PAYLOAD: {json}'.format(**kwargs))

        async with aiohttp.ClientSession() as session:
            async with session.request(**kwargs) as response:
                _logger.info(u'{method} Response: {status} {text}' \
                             .format(method=kwargs['method'], status=response.status, text=(await response.text())))

                return response

    @_enabled_or_noop
    async def _post(self, url, data=None):
        """
        Handle authenticated POST requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        url = urljoin(self.base_url, url)
        try:
            r = await self._make_request(**dict(
                method='POST',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                headers=self.request_headers
            ))
        except aiohttp.ClientError as e:
            raise e
        else:
            if r.status >= 400:
                raise MailChimpError(await r.json())
            if r.status == 204:
                return None
            return r.json()

    @_enabled_or_noop
    async def _get(self, url, **queryparams):
        """
        Handle authenticated GET requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param queryparams: The query string parameters
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        if len(queryparams):
            url += '?' + urlencode(queryparams)
        try:
            r = await self._make_request(**dict(
                method='GET',
                url=url,
                auth=self.auth,
                timeout=self.timeout,
                headers=self.request_headers
            ))
        except aiohttp.ClientError as e:
            raise e
        else:
            if r.status >= 400:
                raise MailChimpError(await r.json())
            return await r.json()

    @_enabled_or_noop
    async def _delete(self, url):
        """
        Handle authenticated DELETE requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = await self._make_request(**dict(
                method='DELETE',
                url=url,
                auth=self.auth,
                timeout=self.timeout,
                headers=self.request_headers
            ))
        except aiohttp.ClientError as e:
            raise e
        else:
            if r.status >= 400:
                raise MailChimpError(await r.json())
            if r.status == 204:
                return
            return await r.json()

    @_enabled_or_noop
    async def _patch(self, url, data=None):
        """
        Handle authenticated PATCH requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = await self._make_request(**dict(
                method='PATCH',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                headers=self.request_headers
            ))
        except aiohttp.ClientError as e:
            raise e
        else:
            if r.status >= 400:
                raise MailChimpError(await r.json())
            return await r.json()

    @_enabled_or_noop
    async def _put(self, url, data=None):
        """
        Handle authenticated PUT requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = await self._make_request(**dict(
                method='PUT',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                headers=self.request_headers
            ))
        except aiohttp.ClientError as e:
            raise e
        else:
            if r.status >= 400:
                raise MailChimpError(await r.json())
            return await r.json()
