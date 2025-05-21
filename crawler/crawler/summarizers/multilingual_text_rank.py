from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.utils import get_stop_words

from crawler.models import EvaluatedSentence


class MultilingualTextRankSummarizer:
    def __init__(self):
        self._tokenizers = {}
        self._summarizers = {}

    def __call__(self, text: str, language: str, max_words_count: int) -> list[str]:
        evaluated_sentences = self._evaluate_sentences(text, language)

        summary_sentences, summary_words_count = [], 0

        for sentence in evaluated_sentences:
            sentence_words_count = len(sentence.value.words)

            if summary_words_count + sentence_words_count > max_words_count:
                continue

            summary_sentences.append(sentence)

            summary_words_count += sentence_words_count

        return [str(sentence.value) for sentence in sorted(summary_sentences, key=lambda s: s.order)]

    def _evaluate_sentences(self, text: str, language: str) -> list[EvaluatedSentence]:
        summarizer = self._get_summarizer(language)

        parser = PlaintextParser.from_string(text, self._get_tokenizer(language))

        ratings = summarizer.rate_sentences(parser.document)

        evaluated_sentences = [
            EvaluatedSentence(
                value=sentence,
                order=order,
                rating=ratings[sentence]
            )
            for order, sentence in enumerate(parser.document.sentences)
        ]

        return sorted(evaluated_sentences, key=lambda s: s.rating, reverse=True)

    def _get_tokenizer(self, language: str) -> Tokenizer:
        return self._tokenizers.setdefault(language, Tokenizer(language))

    def _get_summarizer(self, language: str) -> TextRankSummarizer:
        summarizer = self._summarizers.setdefault(language, TextRankSummarizer())

        if not summarizer.stop_words:
            summarizer.stop_words = get_stop_words(language)

        return summarizer
