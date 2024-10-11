from src.utils.openai_utils import get_completions


def translate(text: str, lang: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a professional book translator."
        },
        {
            "role": "user",
            "content": f"Translate the following text into langauge {lang}:\n\n{text}"
        }
    ]

    return get_completions({"messages": messages})["message"]["content"]


if __name__ == '__main__':
    print(translate("In consequence I’m inclined to reserve all judgments", "zh-cn"))
