from PyQt5 import QtCore, QtWidgets
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
        # Check if the branch exists, and switch to it, or create it
        if branch_name in self.repo.branches:
            print(f"Switching to branch '{branch_name}'")
            self.repo.git.checkout(branch_name)
        else:
            print(f"Branch '{branch_name}' does not exist. Creating a new branch.")
            self.repo.git.checkout('-b', branch_name)
            # Set the upstream branch for the new branch
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, git_manager):
        self.git_manager = git_manager

        # Window setup
        MainWindow.setObjectName("GitBit")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Commit history
        self.commitHistory = QtWidgets.QListView(self.centralwidget)
        self.commitHistory.setGeometry(QtCore.QRect(490, 10, 401, 541))
        self.commitHistory.setObjectName("commitHistory")

        # Branch box
        self.branchBox = QtWidgets.QComboBox(self.centralwidget)
        self.branchBox.setGeometry(QtCore.QRect(320, 50, 161, 31))
        self.branchBox.setObjectName("branchBox")

        # Branch label
        self.branchLabel = QtWidgets.QLabel(self.centralwidget)
        self.branchLabel.setGeometry(QtCore.QRect(320, 10, 101, 41))
        self.branchLabel.setObjectName("branchLabel")

        # Title
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(100, 10, 81, 41))
        self.titleLabel.setObjectName("titleLabel")

        # Commit message input
        self.commitMessageInput = QtWidgets.QLineEdit(self.centralwidget)
        self.commitMessageInput.setGeometry(QtCore.QRect(10, 70, 200, 23))
        self.commitMessageInput.setObjectName("commitMessageInput")
        self.commitMessageInput.setPlaceholderText("Enter commit message")

        # Commit button
        self.commitButton = QtWidgets.QPushButton(self.centralwidget)
        self.commitButton.setGeometry(QtCore.QRect(10, 100, 75, 23))
        self.commitButton.setObjectName("commitButton")
        self.commitButton.clicked.connect(self.commitClicked)

        # Push button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushClicked)

        # Pull button
        self.pullButton = QtWidgets.QPushButton(self.centralwidget)
        self.pullButton.setGeometry(QtCore.QRect(10, 160, 75, 23))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "GitBit"))
        self.branchLabel.setText(_translate("MainWindow", "Branch:"))
        self.titleLabel.setText(_translate("MainWindow", "GitBit"))
        self.commitButton.setText(_translate("MainWindow", "Commit"))
        self.pushButton.setText(_translate("MainWindow", "Push"))
        self.pullButton.setText(_translate("MainWindow", "Pull"))
        self.commitMessageInput.setPlaceholderText(_translate("MainWindow", "Enter commit message"))


    def commitClicked(self):
        commit_message = self.commitMessageInput.text().strip()

        if not commit_message:
            commit_message = "Auto commit message"

        self.git_manager.add_and_commit(commit_message)
        print(f"Commit action performed with message: '{commit_message}'")

    def pushClicked(self):
        self.git_manager.push()
        print("Push action performed.")

    def pullClicked(self):
        self.git_manager.pull()
        print("Pull action performed.")

if __name__ == "__main__":
    import sys

    REPO_PATH = "C:\Projects\GitClient\TestRepo\Git-Client-Test"
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
