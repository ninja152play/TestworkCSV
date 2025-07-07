import argparse
from tabulate import tabulate

from csv_processor import CSVProcessor

def main():
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="CSV processor")
    parser.add_argument("--file", type=str, help="Path to csv file",)
    parser.add_argument("--where", type=str, help="Filtering with operators", default=None,)
    parser.add_argument("--aggregate", type=str, help="Aggregation with calculation", default=None,)
    parser.add_argument("--orderby", type=str, help="Order by column", default=None,)
    args = parser.parse_args()

    try:
        processor = CSVProcessor(args.file)

        if args.orderby:
            result = processor.order_by_data(args.where, args.orderby)
            print(tabulate(result, headers="keys", tablefmt="grid"))
        elif args.aggregate:
            result = processor.aggregate_data(args.where, args.aggregate)
            print(tabulate([result], headers="keys", tablefmt="grid"))
        else:
            data = processor.filter_data(args.where)
            print(tabulate(data, headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()