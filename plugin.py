# -*- coding: utf-8 -*-

import logging
import os

import neovim
import records

# NOTE sure we really need this
logger = logging.getLogger('nsql')


def setup_logger():
    hdlr = logging.FileHandler('/tmp/nsql.vim.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)

    logger.addHandler(hdlr)
    logger.setLevel(os.getenv('LOG_LEVEL', logging.DEBUG))


@neovim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.conn = None

    def out(self, msg):
        logger.info(msg)
        self.nvim.out_write(msg)

    @neovim.command("Query", range='', nargs='*')
    def testcommand(self, args, range):
        """Send query to Postgres.

        Args:
            args: call positional arguments
            range: cursor range if sent from visual mode

        """
        # TODO iterate until finding ";"
        # TODO or use range/line
        # TODO support export depending on args (and interactive pandas df ?)
        self.out('Command with args: {}, range: {}'.format(args, range))
        rows = self.conn.query(self.nvim.current.line)
        self.nvim.current.line = rows.first()

    @neovim.autocmd('BufEnter', pattern='*.sql', eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        """Connect to database from environment."""
        setup_logger()

        db_host = os.getenv('DB_HOST')

        if db_host:
            self.out("connecting to database:" + db_host)
            self.conn = records.Database(db_host)
        else:
            self.out("disabling plugin - no connection uri found")
