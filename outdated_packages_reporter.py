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
                project_report = self._generate_report_for_project(project)
                if self._any_outdated_requirement(project_report):
                    report.append(project_report)
            return report

    def _find_outdated_requirements(self, requirements):
        return [requirement for requirement in requirements if self.version_checker.is_outdated(requirement)]

    def _any_outdated_requirement(self, project_report):
        return len(project_report.outdated_requirements) > 0

    def _generate_report_for_project(self, project):
        project_report = ProjectReport(project_name=project.project_name, outdated_requirements=[])
        project_report.outdated_requirements = self._find_outdated_requirements(project.requirements)
        return project_report
 
