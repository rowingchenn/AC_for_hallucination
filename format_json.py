#!/usr/bin/env python3
import json
import os
import sys
import argparse


def format_json_file(file_path, indent=4, sort_keys=False):
    """Format a JSON file and save it back to the same location."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, sort_keys=sort_keys)

        print(f"Successfully formatted: {file_path}")
        return True
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file")
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False


def format_jsonl_file(file_path, indent=4, sort_keys=False):
    """Format each line in a JSONL file and save it back to the same location."""
    try:
        valid_lines = []
        invalid_lines = 0

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    data = json.loads(line)
                    valid_lines.append(data)
                except json.JSONDecodeError:
                    invalid_lines += 1
                    print(
                        f"Warning: Line {line_num} in {file_path} is not valid JSON, skipping"
                    )

        if invalid_lines > 0:
            print(f"Found {invalid_lines} invalid JSON lines in {file_path}")

        if valid_lines:
            with open(file_path, "w", encoding="utf-8") as f:
                for data in valid_lines:
                    json_str = json.dumps(
                        data, indent=indent, ensure_ascii=False, sort_keys=sort_keys
                    )
                    f.write(json_str + "\n")

            print(f"Successfully formatted: {file_path} ({len(valid_lines)} lines)")
            return True
        else:
            print(f"No valid JSON lines found in {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False


def format_directory(directory, indent=4, sort_keys=False, recursive=False):
    """Format all JSON files in the given directory."""
    success_count = 0
    error_count = 0

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".json"):
                file_path = os.path.join(root, file)
                if format_json_file(file_path, indent, sort_keys):
                    success_count += 1
                else:
                    error_count += 1
            elif file.lower().endswith(".jsonl"):
                file_path = os.path.join(root, file)
                if format_jsonl_file(file_path, indent, sort_keys):
                    success_count += 1
                else:
                    error_count += 1

        if not recursive:
            break  # Only process the top-level directory

    print(
        f"\nCompleted. Successfully formatted {success_count} files. Errors: {error_count}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Format JSON and JSONL files in a directory"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory containing JSON/JSONL files (default: current directory)",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=4,
        help="Number of spaces for indentation (default: 4)",
    )
    parser.add_argument(
        "-s", "--sort-keys", action="store_true", help="Sort keys alphabetically"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively",
    )

    args = parser.parse_args()

    format_directory(args.directory, args.indent, args.sort_keys, args.recursive)


if __name__ == "__main__":
    main()
