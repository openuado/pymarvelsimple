import datetime
import hashlib
import json
import urllib

from bunch import bunchify
import requests


class EmptyPage(Exception):
    pass


class Marvel(object):
    """A wrapper for Marvel API, easy to use."""
    def __init__(self, public, private,
                 url='http://gateway.marvel.com/v1/public', limit=10):
        """To initialize the class.

        @param public: The public key
        @type public: str

        @param private: The private key
        @type private: str

        @param url: The API url (default http://gateway.marvel.com/v1/public)
        @type url: str

        @param limit: Item per page used for list (default 10)
        @type limit: int

        @raise ValueError: Item per page is limited to 100
        """
        if limit > 100:
            raise ValueError('Limit greater than 100')

        self.public = public
        self.private = private
        self.url = url
        self.limit = limit

    def _auth_acces(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        hash_auth = hashlib.md5('{date}{private}{public}'.format(
            date=now, private=self.private, public=self.public)).hexdigest()
        querystring = "?ts={date}&apikey={public}&hash={hash_auth}".format(
            date=now, public=self.public, hash_auth=hash_auth)

        return querystring

    def _call_api(self, method, page=None, extra_parameters={}):
        querystring = ''

        if page:
            offset = 0 if page == 1 else self.limit * page - self.limit
            querystring = '&limit={limit}&offset={offset}'.format(
                limit=self.limit, offset=offset)

        if extra_parameters:
            querystring += '&' + urllib.urlencode(extra_parameters)

        if querystring:
            return json.loads(requests.get('{url}/{method}{auth}{qs}'.format(
                url=self.url, method=method, auth=self._auth_acces(),
                qs=querystring)).text)

        return json.loads(requests.get('{url}/{method}{auth}'.format(
            url=self.url, method=method, auth=self._auth_acces())).text)

    def _set_last_page(self, object_list, page):
        if object_list.data.total % self.limit == 0:
            object_list.last_page = int(object_list.data.total / self.limit)
        else:
            object_list.last_page = int(
                object_list.data.total / self.limit) + 1

        if page > object_list.last_page:
            raise EmptyPage('The last page is {last_page}'.format(
                last_page=object_list.last_page))

    def characters_list(self, page=1, *args, **kwargs):
        """Get list of characters.

        @param page: Page to get (default 1)
        @type page: int

        @return: A list characters
        @rtype : dict

        @raise EmptyPage: A empty page
        """
        characters = bunchify(self._call_api('characters', page, kwargs))
        self._set_last_page(characters, page)

        return characters

    def characters_detail_by_name(self, name, *args, **kwargs):
        """Get a character by name.

        @param pk: The name of the character
        @type  pk: str

        @return: The character detail
        @rtype : dict

        @raise EmptyPage: The character not found
        """
        kwargs['name'] = name
        characters = bunchify(
            self._call_api('characters', extra_parameters=kwargs))

        if not characters.data.results:
            raise EmptyPage('Not found this characters {name}'.format(
                name=name))

        characters.data.results = characters.data.results[0]

        return characters

    def characters_detail_by_id(self, pk, *args, **kwargs):
        """Get a character by id.

        @param pk: The id of the character
        @type  pk: int

        @return: The character detail
        @rtype : dict

        @raise EmptyPage: The character not found
        """
        character = bunchify(self._call_api('characters/{pk}'.format(pk=pk)))

        if character.code == 404:
            raise EmptyPage('{message} with id: {pk}'.format(
                message=character.status, pk=pk))

        character.data.results = character.data.result[0]

        return character

    def characters_comics(self, pk, page=1, *args, **kwargs):
        """List of comics filtered by a character id.

        @param pk: The id of the character
        @type pk: int

        @param page: Page to get (default 1)
        @type page: int

        @return: Comics list
        @rtype : dict

        @raise EmptyPage: A empty page
        """
        comics = bunchify(self._call_api('characters/{pk}/comics'.format(
            pk=pk), page))
        self._set_last_page(comics, page)

        return comics

    def characters_events(self, pk, page=1, *args, **kwargs):
        """List of events filtered by a character id.

        @param pk: The id of the character
        @type pk: int

        @param page: Page to get (default 1)
        @type page: int

        @return: Events list
        @rtype : dict

        @raise EmptyPage: A empty page
        """
        events = bunchify(self._call_api('characters/{pk}/events'.format(
            pk=pk), page))
        self._set_last_page(events, page)

        return events

    def characters_series(self, pk, page=1, *args, **kwargs):
        """List of series filtered by a character id.

        @param pk: The id of the character
        @type pk: int

        @param page: Page to get (default 1)
        @type page: int

        @return: Series list
        @rtype : dict

        @raise EmptyPage: A empty page
        """
        series = bunchify(self._call_api('characters/{pk}/series'.format(
            pk=pk), page))
        self._set_last_page(series, page)

        return series

    def characters_stories(self, pk, page=1, *args, **kwargs):
        """List of stories filtered by a character id.

        @param pk: The id of the character
        @type pk: int

        @param page: Page to get (default 1)
        @type page: int

        @return: Stories list
        @rtype : dict

        @raise EmptyPage: A empty page
        """
        stories = bunchify(self._call_api('characters/{pk}/stories'.format(
            pk=pk), page))
        self._set_last_page(stories, page)

        return stories
