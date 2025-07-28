"""
https://qiita.com/Tadataka_Takahashi/items/2f7a3e19ed084a7b4cf7
+AI-generated code
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import psutil
from datetime import datetime


class SystemMonitorApp:
    """Matplotlibを用いたTkinterベースのシステムモニタGUI"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("System Monitor (Matplotlib)")
        self.root.geometry("900x600")

        # -----------------------
        # コントロールパネル部分
        # -----------------------
        control_frame: ttk.Frame = ttk.Frame(root)
        control_frame.pack(fill="x", padx=10, pady=5)

        # 更新間隔の選択メニュー
        ttk.Label(control_frame, text="更新間隔 (秒):").pack(side="left", padx=5)
        self.interval_var: tk.StringVar = tk.StringVar(value="1")  # 初期値: 1秒
        interval_menu: ttk.OptionMenu = ttk.OptionMenu(
            control_frame, self.interval_var, "1", "1", "2", "5", "10"
        )
        interval_menu.pack(side="left")

        # 開始・停止ボタン
        self.toggle_button: ttk.Button = ttk.Button(
            control_frame, text="Stop", command=self.toggle_update
        )
        self.toggle_button.pack(side="left", padx=10)

        # ステータス表示（更新時間など）
        self.status_var: tk.StringVar = tk.StringVar()
        ttk.Label(root, textvariable=self.status_var).pack(pady=5)

        # ------------------------
        # Matplotlibグラフの設定
        # ------------------------
        self.figure: Figure = Figure(figsize=(8, 4), dpi=100)
        self.ax_cpu = self.figure.add_subplot(211)   # 上段：CPU使用率
        self.ax_mem = self.figure.add_subplot(212)   # 下段：メモリ使用率

        # 軸ラベルの設定
        self.ax_cpu.set_ylabel("CPU Usage (%)")
        self.ax_mem.set_ylabel("Memory Usage (%)")
        self.ax_mem.set_xlabel("Time (s)")

        # Tkinter に Matplotlib のグラフを埋め込む
        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # ===============================
        # 内部データ
        # ===============================
        # データ履歴（最新60個を保持）
        self.cpu_history    : list[float]   = []
        self.mem_history    : list[float]   = []
        self.time_history   : list[str]     = []
        self.max_points     : int           = 60    # 最大保持数（秒数）

        self.running        : bool          = True  # 更新ループの有効/無効
        self.update_graph()                         # 初回更新実行

    def toggle_update(self) -> None:
        """Start/Stopボタン押下時の処理"""
        self.running = not self.running
        self.toggle_button.configure(text="Stop" if self.running else "Start")
        if self.running:
            self.update_graph()

    def update_graph(self) -> None:
        """定期的に呼び出される：データ更新とグラフ描画"""
        if not self.running:
            return  # 停止中なら何もしない

        # -------------------------------
        # データ取得
        # -------------------------------
        # psutilでCPU・メモリ使用率を取得
        cpu: float = psutil.cpu_percent(interval=None)
        mem: float = psutil.virtual_memory().percent
        timestamp: str = datetime.now().strftime("%H:%M:%S")  # 現在時刻を取得

        # 履歴に追加
        self.cpu_history.append(cpu)
        self.mem_history.append(mem)
        self.time_history.append(timestamp)

        # 最大データ数を超えたら古いものを削除
        if len(self.cpu_history) > self.max_points:
            self.cpu_history.pop(0)
            self.mem_history.pop(0)
            self.time_history.pop(0)
            
            
        # -----------------------
        # グラフ描画処理
        # -----------------------
        self.ax_cpu.clear()
        self.ax_mem.clear()

        # 折れ線グラフを描画
        self.ax_cpu.plot(self.time_history, self.cpu_history, color='green', label='CPU')
        self.ax_mem.plot(self.time_history, self.mem_history, color='blue', label='Memory')

        # ラベルと軸設定
        self.ax_cpu.set_ylabel("CPU Usage (%)")
        self.ax_mem.set_ylabel("Memory Usage (%)")
        self.ax_mem.set_xlabel("Time")

        self.ax_cpu.set_ylim(0, 100)
        self.ax_mem.set_ylim(0, 100)

        self.ax_cpu.tick_params(axis='x', rotation=45)
        self.ax_mem.tick_params(axis='x', rotation=45)

        # グリッドを有効化
        self.ax_cpu.grid(True)
        self.ax_mem.grid(True)

        # Tkinterキャンバスに反映
        self.canvas.draw()

        # ステータス更新
        self.status_var.set(f"Last updated: {timestamp}  CPU: {cpu:.1f}%  Mem: {mem:.1f}%")

        # 指定された時間後に次の更新をスケジュール
        interval_ms = int(self.interval_var.get()) * 1000
        self.root.after(interval_ms, self.update_graph)


def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
