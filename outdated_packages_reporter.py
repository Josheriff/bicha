NO_PROJECTS_FOUND_MESSAGE = 'No projects found'
ALL_PROJECTS_UP_TO_DATE = 'All projects up to date'

class OutdatedPackagesReporter:

    def __init__(self, projects_finder):
        self.projects_finder = projects_finder

    def generate_report(self):
        projects = self.projects_finder.find_all()
        if len(projects) == 0:
            return NO_PROJECTS_FOUND_MESSAGE
        else:
            return ALL_PROJECTS_UP_TO_DATE
