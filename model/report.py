class Report:

    def __init__(self, message=''):
        self.message = message 
        self.projects_reports = []

    def __eq__(self, other):
        return self.message == other.message and self.projects_reports == other.projects_reports

    def add_project_report(self, project_report):
        self.projects_reports.append(project_report)
