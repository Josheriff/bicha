from mamba import description, context, it, before
from doublex import Stub, when
from expects import expect, equal

from projects_finder import ProjectsFinder
from project import Project
from outdated_packages_reporter import (OutdatedPackagesReporter,
                                        NO_PROJECTS_FOUND_MESSAGE,
                                        ALL_PROJECTS_UP_TO_DATE)

EMPTY_PROJECTS_LIST = []
PROJECT_WITH_UP_TO_DATE_REQUIREMENTS = Project(project_name='project_with_up_to_date_requirements', requirements=['an_up_to_date_requirement'])
PROJECT_WITH_OUTDATED_REQUIREMENTS = Project(project_name='project_with_outdated_requirements', requirements=['an_outdated_requirement'])

with description('Outdated packages reporter') as self:
    with before.each:
        self.projects_finder = Stub(ProjectsFinder)
        self.reporter = OutdatedPackagesReporter(self.projects_finder)

    with context('when NO projects found'):
        with it('reports no projects found message'):
            when(self.projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)

            report = self.reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))

    with context('when projects found'):
        with context('all requirements up to date'):
            with it('reports all requirements up to date message'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_UP_TO_DATE_REQUIREMENTS])
                report = self.reporter.generate_report()
                
                expect(report).to(equal(ALL_PROJECTS_UP_TO_DATE))

        with context('A requirements is outdated'):
            with it('reports the project outdated and the requirement'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_OUTDATED_REQUIREMENTS])

                report = self.reporter.generate_report()

                expect(report).to(equal([]))
