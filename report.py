class Report:

    def __init__(self):
        self.message = ''
        self.projects_reports = []

    def add_project_report(self, project_report):
        self.projects_reports.append(project_report)
