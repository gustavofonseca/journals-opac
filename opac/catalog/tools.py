import collections
from catalog import mongomodels


class Navigation(object):

    def __init__(self,
                 journal,
                 issue=None,
                 issue_lib=mongomodels.Issue):
        self._issue_lib = issue_lib

        _tmp_issues = ([(iss['data']['publication_year'], iss['data']['volume'],
                    iss['data']['order']), iss['data']['id']]
                    for iss in journal.issues)

        self._issues = sorted(_tmp_issues)
        self._issues_indexes = {_tmp_issue[1]: i for i, _tmp_issue in enumerate(self._issues)}

        self._current_id = self._issues[-1][1]
        if issue:
            self._issue = issue

        self._journal = journal

    def _load_issue(self):
        self._issue = self._issue_lib.get_issue(
                                        self._journal.acronym,
                                        self._current_id
                                        )

    @property
    def ahead(self):

        ahead = self._journal.current_ahead_documents

        if ahead > 0:
            return '/ahead/{0}/'.format(self._journal.acronym)
        else:
            return None

    @property
    def current_issue(self):
        """
        This method retrives a link to the current issue from a
        given journal.
        """

        return '/issue/{0}/{1}/'.format(
                                        self._journal.acronym,
                                        self._current_id
                                        )

    @property
    def next_issue(self):
        """
        This method retrives a link to the next issue or None
        """
        if not hasattr(self, '_issue'):
            self._load_issue()

        actual_index = self._issues_indexes[self._issue.id]

        try:
            next_issue = self._issues[actual_index + 1]
        except IndexError:
            return None

        return '/issue/{0}/{1}/'.format(
                                    self._journal.acronym,
                                    next_issue[1])

    @property
    def previous_issue(self):
        """
        This method retrives a link to the previous issue or None
        """

        if not hasattr(self, '_issue'):
            self._load_issue()

        actual_index = self._issues_indexes[self._issue.id]

        if actual_index <= 0:
            return None

        try:
            previous_issue = self._issues[actual_index - 1]
        except IndexError:
            return None

        return '/issue/{0}/{1}/'.format(
                                    self._journal.acronym,
                                    previous_issue[1])
