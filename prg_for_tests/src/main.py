import os
import argparse
from lib.file_glob import *

def main():
    parser = argparse.ArgumentParser(description="プロジェクトフォルダを作成するプログラム")
    parser.add_argument('-pp','--project_path', 
                        nargs="?",  # 引数が指定されなかった場合：デフォルト値が使用されます。
                                    # 引数が1つ指定された場合：その値が使われます。
                                    # 引数が複数指定された場合：最後の値が使われます
                        default=os.getcwd(), 
                        help="プロジェクトフォルダを作成するディレクトリパス.\
                            無指定の場合はカレントディレクトリ")
    
    parser.add_argument('-pn','--project_name', 
                        required = False,
                        help="プロジェクト名")
    
    parser.add_argument('-f','--force', 
                        action = 'store_true',
                        help="強制的に作成する。")

    args = parser.parse_args()



    file=glob.glob(f"{args.project_path}"+"/*")
    
    for f in file:
        print(f)

if __name__ == "__main__":
    main()
