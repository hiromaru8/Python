import re
import csv

class LogParser:
    """
    Mixin class to parse log files and store log information.
    """
    log_pattern = ""
    csv_heder = []
    def __init__(self) -> None:
        self.logs = []
        self.previous_message = ""
        self.index = 0        
        pass
    
    def parse_log_file(self, log_file_path):
        """
        Parse the specified log file and store log information in a list.

        Args:
            log_file_path (str): The path of the log file to parse.

        Returns:
            None
        """
        with open(log_file_path, 'r') as file:
            for line in file:
                match = self.log_pattern.match(line)
                if match:
                    self.index += 1
                    timestamp, log_level, message = match.groups()
                    self.logs.append([self.index, timestamp, log_level, message])
                    self.previous_message = message
                else:
                    # マッチしなかった場合、前行のmessageに追加
                    self.previous_message += line 
                    if self.logs:
                        self.logs[-1][3] = self.previous_message

    def write_to_csv(self, output_csv_file):
        """
        Write the parsed log information to a CSV file.

        Args:
            output_csv_file (str): The path of the CSV file to write.

        Returns:
            None
        """
        with open(output_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # CSVファイルにヘッダーを書き込む
            writer.writerow(self.csv_heder)
            # ログをCSVファイルに書き込む
            writer.writerows(self.logs)


class LogParser1(LogParser):
    log_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+\[(\w+)\]\s+(.+)$')
    # yyyy-mm-dd hh:mm:ss,SSS [Log Level] Message........
    # d{4} : \dは数字、{4}は4回繰り返しを意味する
    # \w+は1つ以上の英数字またはアンダースコアにマッチ。[]で囲まれた部分はログレベルを表しています。
    # \s+: 1つ以上の空白文字（スペース、タブ、改行など）にマッチします。
    csv_heder = ['index', 'Timestamp', 'Log Level', 'Message']




if __name__ == "__main__":
    log_parser = LogParser1()
    log_file_path = "D:\Learnning\Python\parseLogfile\sample.log"  # 解析するlogファイルのパスを指定
    output_csv_file = "D:\Learnning\Python\parseLogfile\output_logs2.csv"  # 出力するCSVファイルの名前を指定

    log_parser.parse_log_file(log_file_path)
    log_parser.write_to_csv(output_csv_file)
