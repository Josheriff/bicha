NO_PROJECTS_FOUND_MESSAGE = 'No projects found'
NO_REQUIREMENTS_MESSAGE = 'No requirements found'

class OutdatedPackagesReporter:

    def __init__(self, requirements_finder):
        self.requirements_finder = requirements_finder

    def generate_report(self):
        requirements = self.requirements_finder.find_all()
        if len(requirements) == 0:
            return NO_PROJECTS_FOUND_MESSAGE
        else:
            return NO_REQUIREMENTS_MESSAGE
