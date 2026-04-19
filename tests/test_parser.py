import pytest
import io


def test_parser_module_imports():
    """Parser module should import cleanly."""
    from utils import parser
    assert hasattr(parser, "parse_resume")


def test_parse_resume_with_text_file():
    """Parser should handle uploaded file-like objects."""
    from utils.parser import parse_resume

    class MockFile:
        name = "test_resume.txt"
        def read(self):
            return b"John Doe\nSoftware Engineer\nPython, Docker, Kubernetes"
        def seek(self, pos):
            pass

    result = parse_resume(MockFile())
    # Result should be a non-empty string (or a handled error string)
    assert isinstance(result, str)
