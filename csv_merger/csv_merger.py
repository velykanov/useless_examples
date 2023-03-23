import csv
import os
import sys

from datetime import datetime

print("HELLO")


def merge_files(first_path: str, second_path: str, prune_duplicates: bool = True) -> str:
    with open(first_path) as first_file, open(second_path) as second_file:
        first_reader = csv.DictReader(first_file)
        second_reader = csv.DictReader(second_file)

        assert first_reader.fieldnames == second_reader.fieldnames, 'Files must share the same structure'

        if not os.path.exists('merged'):
            os.mkdir('merged')

        first_filename = first_path.rsplit('/', 1)[-1]
        second_filename = second_path.rsplit('/', 1)[-1]
        now = int(datetime.now().timestamp() * 1e6)
        output_path = os.path.join('merged', f'{now}_{first_filename}_{second_filename}')
        with open(output_path, 'w') as output_file:
            output_writer = csv.DictWriter(output_file, first_reader.fieldnames)
            output_writer.writeheader()
            if not prune_duplicates:
                output_writer.writerows(first_reader)
                output_writer.writerows(second_reader)
            else:
                output_data = list(first_reader)
                output_data.extend(second_reader)
                output_writer.writerows(
                    (
                        dict(t) for t in {
                            # sorted might be unnecessary but still to ensure right order
                            tuple(sorted(d.items(), key=lambda el: el[0])) for d in output_data
                        }
                    )
                )

            return os.path.join('merged', f'{first_filename}_{second_filename}')


if __name__ == '__main__':
    prune_duplicates = True if sys.argv[1] == 'prune' else False
    files_list = sys.argv[2:]

    init = files_list[0]
    for file_path in files_list[1:]:
        init = merge_files(init, file_path, prune_duplicates)
