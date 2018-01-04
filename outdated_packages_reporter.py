from project_report import ProjectReport
NO_PROJECTS_FOUND_MESSAGE = 'No projects found'

class OutdatedPackagesReporter:

    def __init__(self, projects_finder, version_checker):
        self.projects_finder = projects_finder
        self.version_checker = version_checker

    def generate_report(self):
        projects = self.projects_finder.find_all()
        if len(projects) == 0:
            return NO_PROJECTS_FOUND_MESSAGE
        else:
           return [self._generate_report_for_project(project) for project in projects if self._has_outdated_requirements(project)]
            
    def _has_outdated_requirements(self, project):
        project_report = self._generate_report_for_project(project)
        return self._any_outdated_requirement(project_report)
              
    def _generate_report_for_project(self, project):
        project_report = ProjectReport(project_name=project.project_name, outdated_requirements=[])
        project_report.outdated_requirements = self._find_outdated_requirements(project.requirements)
        return project_report

    def _find_outdated_requirements(self, requirements):
        return [requirement for requirement in requirements if self.version_checker.is_outdated(requirement)]

    def _any_outdated_requirement(self, project_report):
        return len(project_report.outdated_requirements) > 0
