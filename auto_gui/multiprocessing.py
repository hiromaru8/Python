from concurrent.futures import ProcessPoolExecutor
from pywinauto.findwindows import find_elements
from pywinauto import Application

def worker(pid, text):
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Tera .*")
    edit = win.child_window(title="ホスト(T):", control_type="Edit")
    edit.set_edit_text(f"pid {pid} のSakuraに直接書き込んでいます！:{text}")


def get_pids(name):
    # return [p.info["pid"] for p in psutil.process_iter(["pid", "name"]) if p.info["name"].lower() == name.lower()]
    elements = find_elements(title_re=name)
    return [e.process_id for e in elements]

if __name__ == "__main__":
    pids = get_pids(".*Tera.*")
    print(f"対象: {len(pids)} プロセス")


    # 並列数を10に制限
    with ProcessPoolExecutor(max_workers=10) as executor:
        for i, pid in enumerate(pids, 1):
            executor.submit(worker, pid, f"Parallel writing {i}\n")

    print("完了！")
