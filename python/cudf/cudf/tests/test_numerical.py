import numpy as np

from cudf import Series


def test_overflow_safe_to_same_kind():
    data = Series([1, 2, 3], dtype="int32")._column
    to_dtype = np.dtype("int64")

    assert data.overflow_safe_to(to_dtype)

    data = Series([1, 2, 3], dtype="int64")._column
    to_dtype = np.dtype("int32")

    assert data.overflow_safe_to(to_dtype)

    data = Series([1, 2, 2 ** 31], dtype="int64")._column
    assert not data.overflow_safe_to(to_dtype)


def test_overflow_safe_to_mixed_kind():
    data = Series([1, 2, 3], dtype="int32")._column
    to_dtype = np.dtype("float32")
    assert data.overflow_safe_to(to_dtype)

    # too big to fit into f32 exactly
    data = Series([1, 2, 2 ** 24 + 1], dtype="int32")._column
    assert not data.overflow_safe_to(to_dtype)

    to_dtype = np.dtype("float64")
    assert data.overflow_safe_to(to_dtype)

    data = Series([1.0, 2.0, 3.0], dtype="float32")._column
    to_dtype = np.dtype("int32")
    assert data.overflow_safe_to(to_dtype)

    # not integer float
    data = Series([1.0, 2.0, 3.5], dtype="float32")._column
    assert not data.overflow_safe_to(to_dtype)

    # float out of int range
    data = Series([1.0, 2.0, 1.0 * (2 ** 31)], dtype="float32")._column
    assert not data.overflow_safe_to(to_dtype)
