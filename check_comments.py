import os
import ast


def calculate_comment_percentage(directory):
    total_lines = 0
    comment_lines = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    comment_lines += sum(1 for line in lines if line.strip().startswith('#'))

    return (comment_lines / total_lines) * 100 if total_lines > 0 else 0


if __name__ == "__main__":
    directory_to_check = 'src'
    comment_percentage = calculate_comment_percentage(directory_to_check)
    print(f"Comment percentage: {comment_percentage:.2f}%")
    if comment_percentage < 10:
        print("Error: Comment percentage is below the threshold of 10%")
        exit(1)
