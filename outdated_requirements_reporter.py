from model.report import Report
from model.project_report import ProjectReport
NO_PROJECTS_FOUND_MESSAGE = 'No projects found'

class OutdatedRequirementsReporter:

    def __init__(self, projects_finder, version_checker):
        self.projects_finder = projects_finder
        self.version_checker = version_checker

    def generate_report(self):
        report = Report()
        projects = self.projects_finder.find_all()
        if len(projects) == 0:
            report.message = NO_PROJECTS_FOUND_MESSAGE
        else:
            for project in projects:
                project_report = self._generate_report_for_project(project)
                if self._any_outdated_requirement(project_report):
                    report.add_project_report(project_report)
        return report
               
    def _generate_report_for_project(self, project):
        project_report = ProjectReport(project_name=project.project_name, outdated_requirements=[])
        project_report.outdated_requirements = self._find_outdated_requirements(project.requirements)
        return project_report

    def _find_outdated_requirements(self, requirements):
        return [requirement for requirement in requirements if self.version_checker.is_outdated(requirement)]

    def _any_outdated_requirement(self, project_report):
        return len(project_report.outdated_requirements) > 0
