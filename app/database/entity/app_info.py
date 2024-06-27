class AppInfo:
    def __init__(self, app_id=None, icon='', name='', content=''):
        self.app_id = app_id
        self.icon = icon
        self.name = name
        self.content = content

    def __str__(self):
        return f"{self.name} ({self.content})"
