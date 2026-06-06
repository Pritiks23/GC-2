class LLMProvider:
    def call(self, messages, max_tokens):
        raise NotImplementedError
