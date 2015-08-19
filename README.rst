Introduction
============
PyMarvelSimple is a wrapper for Marvel API. Abstract the authorization and API
call.

Example:

.. code-block:: python

    from pymarvelsimple.marvel import Marvel

    marvel = Marvel(self.public, self.private)
    characters = marvel.characters_list()

    for character in characters.data.results:
        print character.name

    print characters.last_page

    character = marvel.characters_detail_by_name(u'Thor')
    print character.data.results.name

Play with marvel.
