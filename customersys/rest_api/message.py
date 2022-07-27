class message(dict):
    """
    指定要返回的数据，dict类型方便Response进行json转化
    """

    def __init__(self, status='success', code=200, message='', *args, **kwargs):
        self.content = {
            "code": code,
            "message": message,
            "status": status
        }
        for k, v in kwargs.items():
            self.content.update(v)
        super().__init__(self.content)
