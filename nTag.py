class nTag:
    index = None            # DB 내부 인덱스
    name = None             # 사용자 지정 이름

    @staticmethod 
    def createWithRow(row):
        instance = nTag()
        instance.index = row['idx']
        instance.name = row['name']
        return instance
