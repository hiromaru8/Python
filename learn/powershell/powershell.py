import subprocess
import json

def run_powershell_command(command):
    # PowerShellコマンドを実行し、標準出力をキャプチャする
    #result = subprocess.run(["powershell", command], capture_output=True, text=True)
    result = subprocess.run(["powershell", command," | ConvertTo-Json -Compress"], capture_output=True, text=True)

    # PowerShellの結果をJSONオブジェクトに変換する
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = result.stdout.strip()

    return output

# PowerShellコマンドを実行してオブジェクトを取得する例
#ps_command = 'Get-Process | Select-Object Name, CPU | ConvertTo-Json -Compress'
ps_command = 'Get-Process | Select-Object Name, CPU '
processes = run_powershell_command(ps_command)

# 取得したプロセスの情報を表示する例
for process in processes:
    if isinstance(process, dict):
        print(f"Name: {process['Name']}, CPU Usage: {process['CPU']}")


