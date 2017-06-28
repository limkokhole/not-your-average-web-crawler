# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Tijme Gommers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy

try: # Python 3
    from urllib.parse import urlparse
except: # Python 2
    from urlparse import urlparse

from nyawc.helpers.URLHelper import URLHelper

class HTTPRequestHelper:
    """A helper for the src.http.Request module."""

    @staticmethod
    def patch_with_options(request, options, parent_queue_item=None):
        """Patch the given request with the given options (e.g. user agent).

        Args:
            request (:class:`nyawc.http.Request`): The request to patch.
            options (:class:`nyawc.Options`): The options to patch the request with.
            parent_queue_item (:class:`nyawc.QueueItem`): The parent queue item object (request/response pair) if exists.

        """

        request.auth = copy.deepcopy(options.identity.auth)
        request.cookies = copy.deepcopy(options.identity.cookies)
        request.headers = copy.deepcopy(options.identity.headers)
        request.proxies = copy.deepcopy(options.identity.proxies)

        if parent_queue_item != None:
            for cookie in parent_queue_item.request.cookies:
                request.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

            for cookie in parent_queue_item.response.cookies:
                request.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

    @staticmethod
    def complies_with_scope(queue_item, new_request, scope):
        """Check if the new request complies with the crawling scope.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The parent queue item of the new request.
            new_request (:class:`nyawc.http.Request`): The request to check.
            scope (:class:`nyawc.Options.OptionsScope`): The scope to check.

        Returns:
            bool: True if it complies, False otherwise.

        """

        if not URLHelper.is_parsable(queue_item.request.url):
            return False

        if not URLHelper.is_parsable(new_request.url):
            return False

        if scope.protocol_must_match:
            if URLHelper.get_protocol(queue_item.request.url) != URLHelper.get_protocol(new_request.url):
                return False

        if scope.subdomain_must_match:
            if URLHelper.get_subdomain(queue_item.request.url) != URLHelper.get_subdomain(new_request.url):
                return False

        if scope.hostname_must_match:
            if URLHelper.get_hostname(queue_item.request.url) != URLHelper.get_hostname(new_request.url):
                return False

        if scope.tld_must_match:
            if URLHelper.get_tld(queue_item.request.url) != URLHelper.get_tld(new_request.url):
                return False

        return True