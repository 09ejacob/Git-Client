from PyQt5 import QtCore, QtWidgets, QtGui
import os
from git import Repo
from dotenv import load_dotenv

load_dotenv()

class GitManager:
    def __init__(self, repo_path, repo_url, username, token):
        self.repo_path = repo_path
        self.repo_url = repo_url
        self.username = username
        self.token = token
        self.https_url = self._create_https_url()

        self.repo = self._setup_repo()

    def _create_https_url(self):
        return self.repo_url.replace("https://", f"https://{self.username}:{self.token}@")

    def _setup_repo(self):
        if not os.path.exists(self.repo_path):
            print("Cloning repository...")
            return Repo.clone_from(self.https_url, self.repo_path)
        else:
            print("Repository already exists locally.")
            return Repo(self.repo_path)

    def switch_to_branch(self, branch_name):
        if branch_name in self.repo.branches:
            print(f"Switching to branch '{branch_name}'")
            self.repo.git.checkout(branch_name)
        else:
            print(f"Branch '{branch_name}' does not exist. Creating a new branch.")
            self.repo.git.checkout('-b', branch_name)
            self.repo.git.push('--set-upstream', 'origin', branch_name)

        print(f"Currently working on branch: {self.repo.active_branch}")

    def add_and_commit(self, commit_message):
        self.repo.git.add(A=True)
        self.repo.index.commit(commit_message)
        print(f"Committed with message: '{commit_message}'")

    def push(self):
        print("Pushing changes...")
        origin = self.repo.remote(name='origin')
        origin.push()
        print("Push completed.")

    def pull(self):
        print("Pulling latest changes...")
        origin = self.repo.remote(name='origin')
        origin.pull()
        print("Pull completed.")

    def get_commit_history(self):
        commits = list(self.repo.iter_commits(self.repo.active_branch))
        commit_messages = [
            f"{commit.author.name} - {commit.committed_datetime.strftime('%d-%m-%Y %H:%M:%S')} - {commit.message.strip()}"
            for commit in commits
        ]
        return commit_messages

    def get_changes(self):
        changed_files = []
        repo_status = self.repo.git.status(porcelain=True)
        if repo_status:
            changed_files = repo_status.splitlines()
        return changed_files


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, git_manager):
        self.git_manager = git_manager

        # Window setup
        MainWindow.setObjectName("Inscribed")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        MainWindow.setStyleSheet("""
                QWidget {
                    background-color: #555563;
                }

                QPushButton {
                    background-color: #d1d5ff;
                    color: black;
                    font-size: 14px; 
                    border-radius: 2px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #aeb0cf;
                }

                QLineEdit {
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 14px;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 4px;
                }

                QTextEdit {
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 14px;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 4px;
                }

                QListView {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    font-size: 14px;
                    color: #333333;
                    padding: 5px;
                }
                                             
                QListView::item:selected {
                    background-color: #6a6a7d;
                    color: white;
                }
            """)

        # Commit history
        self.commitHistory = QtWidgets.QListView(self.centralwidget)
        self.commitHistory.setGeometry(QtCore.QRect(490, 10, 700, 550))
        self.commitHistory.setObjectName("commitHistory")

        # Changes preview (QTextEdit)
        self.changesPreview = QtWidgets.QTextEdit(self.centralwidget)
        self.changesPreview.setGeometry(QtCore.QRect(10, 100, 470, 280))
        self.changesPreview.setObjectName("changesPreview")
        self.changesPreview.setReadOnly(True)  # Make it read-only to prevent user edits
        self.changesPreview.setPlaceholderText("Changes to be committed will appear here...")

        # Branch input (QLineEdit)
        self.branchInput = QtWidgets.QLineEdit(self.centralwidget)
        self.branchInput.setGeometry(QtCore.QRect(320, 55, 161, 31))
        self.branchInput.setObjectName("branchInput")
        self.branchInput.setText("main")  # Set default branch name as "main"

        # Refresh button
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(405, 15, 75, 31))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setText("Refresh")

        # Connect the refresh button to changeBranch method
        self.refreshButton.clicked.connect(self.changeBranch)

        # Branch label
        self.branchLabel = QtWidgets.QLabel(self.centralwidget)
        self.branchLabel.setGeometry(QtCore.QRect(320, 10, 60, 41))
        self.branchLabel.setObjectName("branchLabel")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.branchLabel.setFont(font)
        self.branchLabel.setStyleSheet("color: white;")

        # Title
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(50, 20, 200, 41))
        self.titleLabel.setObjectName("titleLabel")

        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: black;")

        # Commit message input
        self.commitMessageInput = QtWidgets.QTextEdit(self.centralwidget)
        self.commitMessageInput.setGeometry(QtCore.QRect(10, 400, 470, 100))
        self.commitMessageInput.setObjectName("commitMessageInput")
        self.commitMessageInput.setPlaceholderText("Enter commit message")

        # Commit button
        self.commitButton = QtWidgets.QPushButton(self.centralwidget)
        self.commitButton.setGeometry(QtCore.QRect(10, 505, 75, 23))
        self.commitButton.setObjectName("commitButton")
        self.commitButton.clicked.connect(self.commitClicked)

        # Push button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 550, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushClicked)

        # Pull button
        self.pullButton = QtWidgets.QPushButton(self.centralwidget)
        self.pullButton.setGeometry(QtCore.QRect(10, 550, 75, 23))
        self.pullButton.setObjectName("pullButton")
        self.pullButton.clicked.connect(self.pullClicked)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Inscribed"))
        self.branchLabel.setText(_translate("MainWindow", "Branch:"))
        self.titleLabel.setText(_translate("MainWindow", "Inscribed"))
        self.commitButton.setText(_translate("MainWindow", "Commit"))
        self.pushButton.setText(_translate("MainWindow", "Push"))
        self.pullButton.setText(_translate("MainWindow", "Pull"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.commitMessageInput.setPlaceholderText(_translate("MainWindow", "Enter commit message"))

    def commitClicked(self):
        commit_message = self.commitMessageInput.toPlainText().strip()

        if not commit_message:
            commit_message = "Auto commit message"

        self.git_manager.add_and_commit(commit_message)
        print(f"Commit action performed with message: '{commit_message}'")

        self.updateChangesPreview()

    def pushClicked(self):
        self.git_manager.push()
        print("Push action performed.")

    def pullClicked(self):
        self.git_manager.pull()
        print("Pull action performed.")

    def updateCommitHistory(self):
        commit_messages = self.git_manager.get_commit_history()

        model = QtGui.QStandardItemModel()

        for message in commit_messages:
            item = QtGui.QStandardItem(message)
            model.appendRow(item)

        self.commitHistory.setModel(model)
    
    def changeBranch(self):
        branch_name = self.branchInput.text().strip()
        if branch_name:
            self.git_manager.switch_to_branch(branch_name)
            print(f"Switched to branch: {branch_name}")

            self.updateCommitHistory()
            self.updateChangesPreview()

    def updateChangesPreview(self):
        try:
            changed_files = self.git_manager.get_changes()
            if changed_files:
                self.changesPreview.setPlainText("\n".join(changed_files))
            else:
                self.changesPreview.setPlainText("No changes to be committed.")
        except Exception as e:
            self.changesPreview.setPlainText(f"Error retrieving changes: {e}")


if __name__ == "__main__":
    import sys

    REPO_PATH = "C:\\Projects\\GitClient\\TestRepo\\Git-Client-Test"
    REPO_URL = "https://github.com/09ejacob/Git-Client-Test"
    USERNAME = os.getenv("GITHUB_USERNAME")
    TOKEN = os.getenv("GITHUB_TOKEN")

    git_manager = GitManager(REPO_PATH, REPO_URL, USERNAME, TOKEN)
    git_manager.switch_to_branch("main")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, git_manager)
    MainWindow.show()

    sys.exit(app.exec_())