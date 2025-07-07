import csv
from typing import List, Dict, Any, Optional, Tuple


class CSVProcessor:
    """Класс для обработки CSV файлов."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        """Загрузка данных из CSV файла."""
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def filter_data(self, where: Optional[str] = None) -> List[Dict[str, Any]]:
        """Фильтрация данных по условию."""
        if not where:
            return self.data

        column, operation, value = self._parse_where(where)

        filtered_data = []
        for row in self.data:
            row_value = row.get(column)
            if row_value is None:
                continue

            if operation == "=" and str(row_value) == value:
                filtered_data.append(row)
            elif operation == ">" and self._compare_values(row_value, value) > 0:
                filtered_data.append(row)
            elif operation == "<" and self._compare_values(row_value, value) < 0:
                filtered_data.append(row)

        return filtered_data

    def aggregate_data(
        self, where: Optional[str] = None, aggregate: Optional[str] = None
    ) -> Dict[str, Any]:
        """Агрегация данных по условию."""
        if not aggregate:
            raise ValueError("Aggregate parameter is required.")

        column, operation = self._parse_aggregate(aggregate)
        filtered_data = self.filter_data(where)

        numeric_values = []
        for row in filtered_data:
            try:
                value = float(row.get(column, 0))
                numeric_values.append(value)
            except (ValueError, TypeError):
                continue

        if not numeric_values:
            return {operation: "No numeric values found"}

        if operation == "avg":
            result = sum(numeric_values) / len(numeric_values)
        elif operation == "min":
            result = min(numeric_values)
        elif operation == "max":
            result = max(numeric_values)
        else:
            raise ValueError(f"Unsupported aggregate operation: {operation}")

        return {operation: result}

    def order_by_data(
        self, where: Optional[str] = None, order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Сортировка данных по колонке."""
        if not order_by:
            raise ValueError("Order by parameter is required.")

        column, order = self._parse_orderby(order_by)
        filtered_data = self.filter_data(where)
        sorted_data = sorted(
            filtered_data, key=lambda x: x[column], reverse=(order == "desc")
        )

        return sorted_data

    @staticmethod
    def _parse_where(where: str) -> Tuple[str, str, str]:
        """Разбить where на части."""
        operations = ["=", ">", "<"]
        for op in operations:
            if op in where:
                parts = where.split(op)
                if len(parts) == 2:
                    if not parts[0].strip() or not parts[1].strip():
                        raise ValueError(f"Invalid where condition: {where}")
                    return parts[0].strip(), op, parts[1].strip()
        raise ValueError(f"Invalid where condition: {where}")

    @staticmethod
    def _parse_aggregate(aggregate: str) -> Tuple[str, str]:
        """Разбить aggregate на части."""
        if "=" not in aggregate:
            raise ValueError("Aggregate format should be 'operation=column'")
        column, operation = aggregate.split("=", 1)
        if len(column) == 0 or len(operation) == 0:
            raise ValueError("Aggregate format should be 'operation=column'")
        return column.strip(), operation.strip()

    @staticmethod
    def _parse_orderby(order_by: str) -> Tuple[str, str]:
        """Разбить order_by на части."""
        if "=" not in order_by:
            raise ValueError("Order by format should be 'column=asc|desc'")
        column, order = order_by.split("=", 1)
        return column.strip(), order.strip()

    @staticmethod
    def _compare_values(value1: Any, value2: Any) -> int:
        """Сравнить значения."""
        try:
            value1_num, value2_num = float(value1), float(value2)
            if value1_num == value2_num:
                return 0
            return 1 if value1_num > value2_num else -1
        except ValueError:
            value1_str, value2_str = str(value1), str(value2)
            if value1_str == value2_str:
                return 0
            return 1 if value1_str > value2_str else -1
