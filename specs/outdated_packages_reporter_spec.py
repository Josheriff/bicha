from mamba import description, context, it, before
from doublex import Stub, when
from expects import expect, equal

from projects_finder import ProjectsFinder
from project import Project
from project_report import ProjectReport
from version_checker import VersionChecker
from outdated_packages_reporter import (OutdatedPackagesReporter,
                                        NO_PROJECTS_FOUND_MESSAGE)

EMPTY_PROJECTS_LIST = []
PROJECT_WITH_UP_TO_DATE_REQUIREMENTS = Project(project_name='project_with_up_to_date_requirements', requirements=['an_up_to_date_requirement'])
OUTDATED_REQUIREMENT = 'an_outdated_requirement'
PROJECT_WITH_OUTDATED_REQUIREMENTS = Project(project_name='project_with_outdated_requirements', requirements=[OUTDATED_REQUIREMENT])

with description('Outdated packages reporter') as self:
    with before.each:
        self.projects_finder = Stub(ProjectsFinder)
        self.version_checker = Stub(VersionChecker)
        self.reporter = OutdatedPackagesReporter(self.projects_finder, self.version_checker)

    with context('when NO projects found'):
        with it('reports no projects found message'):
            when(self.projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)

            report = self.reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))

    with context('when projects found'):
        with context('all requirements up to date'):
            with it('reports nothing'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_UP_TO_DATE_REQUIREMENTS])
                report = self.reporter.generate_report()
                
                expect(report).to(equal([]))

        with context('A requirements is outdated'):
            with it('reports the project outdated and the requirement'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_OUTDATED_REQUIREMENTS])
                when(self.version_checker).is_outdated(OUTDATED_REQUIREMENT).returns(True)

                report = self.reporter.generate_report()

                expected_report = [ProjectReport(project_name=PROJECT_WITH_OUTDATED_REQUIREMENTS.project_name, outdated_requirements=[OUTDATED_REQUIREMENT])]
                expect(report).to(equal(expected_report))
