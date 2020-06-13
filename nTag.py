class nTag:
    index = None            # DB 내부 인덱스
    name = None             # 사용자 지정 이름

    def __init__(self, index, name):
        super().__init__()
        self.index = index
        self.name = name

    @staticmethod 
    def createWithRow(row):
        return nTag(row['idx'], row['name'])
