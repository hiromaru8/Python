MESSAGE_INFO = {
    "MSG001": {
        "ja": "会員登録リクエスト",
        "desc": "新規ユーザを会員DBに登録するための要求電文"
    },
    "MSG002": {
        "ja": "会員登録レスポンス",
        "desc": "登録要求に対する結果を返す電文"
    },
    "MSG100": {
        "ja": "注文受付",
        "desc": "顧客から注文を受け付けるための電文"
    },
    "MSG200": {
        "ja": "注文結果",
        "desc": "注文受付の処理結果を返却する電文"
    },
}

print(type(MESSAGE_INFO))
print(f"{MESSAGE_INFO['MSG001']['ja']}: {MESSAGE_INFO['MSG001']['desc']}")
