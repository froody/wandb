"""Writer thread."""

import logging

from . import context, datastore

logger = logging.getLogger(__name__)


class WriteManager:
    _context_keeper: context.ContextKeeper

    def __init__(
        self,
        settings,
        record_q,
        result_q,
        context_keeper: context.ContextKeeper,
    ):
        self._settings = settings
        self._record_q = record_q
        self._result_q = result_q
        self._context_keeper = context_keeper
        self._ds = None

    def open(self):
        self._ds = datastore.DataStore()
        self._ds.open_for_write(self._settings.sync_file)

    def write(self, record):
        if not self._ds:
            self.open()

        record_type = record.WhichOneof("record_type")
        assert record_type

        self._ds.write(record)

    def finish(self):
        if self._ds:
            self._ds.close()

    def debounce(self) -> None:
        pass
