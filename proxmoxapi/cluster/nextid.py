"""Module for cluster nextid resource."""

from proxmoxapi.resource import Resource


class NextID(Resource):
    """Class for cluster nextid resource."""
    # pylint: disable=too-few-public-methods

    url = "cluster/nextid"

    def _get(self):
        """Get next free VMID.
           If you pass an VMID it will raise an error if the ID is already used.

        :returns: The instance of :class:`requests.Response`.
        """
        return self.send_request("GET")

    def get_vmid(self):
        """Get next free VMID.
           If you pass an VMID it will raise an error if the ID is already used.

        :returns: The next VMID of cluster.
        """
        response = self._get()
        return response.json()["data"]
