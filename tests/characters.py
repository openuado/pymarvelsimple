#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from pymarvelsimple.marvel import Marvel, EmptyPage


class MarvelTestCase(unittest.TestCase):
    """Test characters part"""
    def setUp(self):
        """To initalize marvel"""
        self.public = '53f6e384300d5a3010aab435f0d36342'
        self.private = 'b09a253cbf7c1f799a875231dfd7b11a60d48b40'
        self.marvel = Marvel(self.public, self.private)
        self.characters = self.marvel.characters_list()
        self.comics = self.marvel.characters_comics(1009664)
        self.events = self.marvel.characters_events(1009664)
        self.series = self.marvel.characters_series(1009664)
        self.stories = self.marvel.characters_stories(1009664)

    def _count_last_page(self, object_list):
        count = object_list.data.total % self.marvel.limit
        last_page = object_list.data.total / self.marvel.limit
        count_last_page = 10 if count == 0 else count

        if count != 0:
            last_page += 1

        return last_page, count_last_page

    def test_limit_max(self):
        self.assertRaises(
            ValueError, Marvel, self.public, self.private, '', 200)

    def test_characters_list(self):
        all_characters_name = [
            character.name for character in self.characters.data.results]

        self.assertEqual(len(self.characters.data.results), 10)
        self.assertIn(u'3-D Man', all_characters_name)
        self.assertNotIn(u'Professor X', self.characters)

    def test_characters_list_last_page(self):
        characters_last_page = self.marvel.characters_list(
            self.characters.last_page)
        last_page, count_last_page = self._count_last_page(self.characters)
        all_characters_name = [
            character.name for character in characters_last_page.data.results]

        self.assertEqual(characters_last_page.status, u'Ok')
        self.assertEqual(last_page, self.characters.last_page)
        self.assertEqual(len(characters_last_page.data.results),
                         count_last_page)
        self.assertIn(u'Zemo', all_characters_name)
        self.assertNotIn(u'Professor X', all_characters_name)

    def test_characters_list_empty_page(self):
        page = self.characters.data.total / self.marvel.limit + 42
        self.assertRaises(EmptyPage, self.marvel.characters_list, page)

    def test_characters_by_id(self):
        character = self.marvel.characters_detail_by_name(u'Thor')

        self.assertEqual(character.status, u'Ok')
        self.assertEqual(character.data.results.id, 1009664)
        self.assertTrue(character.data.results.description.startswith(
            u'As the Norse God of thunder and lightning'))
        self.assertNotEqual(character.data.results.name, u'Professor X')

    def test_characters_by_name(self):
        character = self.marvel.characters_detail_by_name(u'Thor')

        self.assertEqual(character.status, u'Ok')
        self.assertEqual(character.data.results.name, u'Thor')
        self.assertTrue(character.data.results.description.startswith(
            u'As the Norse God of thunder and lightning'))
        self.assertNotEqual(character.data.results.name, u'Professor X')

    def test_characters_comics_list(self):
        all_comics_title = [
            comic.title for comic in self.comics.data.results]

        self.assertEqual(len(self.comics.data.results), 10)
        self.assertIn(u'Inhuman (2014) #4', all_comics_title)
        self.assertNotIn(u'Avengers (2010) #26', all_comics_title)

    def test_characters_comics_last_page(self):
        comics_last_page = self.marvel.characters_comics(
            1009664, self.comics.last_page)
        all_comics_title = [
            comic.title for comic in comics_last_page.data.results]
        last_page, count_last_page = self._count_last_page(self.comics)

        self.assertEqual(comics_last_page.status, u'Ok')
        self.assertEqual(last_page, self.comics.last_page)
        self.assertEqual(len(comics_last_page.data.results),
                         count_last_page)
        self.assertIn(u'Journey Into Mystery (1952) #88', all_comics_title)
        self.assertNotIn(u'Avengers (2010) #26', all_comics_title)

    def test_characters_comics_list_empty_page(self):
        page = self.comics.data.total / self.marvel.limit + 42
        self.assertRaises(
            EmptyPage, self.marvel.characters_comics, 1009664, page)

    def test_characters_series_list(self):
        all_series_title = [
            serie.title for serie in self.series.data.results]

        self.assertEqual(len(self.series.data.results), 10)
        self.assertIn(u'Alpha Flight Classic Vol. 1 (2007)', all_series_title)
        self.assertNotIn(u'Avengers Assemble (2004)', all_series_title)

    def test_characters_series_last_page(self):
        series_last_page = self.marvel.characters_series(
            1009664, self.series.last_page)
        all_series_title = [
            serie.title for serie in series_last_page.data.results]
        last_page, count_last_page = self._count_last_page(self.series)

        self.assertEqual(series_last_page.status, u'Ok')
        self.assertEqual(last_page, self.series.last_page)
        self.assertEqual(len(series_last_page.data.results),
                         count_last_page)
        self.assertIn(u'X-Treme X-Men (2001 - 2004)', all_series_title)
        self.assertNotIn(u'Avengers Assemble (2004)', all_series_title)

    def test_characters_series_list_empty_page(self):
        page = self.series.data.total / self.marvel.limit + 42
        self.assertRaises(
            EmptyPage, self.marvel.characters_series, 1009664, page)

    def test_characters_stories_list(self):
        all_stories_title = [
            story.title for story in self.stories.data.results]

        self.assertEqual(len(self.stories.data.results), 10)
        self.assertIn(u'Interior #879', all_stories_title)
        self.assertNotIn(u'Interior #975', all_stories_title)

    def test_characters_stories_last_page(self):
        stories_last_page = self.marvel.characters_stories(
            1009664, self.stories.last_page)
        all_stories_title = [
            story.title for story in stories_last_page.data.results]
        last_page, count_last_page = self._count_last_page(self.stories)

        self.assertEqual(stories_last_page.status, u'Ok')
        self.assertEqual(last_page, self.stories.last_page)
        self.assertEqual(len(stories_last_page.data.results),
                         count_last_page)
        self.assertIn(u'Cover #97040', all_stories_title)
        self.assertNotIn(u'Interior #975', all_stories_title)

    def test_characters_stories_list_empty_page(self):
        page = self.stories.data.total / self.marvel.limit + 42
        self.assertRaises(
            EmptyPage, self.marvel.characters_stories, 1009664, page)
