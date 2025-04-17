import argparse
import os
import json
import re
from collections import defaultdict

regex_for_parser = r'(?P<ip>[\d\.]+) .* (?P<time>\[.*?\]) "(?P<request>[^"]*.*)" (?P<status>\d{3}) (?P<bytes>\d+|-) "(?P<referer>[^"]*.*)" "(?P<user_agent>[^"]*.*)" (?P<duration>\d+)'


def analyze_log_file(file_path):
    result = {
        "top_ips": defaultdict(int),
        "top_longest": [],
        "total_stat": defaultdict(int),
        "total_requests": 0,
    }
    with open(file_path, "r") as file:
        for line in file:
            match = re.compile(regex_for_parser).match(line)
            result["total_requests"] += 1
            request = match.group("request")
            method = request.split()[0]
            ip = match.group("ip")
            duration = int(match.group("duration"))
            result["total_stat"][method] += 1
            result["top_ips"][ip] += 1
            result["top_longest"].append(
                {
                    "ip": ip,
                    "date": match.group("time"),
                    "method": method,
                    "url": match.group("referer"),
                    "duration": duration,
                }
            )
    result["top_ips"] = dict(
        sorted(result["top_ips"].items(), key=lambda x: x[1], reverse=True)[:3]
    )
    result["top_longest"] = sorted(
        result["top_longest"], key=lambda x: x["duration"], reverse=True
    )[:3]
    return result


def print_and_save_results(result, file_path):
    with open(file_path.replace(".log", "_stats.json"), "w") as json_file:
        json.dump(result, json_file, indent=4)
    print(f"Статистика для {file_path}:")
    print(json.dumps(result, indent=4))


def analyze_log_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            file_path = os.path.join(directory, filename)
            stats = analyze_log_file(file_path)
            print_and_save_results(stats, file_path)


parser = argparse.ArgumentParser()
parser.add_argument("path_to_logs", help="Путь к директории или файлу лога")
args = parser.parse_args()

if os.path.isdir(args.path_to_logs):
    analyze_log_directory(args.path_to_logs)
elif os.path.isfile(args.path_to_logs):
    print_and_save_results(analyze_log_file(args.path_to_logs), args.path_to_logs)
