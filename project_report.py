class ProjectReport:

    def __init__(self, project_name, outdated_requirements):
        self.project_name = project_name
        self.outdated_requirements = outdated_requirements

    def __eq__(self, other):
        return self.project_name == other.project_name and self.outdated_requirements == other.outdated_requirements
