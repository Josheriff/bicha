NO_PROJECTS_FOUND_MESSAGE = 'No projects found'

class OutdatedPackagesReporter:

    def __init__(self, projects_finder):
        self.projects_finder = projects_finder

    def generate_report(self):
        return NO_PROJECTS_FOUND_MESSAGE 
