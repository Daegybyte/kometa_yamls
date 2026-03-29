from comment_block import normalise_text, comment_block

# pylint: disable=missing-function-docstring


###########################
## text normaliser tests ##
###########################
def test_normalise_text_casefold():
    assert normalise_text("HELLO") == "hello"


def test_normalise_text_strips_whitespace():
    assert normalise_text("  hello  ") == "hello"


def test_normalise_text_removes_punctuation():
    assert normalise_text("hello!") == "hello"


def test_normalise_text_removes_special_chars():
    assert normalise_text("hello@#$%") == "hello"


def test_normalise_text_empty_string():
    assert normalise_text("") == ""


def test_normalise_text_numbers_preserved():
    assert normalise_text("hello123") == "hello123"


#########################
## comment block tests ##
#########################
def test_comment_block_border_length(capsys):
    comment_block("hello")
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert lines[0] == "###########"
    assert lines[2] == "###########"


def test_comment_block_middle(capsys):
    comment_block("hello")
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert lines[1] == "## hello ##"


def test_comment_block_normalises_input(capsys):
    comment_block("HELLO!")
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert lines[1] == "## hello ##"
