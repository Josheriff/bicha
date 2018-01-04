NO_PROJECTS_FOUND_MESSAGE = 'No projects found'
NO_REQUIREMENTS_MESSAGE = 'No requirements found'
ALL_REQUIREMENTS_UP_TO_DATE = 'All requirements up to date'

class OutdatedPackagesReporter:

    def __init__(self, requirements_finder):
        self.requirements_finder = requirements_finder

    def generate_report(self):
        projects_requirements = self.requirements_finder.find_all()
        if len(projects_requirements) == 0:
            return NO_PROJECTS_FOUND_MESSAGE
        else:
            for project_requirements in projects_requirements:
                if len(project_requirements['requirements']) > 0:
                    return ALL_REQUIREMENTS_UP_TO_DATE
            return NO_REQUIREMENTS_MESSAGE
