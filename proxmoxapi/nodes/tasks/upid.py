"""Module for node upid resource."""

import logging
import time
from requests.exceptions import HTTPError

from proxmoxapi.resource import Resource
from proxmoxapi.nodes.tasks.status import Status
from proxmoxapi.nodes.tasks.log import Log
from proxmoxapi.nodes.tasks import constants


class UPID(Resource):
    """Class for node upid resource."""

    def __init__(self, api, node_id, task_id):
        """
        :param api: The instance of :class:`ProxmoxAPI
            <proxmoxapi.api.ProxmoxAPI>`.
        :param str node_id: The cluster node name.
        :param str task_id: The task UPID.
        """
        super(UPID, self).__init__(api)
        self.node_id = node_id
        self.task_id = task_id
        self.url = "nodes/{node_id}/tasks/{task_id}".format(
            node_id=self.node_id,
            task_id=self.task_id)

    @property
    def status(self):
        """Property to get status resource.

        :returns: The instance of :class:`Status
            <proxmoxapi.nodes.tasks.status.Status>`.
        """
        return Status(self.api, self.node_id, self.task_id)

    @property
    def log(self):
        """Property to get log resource.

        :returns: The instance of :class:`Log
            <proxmoxapi.nodes.tasks.log.Log>`.
        """
        return Log(self.api, self.node_id, self.task_id)

    def wait_for_completion(self, timeout=None):
        """Wait for task with task_id is finished successfully.

        :param int timeout: (optional) The timeout to wait in seconds.

        :raises NodeTaskError: if exit_status != "OK".
        """
        logger = logging.getLogger(__name__)
        if timeout:
            timeout += time.time()
        while not timeout or time.time() <= timeout:
            try:
                task_status = self.status.get_status()
                if task_status == constants.TASK_STATUS_STOPPED:
                    exit_status = self.status.get_exitstatus()
                    if exit_status == constants.TASK_EXITSTATUS_OK:
                        logger.debug(
                            "Successfully fineshed task with id %s in node %s",
                            self.task_id, self.node_id)
                        return
                    else:
                        raise NodeTaskError(
                            "Task with id {task_id} error by exit_status {exit_status}".format(
                                task_id=self.task_id,
                                exit_status=exit_status))
            except HTTPError:
                logger.debug("Can not find task with id %s in node %s",
                             self.task_id, self.node_id)
            time.sleep(1)
        raise NodeTaskError("Task with id {task_id} error by timeout".format(
            task_id=self.task_id))


class NodeTaskError(Exception):
    """Class for node task error."""
