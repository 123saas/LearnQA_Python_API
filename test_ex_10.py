# -*- coding: utf-8 -*-
class TestExample:
    def test_check_phrase(self):
        phrase = input("Set a phrase: ")
        len_phrase = len(phrase)
        assert len_phrase < 15, f"Количество символов в фразе = {len_phrase}"
