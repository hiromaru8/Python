# parse_logfile.py
  ログファイルを読み込み、 CSVファイルに変換する

  logファイルの例）<br>
  2023-07-30 12:01:23,456 [INFO] This is the first log message.<br>
  2023-07-30 12:02:34,567 [ERROR] Error occurred: Something went wrong.<br>
  2023-07-30 12:03:45,678 [DEBUG] Debugging information.<br>
  This line and the next should be part of the previous log message.<br>
  2023-07-30 12:04:56,789 [INFO] Another log message.<br>
  This line and the next should be part of the previous log message.<br>
  This line and the next should be part of the previous log message.<br>
  output to CSV)<br>
  index,Timestamp,Log Level,Message<br>
  1,"2023-07-30 12:01:23,456",INFO,This is the first log message.<br>
  2,"2023-07-30 12:02:34,567",ERROR,Error occurred: Something went wrong.<br>
  3,"2023-07-30 12:03:45,678",DEBUG,"Debugging information.This line and the next should be part of the previous log message.
  "<br>
  4,"2023-07-30 12:04:56,789",INFO,"Another log message.This line and the next should be part of the previous log message.
  This line and the next should be part of the previous log message.
