import click

import wakeword_training_record.create


@click.group()
def WTRtool():
    pass


@WTRtool.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("wakeword")
@click.argument("language")
def create(**kwargs):
    path = kwargs["path"]
    wakeword = kwargs["wakeword"]
    language = kwargs["language"]
    try:
        language_code = wakeword_training_record.create.getLanguageCode(language)
    except ValueError as e:
        print(f"Problem with language: {e}")
    wakeword_training_record.create.create(path, wakeword, language_code)


if __name__ == "__main__":
    WTRtool()
