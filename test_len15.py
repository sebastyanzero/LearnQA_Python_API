class TestLen15:
    def test_len_phrase(self):
        phrase = input("Set a phrase: ")
        count_phrase=len(phrase)
        assert len(phrase) < 15, f"Фраза длиной {count_phrase} не меньше 15 символов"