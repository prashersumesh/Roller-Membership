from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import os

class GoogleDriveUploader:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'src/service_account.json'

    def __init__(self, parent_folder_id):
        self.parent_folder_id = parent_folder_id
        self.creds = self.authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
        )
        return creds

    def file_exists(self, file_name):
        """Check if a file with the same name exists in the parent folder."""
        try:
            query = f"'{self.parent_folder_id}' in parents and name = '{file_name}' and trashed = false"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            return len(results.get('files', [])) > 0
        except HttpError as error:
            print(f"An error occurred while checking for existing file: {error}")
            return False

    def upload_pdf(self, file_path):
        """Upload a PDF file to Google Drive, skipping if the file already exists."""
        file_name = os.path.basename(file_path)

        if self.file_exists(file_name):
            print(f"File '{file_name}' already exists in the folder. Skipping upload.")
            return

        try:
            file_metadata = {
                'name': file_name,
                'parents': [self.parent_folder_id]
            }

            media_body = file_path  # You can use MediaFileUpload for larger files if needed.

            file = self.service.files().create(
                body=file_metadata,
                media_body=media_body,
                fields='id'
            ).execute()

            print(f"File '{file_name}' uploaded successfully with ID: {file['id']}")
        except HttpError as error:
            print(f"An error occurred while uploading the file: {error}")


    def delete_all_files(self):
        """Delete all files in the specified folder."""
        try:
            query = f"'{self.parent_folder_id}' in parents and trashed = false"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()

            files = results.get('files', [])
            if not files:
                print("No files to delete in the folder.")
                return

            for file in files:
                try:
                    self.service.files().delete(fileId=file['id']).execute()
                    print(f"Deleted file '{file['name']}' with ID: {file['id']}")
                except HttpError as error:
                    print(f"An error occurred while deleting file '{file['name']}': {error}")

        except HttpError as error:
            print(f"An error occurred while retrieving files to delete: {error}")

# Usage example:
if __name__ == "__main__":
    parent_folder_id = "1A8JLRUSrjvl9d5xChtRBi9HqgOuqalPp"
    uploader = GoogleDriveUploader(parent_folder_id)
    uploader.delete_all_files()
