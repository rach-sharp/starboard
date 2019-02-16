from github import GithubObject, PaginatedList, Consts
from github.Repository import Repository


def get_starred_with_dates(named_user):
    """
    :calls: `GET /users/:user/starred <http://developer.github.com/v3/activity/starring>`_
    :rtype: :class:`github.PaginatedList.PaginatedList` of :class:`Starred`
    """
    return PaginatedList.PaginatedList(
        Starred,
        named_user._requester,
        named_user.url + "/starred",
        None,
        headers={'Accept': Consts.mediaTypeStarringPreview}
    )


class Starred(GithubObject.NonCompletableGithubObject):
    """
    This class represents Repos being starred. The reference can be found here https://developer.github.com/v3/activity/starring/#alternative-response-with-star-creation-timestamps
    """

    def __repr__(self):
        return self.get__repr__({"repository": self._repository.value.name})

    @property
    def starred_at(self):
        """
        :type: datetime.datetime
        """
        return self._starred_at.value

    @property
    def repository(self):
        """
        :type: :class:`github.Repository`
        """
        return self._repository.value

    def _initAttributes(self):
        self._starred_at = GithubObject.NotSet
        self._repository = GithubObject.NotSet
        self._url = GithubObject.NotSet

    def _useAttributes(self, attributes):
        if 'starred_at' in attributes:
            self._starred_at = self._makeDatetimeAttribute(attributes['starred_at'])
        if 'repo' in attributes:
            self._repository = self._makeClassAttribute(Repository, attributes['repo'])
