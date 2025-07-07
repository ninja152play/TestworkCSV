import pytest
import os
import tempfile
from csv_processor import CSVProcessor

@pytest.fixture
def sample_csv():
    """Создаем временный CSV файл для тестов."""
    content = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
        os.unlink(f.name)


def test_filter_equals(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.filter_data("brand=apple")
    assert len(result) == 1
    assert result[0]["name"] == "iphone 15 pro"

def test_filter_greater(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.filter_data("price>500")
    assert len(result) == 2
    assert all(float(row["price"]) > 500 for row in result)

def test_filter_less(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.filter_data("rating<4.7")
    assert len(result) == 2
    assert all(float(row["rating"]) < 4.7 for row in result)

def test_aggregate_avg(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.aggregate_data(None, "price=avg")
    assert pytest.approx(result["avg"]) == (999 + 1199 + 199 + 299) / 4

def test_aggregate_min(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.aggregate_data("brand=xiaomi", "price=min")
    assert result["min"] == 199

def test_aggregate_max(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.aggregate_data(None, "rating=max")
    assert result["max"] == 4.9

def test_invalid_where(sample_csv):
    processor = CSVProcessor(sample_csv)
    with pytest.raises(ValueError):
        processor.filter_data("price!1000")
    with pytest.raises(ValueError):
        processor.filter_data(">100")
    with pytest.raises(ValueError):
        processor.filter_data("price>>100")
    with pytest.raises(ValueError):
        processor.filter_data("invalid_where")

def test_invalid_aggregate(sample_csv):
    processor = CSVProcessor(sample_csv)
    with pytest.raises(ValueError):
        processor.aggregate_data(None, "invalid=operation")
    with pytest.raises(ValueError):
        processor.aggregate_data(None, "=avg")
    with pytest.raises(ValueError):
        processor.aggregate_data(None, "price=")
    with pytest.raises(ValueError):
        processor.filter_data("invalid_aggregate")

def test_invalid_orderby(sample_csv):
    processor = CSVProcessor(sample_csv)
    with pytest.raises(ValueError):
        processor.order_by_data("invalid_column")
    with pytest.raises(ValueError):
        processor.order_by_data("price!desc")
    with pytest.raises(ValueError):
        processor.order_by_data("=asc")
    with pytest.raises(ValueError):
        processor.order_by_data("")


def test_invalid_csv():
    with pytest.raises(FileNotFoundError):
        CSVProcessor("nonexistent.csv")

def test_compare_equal_values():
    assert CSVProcessor._compare_values("10", "10") == 0
    assert CSVProcessor._compare_values("text", "text") == 0