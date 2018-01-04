from project_report import ProjectReport
NO_PROJECTS_FOUND_MESSAGE = 'No projects found'
ALL_PROJECTS_UP_TO_DATE = 'All projects up to date'

class OutdatedPackagesReporter:

    def __init__(self, projects_finder, version_checker):
        self.projects_finder = projects_finder
        self.version_checker = version_checker

    def generate_report(self):
        projects = self.projects_finder.find_all()
        if len(projects) == 0:
            return NO_PROJECTS_FOUND_MESSAGE
        else:
            report = []
            for project in projects:
                project_report = ProjectReport(project_name=project.project_name, outdated_requirements=[])
                for requirement in project.requirements:
                    if self.version_checker.is_outdated(requirement):
                        project_report.outdated_requirements.append(requirement)
                if len(project_report.outdated_requirements) > 0:
                    report.append(project_report)
            return report
