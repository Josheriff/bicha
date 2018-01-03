class RequirementsFinder:

    def __init__(self, projects_finder):
        self.projects_finder = projects_finder

    def find_all(self):
        projects = self.projects_finder.find_all()
        if len(projects) > 0:
            return ['paso el test']  
        else:
            return []
        pass
