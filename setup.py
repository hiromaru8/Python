from setuptools import setup, find_packages

setup(
    name='binary_file_tool',
    version='0.1.0',
    packages=find_packages(),
    # install_requires=[
    #     'argcomplete',  # 依存ライブラリがある場合
    # ],
    entry_points={
        'console_scripts': [
            'binary_file_tool=binary_file_tool.__main__:main',  # binary_file_toolコマンドで実行可能に
        ],
    },
    author='H.Y.',
    description='Binary file operation tool',
    python_requires='>=3.11',
)
