import pytest

def test_load_data_function_exists():
    """
    Test that the load_data function can be imported.
    This test is expected to FAIL initially (Red phase) because the function
    has not been implemented yet.
    """
    try:
        # Correct import: we import directly from the package inside src
        from data_processing.loader import load_data
    except ImportError:
        pytest.fail("Could not import 'load_data'. Function implementation is missing.")
    except Exception as e:
        pytest.fail(f"Unexpected error during import: {e}")

def test_load_data_handles_missing_file():
    """
    Test that load_data raises a FileNotFoundError when the file path is invalid.
    """
    # Attempt to import first; if this fails, we can't run the logic test.
    try:
        from data_processing.loader import load_data
    except ImportError:
        pytest.skip("Skipping logic test: load_data function not found.")

    # Verify that the function correctly identifies a missing file
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")