import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTreeWidget,
    QTreeWidgetItem, QStatusBar, QFrame,
    QLineEdit, QPushButton, QScrollArea, QTabWidget,
)
from PyQt6.QtCore import Qt

from cassandra_client import CassandraDatabaseClient

from styles import STYLESHEET

class QueryLine(QWidget):

    def __init__(self, parent: QWidget | None = None, cassandra: CassandraDatabaseClient | None = None):
        super().__init__(parent)
        self.setObjectName("queryLine")
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)

        label = QLabel("Select:")
        label.setObjectName("selectLabel")

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("where statement")
        self.line_edit.setFixedHeight(30)

        self.btn = QPushButton("Run")
        self.btn.setFixedHeight(30)

        layout.addWidget(label)
        layout.addWidget(self.line_edit, stretch=1)
        layout.addWidget(self.btn)


class Table(QScrollArea):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(container)

    def fill(self, column_names, rows):
        for i in range(len(column_names)):
            column = column_names[i]
            cell = QLabel(column)
            cell.setObjectName("columnGridCell")
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell.setFixedHeight(40)
            self.grid.addWidget(cell, 0, i)

        r = 1
        for row in rows:
            for i in range(len(column_names)):
                cell = QLabel(str(row[i]))
                cell.setObjectName("valueGridCell")
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFixedHeight(40)
                self.grid.addWidget(cell, r, i)
            r = r + 1
    

class TabContent(QWidget):

    def __init__(self, name: str, parent: QWidget | None = None, cassandra: CassandraDatabaseClient = None):
        super().__init__(parent)
        self.name = name
        self.cassandra = cassandra

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top_bar  = QueryLine(self)
        self.grid_area = Table(self)

        layout.addWidget(self.top_bar)
        layout.addWidget(self.grid_area, stretch=1)

        # Wire Run button → grid highlight
        self.top_bar.btn.clicked.connect(
            lambda: self.select(self.top_bar.line_edit.text().strip())
        )

        self.init_table()
    
    def init_table(self):
        name_parts = self.name.split(" - ")
        keyspace = name_parts[0]
        table = name_parts[1]

        column_names = list(map(lambda x: x.column_name, self.cassandra.get_table_info(keyspace, table)))
        rows = self.cassandra.select_with_limit(column_names, table)


        self.grid_area.fill(column_names, rows)

    def select(self, where):
        while self.grid_area.grid.count():
            item = self.grid_area.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        name_parts = self.name.split(" - ")
        keyspace = name_parts[0]
        table = name_parts[1]

        column_names = list(map(lambda x: x.column_name, self.cassandra.get_table_info(keyspace, table)))

        rows = self.cassandra.select(table, where)

        self.grid_area.fill(column_names, rows)

class TablesPanel(QWidget):

    def __init__(self, parent: QWidget | None = None, cassandra: CassandraDatabaseClient | None = None):
        super().__init__(parent)
        self.setObjectName("tablesPanel")

        self.cassandra = cassandra

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        layout.addWidget(self.tabs)

    def open_tab(self, tab_name: str) -> None:
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_name:
                self.tabs.setCurrentIndex(i)
                return

        content = TabContent(tab_name, self, self.cassandra)
        index = self.tabs.addTab(content, tab_name)
        self.tabs.setCurrentIndex(index)


class TreeItem(QTreeWidgetItem):
    def __init__(self, parent: QTreeWidget | None, strings: list[str], isTable: bool = False, table: str = None, keyspace: str = None):
        super().__init__(parent, strings)
        self.isTable = isTable
        self.table = table
        self.keyspace = keyspace


class Sidebar(QWidget):
    def __init__(self, parent: QWidget | None = None, cassandra: CassandraDatabaseClient | None = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setMinimumWidth(140)

        self.cassandra = cassandra
        self._init_container()

    def _init_container(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("Connections")
        header.setObjectName("sidebarHeader")
        layout.addWidget(header)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(16)
        layout.addWidget(self.tree)

        self._populate_tree()

    def _populate_tree(self):
        keyspaces = sorted(map(lambda i: i.keyspace_name, self.cassandra.get_keyspaces()))

        cassandra_connection = TreeItem(self.tree, ["Cassandra"])
        cassandra_connection.setExpanded(True)

        keyspaces_tree = TreeItem(cassandra_connection, ["Keyspaces"])
        keyspaces_tree.setExpanded(True)

        for keyspace in keyspaces:
            keyspace_tree_item = TreeItem(keyspaces_tree, [keyspace])

            tables = sorted(map(lambda i: i.table_name, self.cassandra.get_tables_info(keyspace)))
            for table in tables:
                table_tree_item = TreeItem(keyspace_tree_item, [table], True, table, keyspace)

                for column in sorted(self.cassandra.get_table_info(keyspace, table), key=lambda i: i.column_name):
                    if column.kind == 'partition_key':
                        TreeItem(table_tree_item, ["# " + column.column_name + ", " + column.type])
                    else:
                        TreeItem(table_tree_item, ["  " + column.column_name + ", " + column.type])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cassandra Viewer")
        self.resize(1600, 800)
        self.setMinimumSize(600, 400)

        self.cassandra = CassandraDatabaseClient()

        self._build_central()
        self._build_statusbar()
        self.setStyleSheet(STYLESHEET)

    def _build_central(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)
        splitter.setChildrenCollapsible(False)

        self.sidebar      = Sidebar(self, self.cassandra)
        self.editor_panel = TablesPanel(self,  self.cassandra)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.editor_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([220, 880])

        self.setCentralWidget(splitter)

        self.sidebar.tree.itemDoubleClicked.connect(self._on_tree_item_clicked)

    def _on_tree_item_clicked(self, item: TreeItem, _column: int) -> None:
        if not item.isTable:
            return
        
        tab_name = item.keyspace + " - " + item.table
        self.editor_panel.open_tab(tab_name)

    def _build_statusbar(self):
        sb = QStatusBar()
        sb.showMessage("  Version: 0.1  ")
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)


class Application:
    def run(self):
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

