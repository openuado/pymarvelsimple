Introduction
============
PyMarvelSimple is a wrapper for Marvel API. Abstract the authorization and API
call.

Example:

.. code-block:: python

    from pymarvelsimple.marvel import Marvel, EmptyPage
    marvel = Marvel(self.public, self.private)
    characters = self.characters.data.results

    for character in characters:
        print character.name

    print characters.last_name
    marvel.characters_detail_by_name(u'Thor')
    print character.data.results.name

Play with marvel.
